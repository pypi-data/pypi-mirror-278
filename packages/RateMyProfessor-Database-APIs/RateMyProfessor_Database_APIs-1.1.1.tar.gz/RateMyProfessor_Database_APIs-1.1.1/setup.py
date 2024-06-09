from setuptools import setup, find_packages

setup(
    name = 'RateMyProfessor_Database_APIs',
    version = '1.1.1',
    packages=find_packages(),
    install_requires = [
        'requests',
        'tqdm',
        'lxml'
    ],

    include_package_data=True,
    description="RateMyProfessor.com database scrapper.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Prakhar Bhartiya",
    # author_email="your.email@example.com",
    # url="https://github.com/yourusername/your_project",
    classifiers=[
        'Programming Language :: Python :: 3',
        # 'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # python_requires='>=3.6',
)