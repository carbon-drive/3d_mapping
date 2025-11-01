from setuptools import setup, find_packages

setup(
    name="3d_mapping",
    version="0.1.0",
    description="3D model generation from images using Meta's MapAnything",
    author="carbon-drive",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "werkzeug>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
)
