from setuptools import setup, find_packages
import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(name="deplyai",
    version='0.2.3',
    description="Python SDK for DeplyAI's integrated AI agent platform.",
    setup_requires=["wheel"],
    license="BSD-3-Clause",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=install_requires
)