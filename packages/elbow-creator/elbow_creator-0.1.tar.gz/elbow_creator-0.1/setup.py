# setup.py
from setuptools import setup, find_packages

setup(
    name='elbow_creator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'bpy',
        'mathutils',
        'math'
    ],
    entry_points={
        'console_scripts': [
            'create_elbow=elbow_creator.elbow_creator:create_elbow',
        ],
    },
    author='Vamshi Gangadhar',
    author_email='vamshi.gangadhar365@gmail.com',
    description='A package to create an elbow mesh in Blender',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VamshiGangadhar/elbow_creator',
)
