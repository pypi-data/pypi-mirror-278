from setuptools import setup, find_packages

setup(
    name='agentx-tools',
    version='0.5',
    packages=find_packages(),
    description='A collection of tools for Large Language Model Agents',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/Tylerbryy/agentx',
    author='Tyler Gibbs',
    author_email='tylergibbs048@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'numpy==1.26.4',
        'langchain-core>=0.1.52,<0.2.0',  
        'crewai-tools>=0.2.0,<=0.2.6',
        'langchain-community>=0.0.38,<0.1.0',  
        'langchain>=0.1.4,<0.2.0',  
    ],
)
