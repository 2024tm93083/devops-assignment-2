# Assignment-2: DevOps CI/CD Pipeline Implementation for ACEest Fitness & Gym

### Course

**Introduction to DevOps (Merged – CSIZG514 / SEZG514)**

### Student Details

**Name:** Kannan G.B.
**BITS ID:** 2024TM93083
**Institution:** BITS Pilani, Work Integrated Learning Programmes
**Date:** November 2025

---

## 1. Objective

To implement a fully automated CI/CD pipeline for the *ACEest Fitness & Gym* application using modern DevOps tools and practices. The pipeline automates the entire software delivery process from code commit to deployment on Kubernetes.

---

## 2. Learning Outcomes

* Design and implement a complete CI/CD pipeline.
* Integrate **Git**, **Jenkins**, **SonarQube**, **Docker**, and **Kubernetes**.
* Automate build, test, analysis, and deployment stages.
* Demonstrate continuous integration and continuous delivery using industry tools.

---

## 3. Tools and Technologies Used

| Category           | Tool / Technology        | Purpose                           |
| ------------------ | ------------------------ | --------------------------------- |
| Version Control    | Git & GitHub             | Source code management            |
| CI/CD Server       | Jenkins                  | Pipeline automation               |
| Testing            | Pytest                   | Unit test automation              |
| Code Quality       | SonarQube                | Static analysis and quality gate  |
| Containerization   | Docker                   | Build application images          |
| Container Registry | Docker Hub               | Host and version Docker images    |
| Orchestration      | Minikube (Kubernetes)    | Deployment and service management |
| Runtime            | Docker Desktop (Windows) | Local container runtime           |

---

## 4. Implementation Overview

### 4.1 Version Control Setup (Git & GitHub)

* Repository: [https://github.com/2024tm93083/devops-assignment-2](https://github.com/2024tm93083/devops-assignment-2)
* Files committed: `src/`, `tests/`, `requirements.txt`, `Dockerfile`, `k8s/`, and `Jenkinsfile`.
* Version tags created:

  ```bash
  git tag v1.0
  git tag v1.1
  git tag v1.2
  git tag v1.3
  git push origin --tags
  ```

### 4.2 Continuous Integration (Jenkins)

Stages in Jenkinsfile:

1. **Checkout** code from GitHub.
2. **Unit Tests** via Pytest.
3. **SonarQube Analysis** for code quality.
4. **Build Docker Image.**
5. **Push Image to Docker Hub.**
6. **Deploy to Kubernetes.**
7. **Health check verification.**

Result: Jenkins pipeline executed end-to-end successfully (`Finished: SUCCESS`).

### 4.3 Continuous Testing

Pytest integrated into pipeline. Jenkins output:

```
3 passed in 0.01s
```

Ensures continuous feedback and regression testing.

### 4.4 Code Quality Integration (SonarQube)

* SonarQube URL: `http://host.docker.internal:9000`
* Configured via `withSonarQubeEnv` in Jenkins.
* Project key: `ACEest-Fitness`
* Result: **Analysis Successful** and **Quality Gate Passed**.

### 4.5 Build Automation (Docker)

Dockerfile builds Python Flask app and exposes port 5000.
Image successfully built and pushed to Docker Hub:

* Repository: [https://hub.docker.com/r/2024tm93083/aceest-fitness](https://hub.docker.com/r/2024tm93083/aceest-fitness)
* Tags: `latest`, build IDs (e.g., `23`).

### 4.6 Continuous Deployment (Kubernetes / Minikube)

Deployment: `k8s/deployment-rolling.yaml`
Service: `k8s/service.yaml`

Verification:

```
$ kubectl get pods -l app=aceest
2 Pods Running

$ kubectl get svc aceest-service
NodePort: 30001
```

### 4.7 Verification & Endpoint

Minikube tunnel created using `minikube service aceest-service`.

* Endpoint: `http://127.0.0.1:62623/health`
* Output: `{ "status": "ok" }`

---

## 5. Results Summary

| Stage               | Status     | Evidence                                 |
| ------------------- | ---------- | ---------------------------------------- |
| Version Control     | ✅ Complete | Public GitHub repo with commits and tags |
| Jenkins CI          | ✅ Success  | `Finished: SUCCESS` in Jenkins console   |
| Unit Testing        | ✅ Passed   | Pytest output: `3 passed`                |
| SonarQube           | ✅ Passed   | Sonar dashboard Quality Gate Passed      |
| Docker Build & Push | ✅ Success  | Image pushed to Docker Hub               |
| Kubernetes Deploy   | ✅ Success  | 2 pods running, NodePort exposed         |
| Endpoint            | ✅ Verified | Health check JSON response               |

---

## 6. Screenshots (Attach in PDF)

| # | Screenshot          | Description                                      |
| - | ------------------- | ------------------------------------------------ |
| 1 | GitHub Repository   | Showing all project files & Jenkinsfile          |
| 2 | Jenkins Console     | Pipeline ending with `Finished: SUCCESS`         |
| 3 | SonarQube Dashboard | Project quality gate passed                      |
| 4 | Docker Hub          | Repo with tags `latest`, build number            |
| 5 | Kubernetes CLI      | `kubectl get pods` and `kubectl get svc` outputs |
| 6 | Browser Output      | `/health` endpoint showing `{ "status": "ok" }`  |

---

## 7. Challenges & Resolutions

| Issue                              | Resolution                                       |
| ---------------------------------- | ------------------------------------------------ |
| Jenkins missing Docker CLI         | Built custom Jenkins image `jenkins-with-docker` |
| Permission Denied on Docker Socket | Ran Jenkins container with `-u root`             |
| Sonar Scanner not linked           | Used `withSonarQubeEnv` block                    |
| NodePort not reachable             | Used `minikube service` tunnel                   |

---

## 8. Learning Outcomes

* Implemented an automated pipeline integrating all DevOps stages.
* Gained hands-on experience with **Jenkins**, **SonarQube**, and **Kubernetes**.
* Understood the synergy between CI and CD in modern delivery workflows.

---

## 9. Conclusion

The project successfully demonstrates a complete CI/CD pipeline for *ACEest Fitness & Gym*, automating testing, quality validation, containerization, and deployment. All assignment deliverables were achieved.

✅ **Assignment Objectives Fully Achieved.**

---

