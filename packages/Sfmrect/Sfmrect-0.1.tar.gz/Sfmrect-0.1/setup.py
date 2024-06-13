from setuptools import setup, find_packages
from setuptools.command.install import install
import shutil
import os

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        # Get the path to the .dll file in the package
        dll_src = os.path.join(self.install_lib, 'Sfmrect', 'opencv_world320.dll')
        # Define the destination path for the .dll file
        python_dir = os.path.dirname(os.path.dirname(os.__file__))
        dll_dst = os.path.join(python_dir, 'opencv_world320.dll')
        # Copy the .dll file to the destination path
        shutil.copyfile(dll_src, dll_dst)

setup(
    name='Sfmrect',
    version='0.1',
    packages=find_packages(),
    package_data={
        'Sfmrect': ['sfmrect.pyd', 'opencv_world320.dll'],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)
