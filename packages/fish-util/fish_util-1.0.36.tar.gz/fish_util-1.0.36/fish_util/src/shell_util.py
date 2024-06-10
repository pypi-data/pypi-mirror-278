import subprocess


def execute_cmd(shell_command):
    print(f"shell_command: {shell_command}")
    process = subprocess.run(
        shell_command,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return_code = process.returncode
    output = process.stdout.decode("utf-8")
    error = process.stderr.decode("utf-8")
    print(f"return_code: {return_code}")
    print(f"output: {output}")
    print(f"error: {error}")
    return return_code, output, error
