import json
import pathlib
import subprocess
import time

CTX = pathlib.Path("context")
CTX.mkdir(exist_ok=True)
(CTX / "Dockerfile").write_text(
    'FROM docker.io/library/busybox:latest\n'
    'CMD ["sh", "-c", "echo built-by-buildit-through-the-controller"]\n'
)

def call(*args):
    p = subprocess.run(["buildit", *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"buildit {args[0]} exited {p.returncode}: {p.stderr[-2000:]}")
    return json.loads(p.stdout) if p.stdout.strip() else {}

reply = call("build", "--no-wait", "-c", str(CTX.resolve()), "-f", "Dockerfile", "--timeout", "300")
build_id = reply["build_id"]
print(f"submitted {build_id}", flush=True)
while True:
    status = call("status", build_id)
    state = status.get("status")
    print(f"state: {state}", flush=True)
    if state != "running":
        break
    time.sleep(5)
if state != "succeeded":
    print(json.dumps(call("logs", build_id))[-3000:])
    raise SystemExit(f"build {state}")
print(json.dumps({"digest": status.get("digest") or build_id}))
