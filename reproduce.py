"""One-command live collection; reruns resume existing archived work."""
import json
from pathlib import Path
import subprocess
import sys
import urllib.request

root = Path(__file__).parent
if not (root/'data'/'arms.json').exists():
    subprocess.run([sys.executable, str(root/'arms.py')], check=True)
if not (root/'stats-before.json').exists():
    with urllib.request.urlopen('https://1f916.ai/api/stats', timeout=30) as r:
        (root/'stats-before.json').write_bytes(r.read())
subprocess.run([sys.executable, str(root/'outcomes.py')], check=True)
subprocess.run([sys.executable, str(root/'analyze.py')], check=True)
