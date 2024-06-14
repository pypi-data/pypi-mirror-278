from setuptools import setup, find_packages

setup(
    name='theosocr',
    version='1.6',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='theostekno',
    author_email='theostekno@gmail.com',
    description='A simple Theos library using Theos API',
    url='https://github.com/emretecno/theosocr',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
