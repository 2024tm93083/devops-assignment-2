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
      steps {
        echo "Create venv, install deps and run pytest"
        sh '''
          python -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r src/requirements.txt
          pip install pytest
          python -m pytest -q
        '''
      }
    }

    stage('SonarQube Analysis') {
      // Uses Sonar plugin: withSonarQubeEnv binds server config & token
      steps {
        withCredentials([string(credentialsId: "${SONAR_TOKEN_ID}", variable: 'SONAR_TOKEN')]) {
          withSonarQubeEnv("${SONAR_SERVER_NAME}") {
            sh '''
              # sonar-project.properties should be at repo root
              # run sonar-scanner (tool installed or available on PATH)
              sonar-scanner -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_TOKEN}
            '''
          }
        }
      }
    }

    stage('Wait for Quality Gate') {
      steps {
        timeout(time: 3, unit: 'MINUTES') {
          // plugin step that waits for SonarQube quality gate result
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh "docker build -t ${IMAGE_NAME}:${env.BUILD_ID} ."
          sh "docker tag ${IMAGE_NAME}:${env.BUILD_ID} ${IMAGE_NAME}:latest"
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${IMAGE_NAME}:${env.BUILD_ID}
            docker push ${IMAGE_NAME}:latest
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      when {
        expression { return fileExists('k8s/deployment-rolling.yaml') }
      }
      steps {
        withCredentials([file(credentialsId: "${KUBECONFIG_CREDS}", variable: 'KUBECONFIG_FILE')]) {
          sh '''
            export KUBECONFIG=$KUBECONFIG_FILE
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
