from setuptools import setup, find_packages

setup(
    name='project_parcel',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'project_parcel': ['dist/parcel_test.tar.gz']},
    install_requires=[
        # Add dependencies here.
    ],
)