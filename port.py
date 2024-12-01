def kill_port():
    # Specify the port to check
    port = 8000

    try:
        if platform.system() == "Windows":
            # For Windows, use netstat to find the process
            result = subprocess.run(
                ["netstat", "-ano", "|", "findstr", f":{port}"],
                capture_output=True, text=True, shell=True
            )
            lines = result.stdout.splitlines()

            # Parse the output to get the PID (Process ID)
            if lines:
                pid = int(lines[0].split()[-1])  # Get the last column (PID)
                print(f"Terminating process on port {port} with PID {pid}")

                # Kill the process using taskkill
                subprocess.run(["taskkill", "/PID", str(pid), "/F"])
        else:
            # Find the process using the port
            result = subprocess.run(
                ["lsof", "-i", f":{port}"], capture_output=True, text=True
            )
            lines = result.stdout.splitlines()

            # Parse the output to get the PID (Process ID)
            if len(lines) > 1:  # First line is the header, skip it
                pid = int(lines[1].split()[1])  # Extract PID from the output
                print(f"Terminating process on port {port} with PID {pid}")

                # Kill the process
                os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"Failed to free port {port}: {e}")
