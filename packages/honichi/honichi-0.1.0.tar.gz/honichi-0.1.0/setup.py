import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="honichi",
    version="0.1.0",
    author="ouekii",
    author_email="s2122010@stu.musashino-u.ac.jp",
    description="Show the number of tourists coming to Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HaiBunn/honichi/blob/main/README.md",
    project_urls={
        "Bug Tracker": "https://github.com/HaiBunn/honichi",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'honichi = honichi:main'
        ]
    },
)
