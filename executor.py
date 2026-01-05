import subprocess
import tempfile
import os
import shutil
import sys

def run_python(code, packages):
    workdir = tempfile.mkdtemp()

    try:
        subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            cwd=workdir,
            check=True
        )

        python = os.path.join(workdir, "venv/bin/python")
        pip = os.path.join(workdir, "venv/bin/pip")

        for pkg in packages:
            subprocess.run(
                [pip, "install", pkg],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=20
            )

        script = os.path.join(workdir, "main.py")
        with open(script, "w") as f:
            f.write(code)

        res = subprocess.run(
            [python, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=6,
            text=True
        )

        return res.stdout + res.stderr

    except subprocess.TimeoutExpired:
        return "⏱ Execution timed out"

    except Exception as e:
        return str(e)

    finally:
        shutil.rmtree(workdir, ignore_errors=True)
