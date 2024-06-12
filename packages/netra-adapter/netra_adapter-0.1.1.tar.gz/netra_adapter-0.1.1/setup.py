from setuptools import setup, find_packages

setup(
    name='netra_adapter',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'psutil'
    ],
    author='Harsh Lad',
    author_email='harsh.lad@netralabs.ai',
    description='A package for managing LoRA adapters in language models ideal for hotswapping',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Harsh-Lad/netra_adapter/',  # Update with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
