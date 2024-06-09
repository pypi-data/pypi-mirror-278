from setuptools import setup, find_packages # type: ignore

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
        name="librds", 
        version="1.95",
        author="kuba201",
        description='RDS Group Generator',
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        url="https://flerken.zapto.org:1115/kuba/librds",
        install_requires=[],
        project_urls={
            'Source': 'https://flerken.zapto.org:1115/kuba/librds',
        },
        keywords=['radiodatasystem','rds','broadcast_fm'],
        classifiers= [
            "Intended Audience :: Education",
            "Intended Audience :: Telecommunications Industry",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.10",
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: GNU General Public License (GPL)",
        ]
)