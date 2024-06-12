from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='radiometerAPI',
    version='1.0.8',
    author='aburgart02',
    author_email='',
    description='API for radiometer',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='http://www.example.com/',
    packages=find_packages(),
    install_requires=['requests>=2.27.1', 'aiohttp>=3.9.2'],
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
    keywords='radiometer',
    project_urls={
        "Documentation": "https://github.com/aburgart02/radiometer-api",
        "Source Code": "https://github.com/aburgart02/radiometer-api",
        "Bug Tracker": "https://github.com/aburgart02/radiometer-api"
    },
    python_requires='>=3.10'
)
