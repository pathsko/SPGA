from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SPGA",  
    version="0.1.1", 
    author="Pedro Velasco",
    author_email="p2003ve@gmail.com",
    description="Una librería flexible para implementar algoritmos genéticos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/pathsko/SGA",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "matplotlib>=3.0.0",
        "Pillow>=8.0.0",
        "IPython>=7.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "ipython>=7.0",
            'sphinx',
            'sphinx-rtd-theme',
            'numpydoc',  # Recomendado para documentación científica
            'myst-parser',  # Para soportar Markdown
        ],
    },
)