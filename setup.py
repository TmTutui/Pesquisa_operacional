# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(name='Problema_da_Gasolina',
      version='0.0.1',
      description='Resoluação de problemas de programação linear para a disciplina de Pesquisa Operacional',
      url='https://github.com/TmTutui/Pesquisa_operacional',
      author='Geraldo Sousa, Tulio Tutui',
      author_email='geraldo.msousaj@gmail.com, tulio.tutui@gmail.com',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          "pulp"
          ],
      zip_safe=False)
