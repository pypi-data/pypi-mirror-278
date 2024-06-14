import os
import sys
import subprocess
import click

@click.command()
@click.option('--zip', 'zip_file', required=True, help='Path to the zip file.')
@click.option('--pass', 'password_list', required=True, help='Path to the password list file.')
@click.option('--unzip', is_flag=True, help='Automatically unzip after finding the password.')
@click.option('--save', 'save_file', help='Save the found password to a file.')
@click.option('--silent', is_flag=True, help='Silent mode, only display the found password.')
def cli(zip_file, password_list, unzip, save_file, silent):
    if not sys.platform.startswith('linux'):
        print("This tool only works on Linux.")
        sys.exit(1)

    script_path = os.path.join(os.path.dirname(__file__), 'ziplip.sh')

    command = [script_path, '--zip', zip_file, '--pass', password_list]
    
    if unzip:
        command.append('--unzip')
    if save_file:
        command.extend(['--save', save_file])
    if silent:
        command.append('--silent')

    subprocess.run(command)

if __name__ == "__main__":
    cli()
