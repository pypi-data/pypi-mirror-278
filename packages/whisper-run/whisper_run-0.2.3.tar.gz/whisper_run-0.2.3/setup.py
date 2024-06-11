from setuptools import find_packages, setup

def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

def load_requirements(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


setup(
    name='whisper_run',
    version='0.2.3',
    author='Görkem Karamolla',
    author_email='gorkemkaramolla@gmail.com',
    description='Whisper with speaker diarization',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_repository',
    package_dir={'': 'src'},  
    packages=find_packages(where='src'), 
    install_requires=load_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'whisper_run=whisper_run.__main__:main'
        ]
    }
)
