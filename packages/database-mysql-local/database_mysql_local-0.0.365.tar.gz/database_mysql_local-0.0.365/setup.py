import setuptools

PACKAGE_NAME = "database-mysql-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/database-mysql-local
    version='0.0.365',
    author="Circles",
    author_email="info@circlez.ai",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="Database MySQL Local",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "mysql-connector-python>=8.3.0",  # https://pypi.org/project/mysql-connector-python/
        "url-remote>=0.0.97",  # https://pypi.org/project/url-remote/
        "logger-local>=0.0.145",  # https://pypi.org/project/logger-local/
        "database-infrastructure-local>=0.0.26",  # https://pypi.org/project/database-infrastructure-local/
        "language-remote>=0.0.22",  # https://pypi.org/project/language-remote/
        "sql-to-code-local>=0.0.14",  # https://pypi.org/project/sql-to-code-local/
        "python-sdk-remote>=0.0.110",
        # "sshtunnel>=0.4.0",  # https://pypi.org/project/sshtunnel/
    ]
)
