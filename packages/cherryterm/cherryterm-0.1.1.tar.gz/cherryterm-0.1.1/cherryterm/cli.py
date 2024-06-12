import click
import subprocess

@click.group()
def cli():
    pass

@cli.command()
def install():
    """Install the asciinema package using pipx."""
    try:
        subprocess.run(['pipx', 'install', 'asciinema==2.4.0'], check=True)
        click.echo('asciinema has been installed.')
    except subprocess.CalledProcessError as e:
        click.echo(f'An error occurred while installing asciinema: {e}')

@cli.command()
@click.argument('draft_file')
def rec(draft_file):
    """Record a terminal session and move the resulting cast file."""
    try:
        # Construct the command for asciinema recording
        record_command = ['asciinema', 'rec', '--quiet', '--overwrite', draft_file]

        # Execute the asciinema recording command
        subprocess.run(record_command, check=True)

        # Move the draft file to the final cast file
        cast_file = draft_file.replace('.draft', '')
        subprocess.run(['mv', draft_file, cast_file], check=True)

        click.echo(f'{draft_file} has been renamed to {cast_file}.')
    except subprocess.CalledProcessError as e:
        click.echo(f'An error occurred during recording or moving the file: {e}')

if __name__ == '__main__':
    cli()