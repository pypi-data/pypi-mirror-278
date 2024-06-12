from setuptools import setup, find_packages
VERSION = '0.0.1'
DESCRIPTION = 'ESSL Payments Aggregator'
LONG_DESCRIPTION = 'Internal helper package for ESSL online payment'
setup(
    name='espy_pay',
    version='1.0.5',
    author='Femi Adigun',
    author_email='femi.adigun@myeverlasting.net',
    description='Payment services aggregator for ESSL',
    packages=find_packages(),
    install_requires=[
        'bcrypt==4.1.2',
        'pytest==8.1.1',
        'pydantic==2.7.1',
        'sqlalchemy==2.0.29',
        'PyYAML ==6.0.1',
        'requests==2.26.0',
        'python-dotenv==1.0.1',
        'stripe==9.10.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['payment, essl, aggregator, paystack, stripe, interswitch, square, flutterwave, payant'],
)