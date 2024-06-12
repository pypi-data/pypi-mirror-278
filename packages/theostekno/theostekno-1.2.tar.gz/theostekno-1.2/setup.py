from setuptools import setup, find_packages

setup(
    name='theostekno',
    version='1.2',
    packages=find_packages(),
    author='Emre Tekno',
    author_email='theostekno@gmail.com',
    description='A simple random number generator library',
    long_description='Your long description here',
    long_description_content_type='text/markdown',
    url='https://github.com/emretecno/theos-ai',
    keywords=['random', 'number', 'generator', 'library'],
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
    python_requires='>=3.6'
)