def build_algorithm():
    import os
    import subprocess

    import logging

    logger = logging.getLogger('django')

    def run_shell_command(command: list[str]):
        process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        logger.info(process.stdout.decode('utf-8'))
        if process.stderr.decode('utf-8') != '':
            logger.info('stderr:', process.stderr.decode('utf-8'))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logger.info("Building 'hungarian_algorithm_cpp'...")

    # run_shell_command(['chmod', '+x', f'{base_dir}/init_algo.sh'])
    run_shell_command(['sh', f'{base_dir}/init_algo.sh'])
    logger.info("Building 'hungarian_algorithm_cpp' completed.")


build_algorithm()
