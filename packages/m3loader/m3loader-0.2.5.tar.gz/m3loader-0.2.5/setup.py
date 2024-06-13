from setuptools import setup, find_packages

setup(
    name='m3loader',
    version='0.2.5',
    description='A tool to download and merge M3U8 segments into an MP4 file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Darsh',
    author_email='darsh.564742@gmail.com',
    url='https://github.com/d4r5hE/m3loader',
    license='MIT',
    packages=find_packages(include=['m3loader', 'm3loader.*']),
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'tqdm',
        'ffmpeg-python'
    ],
    entry_points={
        'console_scripts': [
            'm3loader=m3loader.dloader:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
)
