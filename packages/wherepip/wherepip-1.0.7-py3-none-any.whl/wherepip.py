#By Python_Fucker On 2024/6/11
import subprocess
import sys
import pkg_resources
def whereis(s):
    if s==None: 
     s=sys.argv[1]
    return __import__(s).__path__[0]
def fuck(s):
    if s==None: 
     s=sys.argv[1]
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', s, '-y'])
def befuck():
    if s==None: 
     s=sys.argv[1]
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', s])
def so(s):
    if s==None: 
     s=sys.argv[1]
    results = []
    for pkg in pkg_resources.working_set:
        if s.lower() in pkg.project_name.lower() or s.lower() in pkg.version.lower():
            results.append(f"{pkg.project_name}=={pkg.version}")
    return results
def all():
    installed_packages = list(pkg_resources.working_set)
    results = []
    for package in installed_packages:
        results.append(f"{package.project_name}=={package.version}")
    return results
