from setuptools import setup

setup(
    name='home_bank_converter',
    version='0.2.0',
    packages=['home_bank_converter'],
    url='https://github.com/FabianReister/home_bank_converter',
    license='GPL-3.0',
    author='Fabian Reister',
    author_email='',
    description='Converter for various online banking transaction files to be able to import them to HomeBank (http://homebank.free.fr)',
    install_requires=[
        "datetime",
        "typing",
    ]
)
