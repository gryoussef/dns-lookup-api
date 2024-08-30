# DNS Lookup API

## Overview
This repository contains a DNS Lookup API application written in Python that uses a PostgreSQL database to store successful queries. The application is containerized using Docker, orchestrated with Docker Compose, and deployed using Helm on Kubernetes.

## Directory Structure
```
.github/
  workflows/    # GitHub Actions workflows
chart/          # Helm chart
  Chart.yaml    # Helm chart metadata
  templates/    # Kubernetes resource templates
  values.yaml   # Default configuration values
docker-compose.yml # Docker Compose configuration
Dockerfile      # Docker image build instructions
requirements.txt # Python dependencies
src/            # Source code
  api.py        # API endpoints
  database.py   # Database interactions
  dependencies.py # Dependency injection
  main.py       # Application entry point
  settings.py   # Configuration settings
  utils.py      # Utility functions
test/           # Unit tests
  mock_database.py # Mock database for testing
  test_database.py # Database tests
  test_endpoints.py # API endpoint tests
  test_utils.py # Utility function tests
```
## Run it with Docker compose

To run the application using Docker Compose, execute the following command in the root directory of the repository:
```
docker-compose up -d --build
```

## Helm chart

The Helm chart for the DNS Lookup API application is located in the chart/ directory. It includes:

- Chart.yaml: Defines chart metadata.
- values.yaml: Contains default configuration values (e.g., Docker image, database credentials).
templates/ directory:
- app-deployment.yaml: Deploys the application.
- app-service.yaml: Exposes the application via a NodePort service.
- configmap.yaml: Stores database configuration.
- secret.yaml: Stores sensitive database credentials.
- db-statefulset.yaml: Deploys PostgreSQL as a StatefulSet.
- db-service.yaml: Exposes the database.
- persistent-volume.yaml: Defines the PersistentVolume.
- persistent-volume-claim.yaml: Defines the PersistentVolumeClaim.

These components collectively deploy and manage the DNS Lookup API and its PostgreSQL database on Kubernetes.

## CI/CD
### GitHub Actions

The CI pipeline for this repository, defined in the `.github/workflows/ci.yml` file, consists of three main jobs:

`test-and-lint`: This job sets up Python 3.9, installs dependencies from requirements.txt, and runs tests with pytest and linting with flake8.

`build-and-push`: This job sets up Docker Buildx, logs into DockerHub using credentials stored in GitHub Secrets, builds the Docker image for the application, and pushes it to [DockerHub repository](https://hub.docker.com/r/gryoussef/dns-lookup-api/tags) with tags based on the commit SHA and latest .

`package-helm`: This job installs Helm, packages the Helm chart, and uploads it to a Github actions artifacts.

The pipeline is triggered on pushes and pull requests to the master branch.

