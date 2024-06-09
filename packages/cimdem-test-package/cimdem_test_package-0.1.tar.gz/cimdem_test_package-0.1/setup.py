from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line and not line.startswith("#")]

setup(
    name='cimdem_test_package',
    version='0.1',
    packages=find_packages(include=['package', 'package.*']),
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
    package_data={
        'mypackage': ['logger.yml'],
    },
    description='A short description of your package',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/mypackage',  # Replace with your repository URL if applicable
)
