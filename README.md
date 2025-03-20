# tinykuberneteslab

## CKA Lab Practice

A terminal-based Kubernetes lab tool for CKA exam practice, built with Python, Minikube, Docker, Rich, and Curses.

## Features
- Runs on Ubuntu Server with Minikube.
- Interactive TUI to start, destroy, and monitor labs.
- JSON-based state tracking.
- Supports Q1: "Monitor pod logs and extract errors."

## Prerequisites
- Python 3, Minikube, kubectl, Docker (installed via `setup.sh`)
- Recommend creating a venv for the repo

## Setup
1. Clone and install prerequisites
   ```bash
   git clone https://github.com/yourusername/tinykuberneteslab.git
   cd tinykuberneteslab
   ./setup.sh

2. Start the Lab:
- Run python3 -m src and select "Start Lab Q1".
- Wait for the lab to start (you’ll see Minikube output).

## Roadmap

- [ ] Lab questions/expected output 
- [ ] 8 Catagorys of questions

## Cheatsheet: Interacting with the Kubernetes Lab (`q1`) (Example)

### Lab Overview
- **Cluster**: Minikube profile `cka-lab-q1` (running locally with the Docker driver).
- **Pod**: `test-pod` (runs an `nginx` container with a custom command to print `error: test error message` and sleep).

---

### 1. Interacting with the Minikube Cluster
These commands help you manage the Kubernetes cluster and its resources using `kubectl`.

#### Check Cluster Status
Verify that the Minikube cluster is running:
```bash
minikube status --profile cka-lab-q1
```
- **Expected Output**:
  ```
  cka-lab-q1
  host: Running
  kubelet: Running
  apiserver: Running
  kubeconfig: Configured
  ```

#### Set `kubectl` Context
Ensure `kubectl` is using the correct cluster context:
```bash
kubectl config current-context
```
- **Expected Output**: `cka-lab-q1`
- If incorrect, set it:
  ```bash
  kubectl config use-context cka-lab-q1
  ```

#### List All Pods
See the pods running in the cluster:
```bash
kubectl get pods
```
- **Expected Output**:
  ```
  NAME       READY   STATUS    RESTARTS   AGE
  test-pod   1/1     Running   0          <age>
  ```

#### List System Pods
View pods in the `kube-system` namespace (Minikube’s control plane components):
```bash
kubectl get pods -n kube-system
```

#### View Pod Logs
Check the logs of the `test-pod` (contains the message printed by the custom command):
```bash
kubectl logs test-pod
```
- **Expected Output**:
  ```
  error: test error message
  ```

#### Describe the Pod
Get detailed information about the `test-pod` (useful for debugging):
```bash
kubectl describe pod test-pod
```
- **Output**: Includes pod status, events, and container details.

#### List All Resources
See all resources in the cluster (pods, services, etc.):
```bash
kubectl get all
```

#### Delete the Pod (if needed)
Manually delete the `test-pod` (it will be recreated if the lab is still running):
```bash
kubectl delete pod test-pod
```

#### Stop the Cluster
Stop the Minikube cluster (if you want to pause it):
```bash
minikube stop --profile cka-lab-q1
```

#### Delete the Cluster
Delete the Minikube cluster (if you want to start fresh):
```bash
minikube delete --profile cka-lab-q1
```

---

### 2. Interacting with the Pod (`test-pod`)
These commands let you access and explore the `test-pod` directly.

#### Open a Shell in the Pod
Access the `test-pod` container to run commands inside it:
```bash
kubectl exec -it test-pod -- sh
```
- **Expected Prompt**:
  ```
  / #
  ```
- **Example Commands Inside the Pod**:
  - Check the current directory:
    ```bash
    pwd
    ```
    - **Output**: `/`
  - List files:
    ```bash
    ls
    ```
    - **Output**: Files in the `nginx` container’s root directory (e.g., `bin`, `etc`, `usr`).
  - Print a message:
    ```bash
    echo "Hello from inside the pod"
    ```
  - Exit the shell:
    ```bash
    exit
    ```

#### Alternative Shell (if `sh` fails)
If `sh` isn’t available, try `bash`:
```bash
kubectl exec -it test-pod -- /bin/bash
```
- **Note**: The `nginx` image has `sh`, so this shouldn’t be necessary.

#### Run a Command in the Pod (Non-Interactive)
Execute a command inside the pod without opening a shell:
```bash
kubectl exec test-pod -- echo "Hello from the pod"
```
- **Expected Output**:
  ```
  Hello from the pod
  ```

#### Copy Files from the Pod
Copy a file from the pod to your local machine (e.g., the `nginx` config file):
```bash
kubectl cp test-pod:/etc/nginx/nginx.conf ./nginx.conf
```
- **Output**: Creates `nginx.conf` in your current directory.

#### Copy Files to the Pod
Copy a file from your local machine to the pod:
```bash
kubectl cp ./local-file.txt test-pod:/tmp/local-file.txt
```
- **Verify Inside the Pod**:
  ```bash
  kubectl exec test-pod -- cat /tmp/local-file.txt
  ```

#### View Pod Resource Usage
Check the CPU and memory usage of the `test-pod`:
```bash
kubectl top pod test-pod
```
- **Expected Output**:
  ```
  NAME       CPU(cores)   MEMORY(bytes)
  test-pod   <value>m     <value>Mi
  ```
- **Note**: Requires metrics-server to be enabled in Minikube. Enable it if needed:
  ```bash
  minikube addons enable metrics-server --profile cka-lab-q1
  ```

---