from setuptools import setup, find_packages

setup(
      name='edugenome',
      version='0.0.1',
      description='It consists of three genetic algorithms that are simply \
          implemented with Python code for genetic algorithm training: \
              creating a number sum of 20, creating (4, 4) images, and \
                  implementing linear regression.',
      author='majestyblue',
      author_email = 'majestyblue88@gmail.com',
      url = 'https://github.com/majestyblue/edugenome',
      install_requires=['numpy'],
      packages=find_packages(exclude=[]),
      keywords=['education', 'genome', 'genetic algorithm'],
      python_requires='>=3.6',
      package_data={},
      zip_safe=False
)