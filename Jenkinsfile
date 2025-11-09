// Jenkinsfile - Full pipeline for ACEest-Fitness
// Assumptions:
// - SonarQube server configured in Jenkins with name 'SonarQube' and credential sonar-token
// - Docker Hub credentials stored as 'dockerhub-creds' (username/password)
// - kubeconfig uploaded as secret file with id 'kubeconfig-file' (optional if you want auto-deploy)
// - Docker daemon accessible from Jenkins (docker socket mounted or agent has docker)
// - Jenkins has SonarQube Scanner tool configured (or sonar-scanner available on PATH)

pipeline {
  agent any

  environment {
    IMAGE_NAME = "2024tm93083/aceest-fitness"
    DOCKERHUB_CREDS = "dockerhub-creds"
    SONAR_TOKEN_ID = "sonar-token"
    KUBECONFIG_CREDS = "kubeconfig-file"
    SONAR_SERVER_NAME = "SonarQube"        // must match Jenkins Configure System SonarQube 'Name'
    // Use host.docker.internal so Jenkins container can reach services on host (Docker Desktop)
    SONAR_HOST_URL = "http://host.docker.internal:9000"
  }

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '30'))
  }

stages {

  stage('Checkout') {
    steps {
      checkout scm
    }
  }

  stage('Unit Tests') {
    agent {
      docker {
        image 'python:3.11-slim'
        args '-u root:root --entrypoint=""'
      }
    }
    steps {
      sh '''
        echo "Running tests from $(pwd) (workspace root)"
        python --version
        # create venv and install deps
        python -m venv .venv
        . .venv/bin/activate
        pip install --upgrade pip
        pip install -r src/requirements.txt
        pip install pytest

        # Make sure the repo root is on PYTHONPATH and run tests as a module
        export PYTHONPATH="$(pwd)"
        python -m pytest -q
      '''
    }
  }

  stage('SonarQube Analysis') {
    agent {
      docker {
        image 'sonarsource/sonar-scanner-cli:latest'
        args '-u root:root --entrypoint=""'
      }
    }
    steps {
      // This wrapper sets SONAR_HOST_URL and ties scanner output to Jenkins
      withSonarQubeEnv('SonarQube') {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          sh '''
            echo "Running sonar-scanner inside SonarQube environment..."
            sonar-scanner \
              -Dsonar.token=${SONAR_TOKEN} \
              -Dsonar.projectKey=ACEest-Fitness \
              -Dsonar.sources=src
          '''
        }
      }
    }
  }

  stage('Wait for Quality Gate') {
    steps {
      echo "Skipping SonarQube quality gate wait for local testing"
    }
  }

  stage('Build and Push Docker Image') {
    agent {
      docker {
        image 'docker:27.2.0-cli'   // lightweight docker CLI image
        args '-v /var/run/docker.sock:/var/run/docker.sock --entrypoint=""'
      }
    }
    steps {
      withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
        sh '''
          docker version
          echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
          docker build -t ${IMAGE_NAME}:${BUILD_ID} .
          docker tag ${IMAGE_NAME}:${BUILD_ID} ${IMAGE_NAME}:latest
          docker push ${IMAGE_NAME}:${BUILD_ID}
          docker push ${IMAGE_NAME}:latest
        '''
      }
    }
  }

  stage('Deploy to Kubernetes') {
    when {
      expression { return fileExists('k8s/deployment-rolling.yaml') }
    }
    agent {
      docker {
        image 'bitnami/kubectl:latest'
        args '--entrypoint=""'
      }
    }
    steps {
      withCredentials([file(credentialsId: "${KUBECONFIG_CREDS}", variable: 'KUBECONFIG_FILE')]) {
        sh '''
          export KUBECONFIG=$KUBECONFIG_FILE
          kubectl version --client
          kubectl apply -f k8s/deployment-rolling.yaml
          kubectl apply -f k8s/service.yaml
          kubectl rollout status deployment/aceest-deployment --timeout=120s || (kubectl rollout undo deployment/aceest-deployment && exit 1)
        '''
      }
    }
  }
}


  post {
    success {
      echo "Pipeline finished successfully: ${env.BUILD_ID}"
    }
    failure {
      echo "Build failed. Investigate console output."
    }
    always {
      // optional cleanup
      sh 'docker system prune -f || true'
    }
  }
}
