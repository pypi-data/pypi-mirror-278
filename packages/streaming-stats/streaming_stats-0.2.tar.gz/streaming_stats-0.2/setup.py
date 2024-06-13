from setuptools import setup

with open(file="README.md", mode="r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='streaming_stats',
    version='0.2',
    author="Aditya Raj",
    author_email="adityaraj867604@gmail.com",
    description='Statistics calculator of a list in O(1) space complexity',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ed21b006/RunningStats',  # Adjust as necessary
    py_modules=['running_stats'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)