import subprocess

def run_command():
    # This is intentionally unsafe for testing Bandit
    subprocess.call("ls -la", shell=True)
