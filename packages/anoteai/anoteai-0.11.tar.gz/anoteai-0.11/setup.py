from setuptools import setup, find_packages

# Function to read the requirements.txt file
def read_requirements():
    with open('/Users/natanvidra/Workspace/Anote-Product/server/requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='anoteai',
    version='0.11',
    packages=find_packages(),
    install_requires=read_requirements(),
    description='An SDK for interacting with the Anote API',
    author='Natan Vidra',
    author_email='nvidra@anote.ai',
    url='https://github.com/nv78/Anote',
    license='MIT',
)