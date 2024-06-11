import subprocess
import sys
import pkg_resources
def where(package_name):
    try:
        package = __import__(package_name)
        return package.__path__[0]
    except ImportError:
        return None
        
def fuck(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', package_name, '-y'])
def befuck(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
def so(query):
    results = []
    for pkg in pkg_resources.working_set:
        if query.lower() in pkg.project_name.lower() or query.lower() in pkg.version.lower():
            results.append(f"{pkg.project_name}=={pkg.version}")
    return results
def all():
    installed_packages = list(pkg_resources.working_set)
    results = []
    for package in installed_packages:
        results.append(f"{package.project_name}=={package.version}")
    return results
