# app/core/runner.py
import sys
import subprocess
from pathlib import Path

# Resolve project root (two levels up from app/core/runner.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent

def trigger_batch_prescreen_stream(input_csv: str = "listings.csv", output_json: str = "batch_results.json"):
    """Spawns batch prescreen and yields stdout line by line for real-time UI streaming."""
    script_path = PROJECT_ROOT / "scripts" / "batch_prescreen.py"
    
    cmd = [
        sys.executable,
        "-u",  # Unbuffered output
        str(script_path),
        "--input", input_csv,
        "--output", output_json,
        "--slots", "Saturday, Sep 12 at 2:00 PM", "Saturday, Sep 12 at 4:30 PM"
    ]
    
    process = subprocess.Popen(
        cmd,
        cwd=str(PROJECT_ROOT),  # Run inside project root
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    if process.stdout:
        for line in iter(process.stdout.readline, ''):
            if line:
                yield line.strip()

    process.wait()
    if process.returncode != 0:
        raise RuntimeError(f"Batch execution stopped with exit code {process.returncode}")