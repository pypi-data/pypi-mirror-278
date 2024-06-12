import setuptools


with open("epicdb/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='epicdb',
    version='1.4',
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas'
    ],
    url='https://github.com/hybridlca/epicdb',
    license='GNU General Public License v3.0',
    author='André Stephan',
    author_email='stephan.andre@gmail.com',
    description='A python package to use the Environmental Performance in Construction (EPiC) Database as a Pandas Dataframe',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
    '':['db/*.feather']
    }
)
