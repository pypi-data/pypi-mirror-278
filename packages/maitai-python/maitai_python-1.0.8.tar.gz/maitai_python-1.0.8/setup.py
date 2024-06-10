# setup.py

from setuptools import setup, find_packages
setup(
    name='maitai-python',
    version='1.0.8',
    packages=find_packages(exclude=("maitai_back", "maitai_back.*")),
    install_requires=[
        'requests',
        'openai',
        'betterproto',
        'httpx',
        'aiohttp',
        'setuptools',
        'websocket-client',
    ],
    # Optional metadata
    author='Maitai',
    author_email='support@trymaitai.ai',
    description='Maitai SDK for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://docs.trymaitai.ai',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
