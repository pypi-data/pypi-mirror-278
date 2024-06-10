from setuptools import setup, find_packages

setup(
    name="vnai",
    version="0.1.1",
    author="Vnstock HQ",
    author_email="support@vnstock.site",
    description=":))",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["requests", "cryptography"],
    package_data={"vnai": ["*.so"]},
    extras_require={"dev": ["pytest", "pytest-cov"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
