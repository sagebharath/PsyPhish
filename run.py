import subprocess
import sys
import time
import os

def main():
    print("Starting PhishGuard Services...")

    # Start the PhishTank updater as a background process
    updater_process = subprocess.Popen(
        [sys.executable, "phishtank_updater.py"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    print("Started PhishTank Updater (PID: {})".format(updater_process.pid))

    # Add a slight delay to allow the updater to initialize the DB if needed
    time.sleep(2)

    # Start the FastAPI server
    try:
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"],
            check=True
        )
    except KeyboardInterrupt:
        print("\nShutting down services...")
    finally:
        # Give the updater a chance to shut down gracefully
        updater_process.terminate()
        updater_process.wait(timeout=5)
        print("Services stopped.")

if __name__ == "__main__":
    main()
