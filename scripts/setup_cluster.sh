#!/bin/bash

function start_cluster() {
  local profile=$1
  minikube start --profile "$profile" --driver=docker --cpus=2 --memory=4096
}

function destroy_cluster() {
  local profile=$1
  minikube delete --profile "$profile"
}