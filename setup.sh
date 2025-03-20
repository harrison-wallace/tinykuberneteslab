#!/bin/bash

echo "Updating package list..."
sudo apt update -y

echo "Installing prerequisites..."
sudo apt install -y curl docker.io python3 python3-pip

echo "Installing Minikube..."
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

echo "Installing kubectl..."
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

echo "Starting Docker..."
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

echo "Installing Python dependencies..."
pip3 install rich

echo "Setup complete! Log out and back in for Docker group changes."