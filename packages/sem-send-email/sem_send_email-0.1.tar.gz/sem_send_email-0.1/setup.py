from setuptools import setup, find_packages

setup(
    name='sem_send_email',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3"
    ]
)