#!/usr/bin/env bash
set -euo pipefail

# Run the project locally using Docker Compose
# Usage:
#   ./run_local.sh up       # build and start services
#   ./run_local.sh down     # stop and remove services
#   ./run_local.sh restart  # restart services
#   ./run_local.sh build    # rebuild images
#   ./run_local.sh logs     # tail logs
#   ./run_local.sh ps       # show status

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"

compose() {
  if docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" "$@"
  else
    docker-compose -f "$COMPOSE_FILE" "$@"
  fi
}

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: $1 is not installed or not in PATH" >&2
    exit 1
  fi
}

print_endpoints() {
  cat <<EOF

Services are starting. Endpoints you can try:
- Nginx reverse proxy:   http://localhost/
- Frontend (Vite web):   http://localhost:5173/
- Backend (FastAPI):     http://localhost:8000/docs

Compose helpers:
- ./run_local.sh logs    # follow logs
- ./run_local.sh down    # stop all
EOF
}

cmd=${1:-up}

require docker

case "$cmd" in
  up)
    echo "Building and starting containers..."
    compose up -d --build
    print_endpoints
    ;;
  down)
    echo "Stopping and removing containers..."
    compose down -v
    ;;
  restart)
    echo "Restarting containers..."
    compose down -v
    compose up -d --build
    print_endpoints
    ;;
  build)
    echo "Rebuilding images..."
    compose build --no-cache
    ;;
  logs)
    echo "Tailing logs (Ctrl+C to exit)..."
    compose logs -f --tail=200
    ;;
  ps)
    compose ps
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    echo "Usage: $0 {up|down|restart|build|logs|ps}" >&2
    exit 2
    ;;
fi
