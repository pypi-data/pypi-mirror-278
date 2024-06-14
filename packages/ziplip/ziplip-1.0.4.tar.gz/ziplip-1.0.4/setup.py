import os
from setuptools import setup, find_packages

def post_install():
    script_path = os.path.join(os.path.dirname(__file__), 'ziplip', 'ziplip.sh')
    os.chmod(script_path, 0o755)

setup(
    name='ziplip',
    version='1.0.4',
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='A tool for finding passwords for encrypted zip files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ByteBreach/ziplips',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords='ziplip, Fidal, zip, brute force, password recovery, zipfile, encryption, security',
    install_requires=[
        'click',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ziplip=ziplip.cli:cli',
        ],
    },
    package_data={
        'ziplip': ['ziplip.sh'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/ByteBreach/ziplips/issues',
        'Source': 'https://github.com/ByteBreach/ziplips',
    },
    license='MIT',
)

post_install()
