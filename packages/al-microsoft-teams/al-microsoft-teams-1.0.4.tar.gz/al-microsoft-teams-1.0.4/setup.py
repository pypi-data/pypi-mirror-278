from setuptools import setup, find_packages

setup(
    name='al-microsoft-teams',
    version='1.0.4',
    packages=['al-microsoft-teams'],
    install_requires=[
        'requests',
        'msal',
        'alsacommonutils'
    ],
    author='Rashelle Woudberg',
    author_email='rashelle@al.co.za',
    description='A Python wrapper to send messages to Microsoft Teams.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AutumnLeafIT/al-aws-notification-modules',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)