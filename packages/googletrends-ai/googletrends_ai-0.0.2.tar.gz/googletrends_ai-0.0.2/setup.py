import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="googletrends_ai",
    version="0.0.2",
    author="spcnkonno",
    author_email="nkonno@sciencepark.co.jp",
    description="Please run pip install pytrends pandas matplotlib beforehand",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spcnkonno/googletrends_ai",
    project_urls={
        "Bug Tracker": "https://github.com/spcnkonno/googletrends_ai",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    py_modules=['googletrends_ai'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.10",
    entry_points = {
        'console_scripts': [
            'googletrends_ai = googletrends_ai:main'
        ]
    },
)