from setuptools import setup, find_packages

setup(
    name='beeai',
    version='1.0.1',
    description='Python SDK for Bee API',
    author='Ethan Sutin',
    author_email='e@bee.computer',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-socketio',
        'websocket-client',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)