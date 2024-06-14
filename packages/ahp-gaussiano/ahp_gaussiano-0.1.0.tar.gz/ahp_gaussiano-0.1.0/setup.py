from setuptools import setup, find_packages

setup(
    name="ahp_gaussiano",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    author="Bruno Melo",
    author_email="Brunomeloslv@gmail.com",
    description="Pacote para cálculo de AHP Gaussiano",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BrunoMeloSlv/ahp_gaussiano",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
