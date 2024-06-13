import setuptools

PACKAGE_NAME = "contact-user-external-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.9',  # https://pypi.org/project/contact-user-external-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles contact-user-external-local Python",
    long_description="PyPI Package for Circles contact-user-external-local Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'database_mysql_local>=0.0.290',
        'logger-local>=0.0.135',
        'user-context-remote>=0.0.77',
        'user-external-local>=0.0.42',
        'internet-domain-local>=0.0.18'
    ],
)
