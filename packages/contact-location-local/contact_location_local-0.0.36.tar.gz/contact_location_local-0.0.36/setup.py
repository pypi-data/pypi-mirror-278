import setuptools

PACKAGE_NAME = "contact-location-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.36',  # https://pypi.org/project/contact-location-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles contact-location-local Python",
    long_description="PyPI Package for Circles contact-location-local Python",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/contact-location-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pycountry>=23.12.11',
        'phonenumbers>=8.13.30',
        'database-mysql-local>=0.0.342',
        'group-local>=0.0.26',
        'language-remote>=0.0.20',
        'location-local>=0.0.119',
        'logger-local>=0.0.135',
        'user-context-remote>=0.0.57',
        'contact-group-local>=0.0.52',
    ],
)
