# devops-assignment-2

This repository automates the CI/CD pipeline for ACEest Fitness &amp; Gym. It implements DevOps principles to ensure continuous delivery and quality. The pipeline integrates Git/GitHub , Jenkins , Pytest , SonarQube , Docker , and Kubernetes/Minikube . Key strategies include Blue-Green and Canary deployments

## Run Python application

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r src/requirements.txt

# Run server
python -m src.app

```

## Docker

### Build image locally

```bash
docker build -t 2024tm93083/aceest-fitness:local-latest .
```

### Run container and test endpoints

```bash
docker run --rm -p 5000:5000 2024tm93083/aceest-fitness:local-latest
```

```bash
docker run --rm 2024tm93083/aceest-fitness:local-latest pytest -q
```

# run pytest using python module mode (this preserves package import semantics)

```bash
python -m pytest -q
```
