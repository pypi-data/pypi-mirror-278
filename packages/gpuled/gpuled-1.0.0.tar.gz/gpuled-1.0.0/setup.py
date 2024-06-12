import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gpuled",
    version="1.0.0",
    author="OuSyouyou",
    url='https://github.com/ousyouyou/gpuled',
    author_email="s2122011@stu.musashino-u.ac.jp",
    description="use led to show GPU temp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
