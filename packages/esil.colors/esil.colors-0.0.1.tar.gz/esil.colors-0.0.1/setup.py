from setuptools import setup, find_packages

setup(
    name='esil.colors',
    version='0.0.1',
    author='Devin Long',
    author_email='long.sc@qq.com',
    description='colors map for python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Devin-Long-7/esil',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,# 允许包含在 MANIFEST.in 文件中指定的所有文件。
    package_data={
        'esil.colors': ['color_maps/*.rgb'],
        'esil.colors': ['color_maps/*.pkl'],  # 包含特定包中的 .pkl 文件
    },
    python_requires='>=3.6',
)