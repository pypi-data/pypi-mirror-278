from setuptools import setup, find_packages

setup(
    name='givemehelp',
    version='0.25',
    packages=find_packages(),
    install_requires=[
        'openai==0.28',
        'boto3'
    ], 
    entry_points={
        "console_scripts":[
            "givemehelp = givemehelp:retreiveSecretKey",
        ],
    },
)
