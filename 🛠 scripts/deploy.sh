#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="probes-demo"
IMAGE="${1:-your-registry/k8s-probes-demo:latest}"

echo "Building image..."
docker build -t "${IMAGE}" ./app

echo "Pushing image..."
docker push "${IMAGE}"

echo "Applying manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment-with-probes.yaml
kubectl apply -f k8s/service.yaml

echo "Waiting for rollout..."
kubectl rollout status deployment/probes-demo -n "${NAMESPACE}"

echo "Done. Pods:"
kubectl get pods -n "${NAMESPACE}"
