from typing import Tuple


def build_algorithm():
    import subprocess

    def run_shell_command(command: list[str]):
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(process.stdout.decode('utf-8'))  # TODO: to logger
        if process.stderr.decode('utf-8') != '':
            print('stderr:', process.stderr.decode('utf-8'))

    print("Building 'hungarian_algorithm_cpp'...")
    run_shell_command(['chmod', '+x', 'init_algo.sh'])
    run_shell_command(['bash', 'init_algo.sh'])


build_algorithm()
