#By Python_Fucker On 2024/6/11
import subprocess
import sys
import pkg_resources
def whereis():
    return __import__(sys.argv[1]).__path__[0]
def fuck():
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', sys.argv[1], '-y'])
def befuck():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', sys.argv[1]])
def so():
    results = []
    for pkg in pkg_resources.working_set:
        if sys.argv[1].lower() in pkg.project_name.lower() or sys.argv[1].lower() in pkg.version.lower():
            results.append(f"{pkg.project_name}=={pkg.version}")
    return results
def all():
    installed_packages = list(pkg_resources.working_set)
    results = []
    for package in installed_packages:
        results.append(f"{package.project_name}=={package.version}")
    return results
