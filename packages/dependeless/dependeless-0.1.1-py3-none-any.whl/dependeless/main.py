from subprocess import run
import click

@click.command()
@click.option('--pip-path', default='pip', help='Path to pip executable')
@click.option('--pardon', default='dependeless, pip', help='Comma-separated list of package names to ignore')
def cli(pip_path, pardon):
    """
    This command will show a list of packages that have no dependents. 
    This can be useful for identifying packages that are no longer needed and can be removed.
    """

    # Show which pip is being used
    which_pip = run(['which', pip_path], capture_output=True, text=True).stdout.strip()
    click.echo(f"Using pip at {which_pip}")

    # Get a list of all installed packages
    all_packages = run([pip_path, 'list'], capture_output=True, text=True).stdout
    package_names = [line.split(' ')[0] for line in all_packages.splitlines()[2:]]
    
    # Ignore pardonned packages
    pardon = pardon.replace(' ', '').split(',')
    pardonned_not_installed = [pp for pp in pardon if pp not in package_names]
    if len(pardonned_not_installed) > 0:
        click.echo(f"\033[93mAre you sure you comma seperated the pardonned package names correctly?")
        click.echo(f"Following packages are not installed: {', '.join(pardonned_not_installed)}\033[0m")
    package_names = [package_name for package_name in package_names if package_name not in pardon]

    # Show which packages have no dependents
    click.echo(f"Scanning {len(package_names)} packages...")
    click.echo("Non-dependent packages:")
    non_dependent_packages = []
    for i, package_name in enumerate(package_names):
        package_info = run([pip_path, 'show', package_name], capture_output=True, text=True).stdout
        required_by ,= [line.split(': ')[1] for line in package_info.splitlines() if line.startswith('Required-by: ')]
        if required_by == '':
            click.echo(f"{package_name}      ")
            non_dependent_packages.append(package_name)
        click.echo(f"{i/len(package_names)*100:.2f}% \r", nl=False)
    click.echo("       ")
    
    # If all packages have dependents, we're done
    if len(non_dependent_packages) == 0:
        click.echo(f"All {len(package_names)} packages have dependents! 🎉")
        return
    
    # Generate a pip command to uninstall all non-dependent packages
    click.echo(f"To uninstall all non-dependent packages, run:")
    click.echo(f"\033[93m$ pip-autoremove -y {' '.join(non_dependent_packages)}\033[0m")
    click.echo("\033[91m\033[1mPlease review the list of packages to be uninstalled before executing!\033[0m")