from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    ld = f.read()

setup(
    name='BrawlPlex',
    version='24.6.4',
    author='BrawlAPI Dev',
    author_email='brawlapi.dev@gmail.com',
    description='A package for Brawl Stars API',
    long_description=ld,
    long_description_content_type="text/markdown",
    url='https://github.com/yourusername/BrawlPlex',  # Replace with your GitHub repository URL
    packages=find_packages("src"),
    install_requires=[
        'requests>=2.32.3',  # Example dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.12',
    include_package_data=True,
)