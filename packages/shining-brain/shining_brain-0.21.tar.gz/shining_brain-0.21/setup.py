from setuptools import setup, find_packages
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='shining-brain',
    version='0.21',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    author='Evan Knox Thomas',
    author_email='evanknoxthomas@gmail.com',
    package_dir={'': 'src'},
    install_requires=['pandas', 'sqlalchemy', 'PyYAML', 'openpyxl', 'mysql-connector-python', 'pathlib']
)
