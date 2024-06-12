import setuptools

PACKAGE_NAME = "contact-profile-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.23',  # https://pypi.org/project/contact-profile-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles contact-profile-local Python",
    long_description="PyPI Package for Circles contact-profile-local Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "logger-local>=0.0.135",
        "database-mysql-local>=0.0.290",
        "contact-persons-local>=0.0.19",
        "language-remote>=0.0.20",
        "profile-local>=0.0.79",
        "user-context-remote>=0.0.75"
    ],
)
