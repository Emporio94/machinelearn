import os, subprocess, sys , importlib

def install_package(package):
    try:
        importlib.import_module(package)
        print(f"✅ {package} already installed!")
        return True
    except ImportError as e:
        print(f"⌛ {package} not installed, installing...")

    try:
        print("Installing package: ", package)
        result = subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "--no-cache", package])
        print(f"✅ {package} installed. Restart the kernel ↺")
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False
    return True

def proxy_install(package):
    result = False
    try:
        result = install_package(package)
    except Exception as e:
        print(f"Failed to install {package} with error {e}")
        result = False
    if not result:
        os.environ["http_proxy"] = "http://wwwcache.gla.ac.uk:8080"
        try:
            result = install_package(package)
            print(f"✅ {package} installed. Restart the kernel ↺")
            return True
        except Exception as e:
            print(f"Failed to install {package} with error {e}")
            result = False
        if not result:
            print(f"❌ Hmm, could not install {package} even with the proxy")
        