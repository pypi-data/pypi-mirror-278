from setuptools import setup, find_packages

setup(
    name='fastboot_log_parser',
    version='0.1.1',
    setup_requires = ['setuptools_scm'],
    author='Macpaul Lin',
    author_email='macpaul.lin@mediatek.com',
    description='A parser for Fastboot logs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/mediatek/aiot/bsp/fastboot-log-parser',
    packages=find_packages(),
    py_modules=['fastboot_log_parser'],
    install_requires=[
        'simplejson',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=False,
)