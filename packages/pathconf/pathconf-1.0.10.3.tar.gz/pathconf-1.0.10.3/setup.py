from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import runpy
import sys

# Read the contents of your README file
with open('README.md') as f:
    long_description = f.read()


class CustomInstallCommand(install):
    """Customized setuptools install command - runs a post-install script."""
    def run(self):
        install.run(self)
        self.execute(self._post_install, (), msg="Running post install task")

    def _post_install(self):
        script_path = os.path.join(os.path.dirname(__file__),
                                   'post_install.py')
        if os.path.isfile(script_path):
            try:
                runpy.run_path(script_path)
            except Exception as e:
                print(f"Error running post-install script: {e}",
                      file=sys.stderr)
        else:
            print(f"Post-install script not found: {script_path}",
                  file=sys.stderr)


setup(
    name='pathconf',
    version='1.0.10.3',  # Back to manual versioning
    packages=find_packages(),
    description='Uses os.walk to find and catalogue a given file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sam Kirby',
    author_email='sam.kirby@gagamuller.com',
    install_requires=[
        # Any dependencies you have, e.g., 'requests', 'numpy', etc.
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',
    cmdclass={
        'install': CustomInstallCommand,
    },
)
