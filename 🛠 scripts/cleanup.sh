#!/usr/bin/env bash
set -euo pipefail

echo "Deleting namespace probes-demo..."
kubectl delete namespace probes-demo --ignore-not-found=true

echo "Done."
