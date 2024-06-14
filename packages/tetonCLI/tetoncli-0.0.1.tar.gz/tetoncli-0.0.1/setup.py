import setuptools
setuptools.setup(
    name='teton_client',
    version='0.1.0',    
    description='a client for wrapping scripts used internally',
    url='',
    author='Emil Koch Ringtved',
    author_email='emil@teton.ai',
        
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    install_requires=['mpi4py>=2.0',
                      'numpy',                     
                      ],
    entry_point = {'console_scripts': ['teton=tetonCLI.cli:main'],}
)