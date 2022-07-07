def build_algorithm():
    import os
    import subprocess

    def run_shell_command(command: list[str]):
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(process.stdout.decode('utf-8'))  # TODO: to logger
        if process.stderr.decode('utf-8') != '':
            print('stderr:', process.stderr.decode('utf-8'))  # TODO: to logger

    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("Building 'hungarian_algorithm_cpp'...")  # TODO: to logger

    run_shell_command(['chmod', '+x', f'{base_dir}/init_algo.sh'])
    run_shell_command(['bash', f'{base_dir}/init_algo.sh'])
    print("Building 'hungarian_algorithm_cpp' completed.")  # TODO: to logger


build_algorithm()
