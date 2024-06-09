import os
import platform
import subprocess
import sys

def get_architecture():
    arch = platform.machine().lower()
    system = platform.system().lower()

    if arch == 'x86_64':
        if system == 'linux':
            return 'linux-amd64'
        elif system == 'windows':
            return 'win-i686.exe'
    elif arch == 'i686' or arch == 'x86':
        if system == 'windows':
            return 'win-i686.exe'
    elif arch == 'aarch64':
        if system == 'linux':
            return 'linux-arm64'
    elif arch == 'loongarch64':
        if system == 'linux':
            return 'linux-loongarch64'
    elif arch == 'riscv64':
        if system == 'linux':
            return 'linux-riscv64'
    elif arch.startswith('arm') and system == 'linux':
        return 'linux-armbi'
    
    return 'unknown'

def main():
    print("dfss python tool, version: v1.7.0")
    binary_arch = get_architecture()
    
    if binary_arch == 'unknown':
        arch = platform.machine().lower()
        system = platform.system().lower()
        print("Unsupported architecture or operating system")
        print("arch:" + arch)
        print("system:" + system)
        return
    print("Find architecture: " + binary_arch)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    binary_name = 'dfss-cpp-' + binary_arch
    binary_path = os.path.join(script_dir, 'output', binary_name)
    if not os.path.isfile(binary_path):
        print("Binary file for architecture " + binary_arch + " not found at " + binary_path)
        return
    args = sys.argv[1:]
    try:
        if platform.system().lower() == 'windows':
            ret = subprocess.run([binary_path] + args, check=True, shell=True)
        else:
            ret = subprocess.run([binary_path] + args, check=True)
        print("Binary for architecture " + binary_arch + " executed successfully, ret: " + str(ret))
    except subprocess.CalledProcessError as e:
        print("Failed to execute binary for architecture " + binary_arch + " : " + str(e))

if __name__ == '__main__':
    main()