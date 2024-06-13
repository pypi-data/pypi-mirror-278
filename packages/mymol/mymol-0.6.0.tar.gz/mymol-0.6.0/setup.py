from setuptools import setup, find_packages

setup(
    name='mymol',
    version='0.6.0',
    author='Arthur Kwak',
    author_email='arthurmichielkwak@gmail.com',
    description='An usefull python module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tureluurtje/mymol',
    packages=find_packages(),
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
    python_requires='>=3.6',
)
