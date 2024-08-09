from setuptools import setup, find_packages

setup(
    name='manchu_morphology_analyzer',              # Required: Name of the package
    version='1.0',                 # Required: Package version
    packages=find_packages(),        # Automatically find and include all packages
    python_requires='>=3.8.5',       # Required: Specify the minimum Python version
    package_data={
        'manchu_morphology_analyzer': ['data/*.txt'],  # Include all .txt files in the data folder
    },
    include_package_data=True,      # Ensure that package_data is included
)
