import subprocess

output = subprocess.run(["getprop"], capture_output=True, text=True)

if output.returncode == 0:
    print("System Properties:")
    print(output.stdout)
else:
    print("Error running `getprop` command:")
    print(output.stderr)