from setuptools import setup, find_packages

setup(
    name='platform_users',
    version='1.0.4',
    author='Vishwajeet Kale',
    author_email='vishwajeet.kale.v2stech@gmail.com',
    description='This is an app for managing users in a SaaS product named Platform.',
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    license='MIT',
    include_package_data=True,  # Include package data specified in MANIFEST.in
    install_requires=[
        'Django>=3.1',
        'djangorestframework>=3.11.1'
        # Add other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
