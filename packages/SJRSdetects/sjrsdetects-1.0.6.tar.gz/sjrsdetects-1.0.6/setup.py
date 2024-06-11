import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SJRSdetects",
    version="1.0.6",
    author="Stevenjoelrs",
    author_email="Stevenjramossalazar@gmail.com",
    description="Detecta movimiento en fotos, video y camara",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Stevenjoelrs/SJRSdetects",
    project_urls={
        "Bug Tracker": "https://github.com/Stevenjoelrs/SJRSdetect/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)