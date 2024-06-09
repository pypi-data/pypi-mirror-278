from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="assistente_willuka",
    version="0.0.1",
    author="William Sousa",
    author_email="william.sousarj@gmail.com",
    description="Assistente para Realização de Tarefas no Windows",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/William-Almeida-Sousa/assistente-willuka.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)