from setuptools import setup, find_packages


def read_readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='PistolMagazine',
    version='0.3.0',
    description='A data mocking tool designed to help you generate realistic data for testing and development purposes.',
    author='Ealyn',
    author_email='miyuk1@126.com',
    packages=find_packages(),
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Faker==25.1.0',
        'pytest==6.2.4'
    ],
)
