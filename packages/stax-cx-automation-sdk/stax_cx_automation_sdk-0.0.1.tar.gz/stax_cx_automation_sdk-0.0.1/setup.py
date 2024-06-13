from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='stax_cx_automation_sdk',
    version='0.0.1',
    url='https://bitbucket.org/staxai/cx-automation-sdk',
    author='Stax.ai, Inc. <https://stax.ai>',
    author_email='naru@stax.ai',
    description='Stax.ai CX Automation SDK',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    license='Proprietary',
    python_requires='>=3.6',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['retry_requests', 'functions_framework']
)