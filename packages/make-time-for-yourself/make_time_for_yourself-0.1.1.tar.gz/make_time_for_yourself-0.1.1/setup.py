import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="make_time_for_yourself",
    version="0.1.1",
    author="takisawa kazuma",
    author_email="ktakisawa@sciencepark.co.jp",
    description="A simple package to generate random numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ktakisawa/make_time_for_yourself",
   
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['make_time_for_yourself'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'make_time_for_yourself = make_time_for_yourself:main'
        ]
    },
)
