from setuptools import setup, find_packages

setup(
    name='theosocr',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='theostekno',
    author_email='theostekno@gmail.com',
    description='A simple Theos library using Theos API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/emretecno/theosocr',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
