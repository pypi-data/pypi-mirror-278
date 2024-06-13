import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mnara_test",
    version='0.0.1',
    author='mnara0613',
    author_email="mnara@sciencepark.co.jp",
    description="how to debut a PyPI for Chemistry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mnara0613/mnara_test",
    project_urls={
        "Bug Tracker":"https://github.com/mnara0613/mnara_test",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"":"src"},
    py_modules=['mnara_test'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.10",
    entry_points={
        'console_scripts':[
            'mnara_test = mnara_test:main'
        ]
    },


)