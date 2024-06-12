from setuptools import setup, find_packages
  
setup(  
    name='pytech-zp',  
    version='0.1.4',  
    author='Peng Zhao',
    author_email='zhaokehan86@163.com',
    description='Python function package of technical indicators and patterns implemented by C++',
    packages=find_packages(),
    include_package_data=True,
    package_data={'pytech': ['*.pyd']},
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license=open('LICENSE').read(),
    install_requires=[
        'numpy',
        'pandas',
        'pyodbc'],
    # 其他必要信息，如 author, description, license 等  
)