# Kubernetes Probes Demo

A hands-on demonstration of **liveness**, **readiness**, and **startup** probes in Kubernetes.

## 🎯 Purpose

This project shows how different types of Kubernetes probes affect application behavior, rolling updates, and service availability. It includes:

- A simple Python (Flask) app with configurable health endpoints
- Deployment manifests with and without probes
- A startup probe example for slow-starting applications
- Scripts for quick deploy and cleanup

## 📚 What Are Probes?

| Probe | Purpose | On Failure |
|-------|---------|------------|
| **Liveness** | Is the container alive? | Container is **restarted** |
| **Readiness** | Can the container serve traffic? | Pod is **removed from Service endpoints** |
| **Startup** | Has the container finished starting? | Container is **restarted** (liveness/readiness are disabled until it passes) |

## 🚀 Quick Start

### Prerequisites
- Kubernetes cluster (minikube, kind, or any cloud)
- `kubectl` configured
- Docker (for building the image)

### Deploy

bash
# Build and push the image (or use your own registry)
docker build -t your-registry/k8s-probes-demo:latest ./app
docker push your-registry/k8s-probes-demo:latest

# Deploy
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment-with-probes.yaml
kubectl apply -f k8s/service.yaml

Test the endpoints

# Port-forward to the service
kubectl port-forward -n probes-demo svc/probes-demo 8080:80

# In another terminal:
curl http://localhost:8080/healthz   # Liveness
curl http://localhost:8080/readyz    # Readiness
curl http://localhost:8080/startupz  # Startup

 Experiments
1. No Probes (Bad Practice)
Deploy deployment-without-probes.yaml. Send traffic to a pod that isn't ready → requests fail.

2. Liveness Probe Failure
The app has a /crash endpoint that makes /healthz return 500. Kubernetes will restart the container.

bash
curl http://localhost:8080/crash
# Watch the pod restart:
kubectl get pods -n probes-demo -w

3. Readiness Probe Failure
The app has a /drain endpoint that makes /readyz return 500. The pod is removed from Service endpoints but not restarted.

bash
curl http://localhost:8080/drain
kubectl get endpoints -n probes-demo

4. Startup Probe (Slow Start)
The app has a /slow-start mode that takes 30 seconds to become ready. Without a startup probe, Kubernetes would kill it prematurely. With a startup probe, it waits.

bash
kubectl apply -f k8s/deployment-startup-probe.yaml
kubectl logs -n probes-demo -l app=probes-demo-slow

