import os
import sys
import subprocess
from typing import List

LOCK_FILE = 'nopip.lock'


class Install:
    def install_module(self, module: str):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
            self._update_lock_file(module)
        except subprocess.CalledProcessError as e:
            print(f"Error: Could not install module '{module}'.")
            raise e

    def install_modules(self, modules: List[str]):
        for module in modules:
            self.install_module(module)

    def from_requirements(self, requirements_path: str):
        with open(requirements_path, 'r') as f:
            for line in f:
                self.install_module(line.strip())

    def _update_lock_file(self, module: str):
        if '==' not in module:
            print(f"Warning: '{module}' installed without specifying the version, lock file not updated.")
            return

        lock_data = {}
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE, 'r') as f:
                for line in f:
                    name, version = line.strip().split('==')
                    lock_data[name] = version

        module_name, module_version = module.split('==')
        lock_data[module_name] = module_version

        with open(LOCK_FILE, 'w') as f:
            for name, version in lock_data.items():
                f.write(f"{name}=={version}\n")

    def install_from_lock_file(self):
        if not os.path.exists(LOCK_FILE):
            print(f"Error: Lock file '{LOCK_FILE}' not found.")
            return

        self.from_requirements(LOCK_FILE)

    def install(self, module: str, use_lock_file=True):
        if use_lock_file:
            self.install_from_lock_file()
        else:
            self.install_module(module)


install = Install()
__all__ = ['install']
