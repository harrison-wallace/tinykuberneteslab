#!/bin/bash

source ./setup_cluster.sh

function run_q1_lab() {
  local profile="cka-lab-q1"
  if ! minikube status --profile "$profile" > /dev/null 2>&1; then
    start_cluster "$profile"
  fi
  kubectl apply -f ../manifests/q1-pod.yaml
  kubectl wait --for=condition=Ready pod/test-pod --timeout=60s
  kubectl logs test-pod | grep "error" > ../data/logs/q1_error_logs.txt
}

function cleanup_q1_lab() {
  local profile="cka-lab-q1"
  kubectl delete -f ../manifests/q1-pod.yaml 2>/dev/null
  destroy_cluster "$profile"
  rm -f ../data/logs/q1_error_logs.txt
}

case "$1" in
  "start") run_q1_lab ;;
  "destroy") cleanup_q1_lab ;;
  *) echo "Usage: $0 {start|destroy}" ;;
esac