from setuptools import setup,find_packages

setup(
        name="simecy",
        version='v0.2',
        description='simple encrypt file',
        author='captainfffsama',
        author_email='tuanzhangsama@outlook.com',
        packages=find_packages(),
        include_package_data=True,
        license='MIT License',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        install_requires=['cryptography',]
)
