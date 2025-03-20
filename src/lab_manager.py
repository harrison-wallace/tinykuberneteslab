import subprocess
import json
import os

# Use os.getcwd() to get the project root when running as a module
BASE_DIR = os.getcwd()
if not os.path.basename(BASE_DIR) == "tinykuberneteslab":
    raise ValueError(f"BASE_DIR is incorrect: {BASE_DIR}. Expected to end with 'tinykuberneteslab'.")

STATUS_FILE = os.path.join(BASE_DIR, "data", "lab_status.json")
LOG_DIR = os.path.join(BASE_DIR, "data", "logs")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

def initialize_status_file():
    if not os.path.exists(STATUS_FILE) or os.path.getsize(STATUS_FILE) == 0:
        with open(STATUS_FILE, "w") as f:
            json.dump({}, f, indent=2)

def load_status():
    initialize_status_file()
    with open(STATUS_FILE, "r") as f:
        content = f.read().strip()
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                save_status({})
                return {}
    return {}

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)

def start_lab(lab, output_callback=None):
    status = load_status()
    if lab in status and status[lab]["running"]:
        return f"Lab {lab} already running."
    
    script_path = os.path.join(SCRIPTS_DIR, "q1_pod_management.sh")
    process = subprocess.Popen(["bash", script_path, "start"],
                               cwd=SCRIPTS_DIR,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    
    output = []
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            output.append(line.strip())
            if output_callback:
                output_callback(line.strip())
    
    if process.returncode == 0:
        status[lab] = {"running": True, "logs": os.path.join(LOG_DIR, "q1_error_logs.txt")}
        save_status(status)
        return "\n".join(output)
    return f"Error: {process.returncode}\n" + "\n".join(output)

def destroy_lab(lab, output_callback=None):
    status = load_status()
    if lab not in status or not status[lab]["running"]:
        return f"Lab {lab} not running."
    
    script_path = os.path.join(SCRIPTS_DIR, "q1_pod_management.sh")
    process = subprocess.Popen(["bash", script_path, "destroy"],
                               cwd=SCRIPTS_DIR,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    
    output = []
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            output.append(line.strip())
            if output_callback:
                output_callback(line.strip())
    
    if process.returncode == 0:
        status[lab]["running"] = False
        save_status(status)
        return "\n".join(output)
    return f"Error: {process.returncode}\n" + "\n".join(output)

def get_status(lab):
    status = load_status()
    if lab in status:
        logs = ""
        log_path = status[lab].get("logs")
        if log_path and os.path.exists(log_path):
            with open(log_path, "r") as f:
                logs = f.read()
        return {
            "running": status[lab]["running"],
            "logs": logs
        }
    return {"running": False, "logs": "Not started yet."}