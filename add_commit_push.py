import subprocess

counter_file = ".counter"
try:
    with open(counter_file, "r") as f:
        count = int(f.read().strip())
except (FileNotFoundError, ValueError):
    count = 1

commit_msg = f"conta-numeri {count}"

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push", "origin", "main"])

with open(counter_file, "w") as f:
    f.write(str(count + 1))