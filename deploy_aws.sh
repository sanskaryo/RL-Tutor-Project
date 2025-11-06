#!/usr/bin/env bash
set -euo pipefail

# Deploys frontend (Next.js) and backend (FastAPI) Docker images to AWS ECR
# and optionally triggers an ECS service rollout. Assumes AWS CLI v2 and Docker
# are installed and configured on this machine/agent.
#
# Environment variables (override as needed):
#   AWS_REGION           - AWS region (default: us-east-1)
#   AWS_ACCOUNT_ID       - Your AWS account ID (auto-detected if missing)
#   ECR_REPO_FRONTEND    - ECR repo name for frontend (default: rl-tutor-frontend)
#   ECR_REPO_BACKEND     - ECR repo name for backend  (default: rl-tutor-backend)
#   IMAGE_TAG            - Image tag (default: git SHA or timestamp)
#   PUSH_LATEST          - Also push :latest tag (default: true)
#   ECS_CLUSTER          - If set, ECS cluster name to trigger rollout
#   ECS_SERVICE          - If set, ECS service name to trigger rollout
#
# Examples:
#   ./deploy_aws.sh
#   AWS_REGION=eu-west-1 IMAGE_TAG=staging ./deploy_aws.sh
#   ECS_CLUSTER=my-cluster ECS_SERVICE=my-service ./deploy_aws.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

AWS_REGION="${AWS_REGION:-us-east-1}"
ECR_REPO_FRONTEND="${ECR_REPO_FRONTEND:-rl-tutor-frontend}"
ECR_REPO_BACKEND="${ECR_REPO_BACKEND:-rl-tutor-backend}"
PUSH_LATEST="${PUSH_LATEST:-true}"

if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
  IMAGE_TAG_DEFAULT="$(git rev-parse --short HEAD)"
else
  IMAGE_TAG_DEFAULT="$(date +%Y%m%d%H%M%S)"
fi
IMAGE_TAG="${IMAGE_TAG:-$IMAGE_TAG_DEFAULT}"

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: $1 is not installed or not in PATH" >&2
    exit 1
  fi
}

require aws
require docker

# Resolve AWS account ID if not provided
if [[ -z "${AWS_ACCOUNT_ID:-}" ]]; then
  AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
fi

ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
FRONTEND_IMAGE="$ECR_URI/$ECR_REPO_FRONTEND"
BACKEND_IMAGE="$ECR_URI/$ECR_REPO_BACKEND"

# Ensure ECR repos exist
ensure_repo() {
  local repo="$1"
  if ! aws ecr describe-repositories --repository-names "$repo" --region "$AWS_REGION" >/dev/null 2>&1; then
    echo "Creating ECR repository: $repo"
    aws ecr create-repository --repository-name "$repo" --image-scanning-configuration scanOnPush=true --region "$AWS_REGION" >/dev/null
  fi
}

ensure_repo "$ECR_REPO_FRONTEND"
ensure_repo "$ECR_REPO_BACKEND"

# Login to ECR
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_URI"

# Build images
echo "Building frontend image..."
docker build -t "$FRONTEND_IMAGE:$IMAGE_TAG" -f Dockerfile .

echo "Building backend image..."
docker build -t "$BACKEND_IMAGE:$IMAGE_TAG" backend

# Optional latest tag
if [[ "$PUSH_LATEST" == "true" ]]; then
  docker tag "$FRONTEND_IMAGE:$IMAGE_TAG" "$FRONTEND_IMAGE:latest"
  docker tag "$BACKEND_IMAGE:$IMAGE_TAG" "$BACKEND_IMAGE:latest"
fi

# Push images
echo "Pushing frontend image: $FRONTEND_IMAGE:$IMAGE_TAG"
docker push "$FRONTEND_IMAGE:$IMAGE_TAG"
if [[ "$PUSH_LATEST" == "true" ]]; then docker push "$FRONTEND_IMAGE:latest"; fi

echo "Pushing backend image:  $BACKEND_IMAGE:$IMAGE_TAG"
docker push "$BACKEND_IMAGE:$IMAGE_TAG"
if [[ "$PUSH_LATEST" == "true" ]]; then docker push "$BACKEND_IMAGE:latest"; fi

# Trigger ECS rollout if configured
if [[ -n "${ECS_CLUSTER:-}" && -n "${ECS_SERVICE:-}" ]]; then
  echo "Triggering ECS service rollout for $ECS_CLUSTER/$ECS_SERVICE"
  aws ecs update-service \
    --cluster "$ECS_CLUSTER" \
    --service "$ECS_SERVICE" \
    --force-new-deployment \
    --region "$AWS_REGION" >/dev/null
  echo "ECS deployment triggered. Verify status in the AWS Console."
else
  echo "ECS_CLUSTER and/or ECS_SERVICE not set. Skipping ECS rollout."
fi

cat <<EOF

Deployment complete
- AWS Account:     $AWS_ACCOUNT_ID
- Region:          $AWS_REGION
- Frontend Image:  $FRONTEND_IMAGE:$IMAGE_TAG
- Backend Image:   $BACKEND_IMAGE:$IMAGE_TAG
- Also pushed :latest: $PUSH_LATEST
- ECS Rollout:     ${ECS_CLUSTER:-<not set>}/${ECS_SERVICE:-<not set>}
EOF
