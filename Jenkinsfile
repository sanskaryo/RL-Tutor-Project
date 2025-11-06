pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
    buildDiscarder(logRotator(numToKeepStr: '15'))
    disableConcurrentBuilds()
  }

  parameters {
    booleanParam(name: 'PUSH_TO_ECR', defaultValue: false, description: 'Push images to ECR and (optionally) deploy via ECS')
    string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS region for ECR/ECS')
    string(name: 'AWS_ACCOUNT_ID', defaultValue: '', description: 'AWS account ID (auto-detected if empty)')
    string(name: 'ECR_REPO_FRONTEND', defaultValue: 'rl-tutor-frontend', description: 'ECR repository for frontend image')
    string(name: 'ECR_REPO_BACKEND', defaultValue: 'rl-tutor-backend', description: 'ECR repository for backend image')
    string(name: 'ECS_CLUSTER', defaultValue: '', description: 'ECS cluster name (optional)')
    string(name: 'ECS_SERVICE', defaultValue: '', description: 'ECS service name (optional)')
    string(name: 'IMAGE_TAG', defaultValue: '', description: 'Override image tag (default: git SHA)')
  }

  environment {
    // Ensure local bin is in PATH for tools like aws installed per-user
    PATH = "/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        sh 'git submodule update --init --recursive || true'
      }
    }

    stage('Node - Install, Lint, Build') {
      steps {
        sh '''
          set -euxo pipefail
          npm ci
          npm run lint
          npm run build
        '''
      }
    }

    stage('Backend - Test') {
      steps {
        sh '''
          set -euxo pipefail
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r backend/requirements.txt
          pytest -q backend
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'backend/**/junit*.xml'
        }
      }
    }

    stage('Docker Build') {
      steps {
        sh '''
          set -euxo pipefail
          # Build frontend (Next.js) from root Dockerfile
          docker build -t rl-tutor-frontend:ci -f Dockerfile .
          # Build backend (FastAPI)
          docker build -t rl-tutor-backend:ci backend
          docker images | grep rl-tutor || true
        '''
      }
    }

    stage('Push & Deploy (optional)') {
      when {
        anyOf {
          expression { return params.PUSH_TO_ECR }
          branch 'main'
        }
      }
      steps {
        sh '''
          set -euxo pipefail
          chmod +x deploy_aws.sh || true
          AWS_REGION='${AWS_REGION}' \
          AWS_ACCOUNT_ID='${AWS_ACCOUNT_ID}' \
          ECR_REPO_FRONTEND='${ECR_REPO_FRONTEND}' \
          ECR_REPO_BACKEND='${ECR_REPO_BACKEND}' \
          ECS_CLUSTER='${ECS_CLUSTER}' \
          ECS_SERVICE='${ECS_SERVICE}' \
          IMAGE_TAG='${IMAGE_TAG}' \
          ./deploy_aws.sh
        '''
      }
    }
  }

  post {
    success {
      echo 'Build pipeline completed successfully.'
    }
    failure {
      echo 'Build pipeline failed.'
    }
    always {
      archiveArtifacts artifacts: '*/**/*.log, *.log', allowEmptyArchive: true
      cleanWs deleteDirs: true, notFailBuild: true
    }
  }
}
