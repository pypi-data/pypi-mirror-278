import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="textemotion_ai",
    version="0.0.1",
    author="spcnkonno",
    author_email="nkonno@sciencepark.co.jp",
    description="make a pypi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spcnkonno/textemotion_ai",
    project_urls={
        "Bug Tracker": "https://github.com/spcnkonno/textemotion_ai",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"":"src"},
    py_modules=['textemotion_ai'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.10",
    entry_points = {
        'console_scripts': [
            'textemotion_ai = textemotion_ai:main'
        ]
    },
)