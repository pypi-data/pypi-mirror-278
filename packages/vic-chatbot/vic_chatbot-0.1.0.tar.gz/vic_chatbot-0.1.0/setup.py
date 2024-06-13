from setuptools import setup, find_packages

setup(
    name='vic_chatbot',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A simple chatbot library with a Flask web interface',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ernald Victa',
    author_email='chuasweet11@gmail.com',
    url='https://github.com/Evasas12/chatbotlib',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'Flask>=2.0',
        'experta>=1.9',
        'scikit-learn>=0.24',
    ],
)
