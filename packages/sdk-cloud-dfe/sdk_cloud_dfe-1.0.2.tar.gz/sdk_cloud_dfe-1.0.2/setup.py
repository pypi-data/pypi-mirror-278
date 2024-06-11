from setuptools import setup, find_packages

setup(
    name="sdk_cloud_dfe",
    version="1.0.2",
    author="Integra Notas",
    author_email="comercial@cloud-dfe.com.br",
    description="SDK para comunicar com API Integra Notas.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
    "requests",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.6",
)
