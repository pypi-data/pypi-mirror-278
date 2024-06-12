from setuptools import setup, find_packages
setup(
    name='quickQrLib',
    version='0.2.40',
    packages=find_packages(),
    install_requires = [
        'djangorestframework-simplejwt',
        'django',
        'djangorestframework',
        'cryptography',
        'boto3',
        'python-dateutil',
        'pytz',
        'requests',
        'redis',
        'django-environ'
    ],
    include_package_data=True, 
)
