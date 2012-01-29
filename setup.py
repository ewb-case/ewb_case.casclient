from setuptools import setup, find_packages
import os

version = '0.1.1'

setup(name='ewb_case.casclient',
      version=version,
      description="Provides CAS authentication for EWB Case website.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Matt Bierner',
      author_email='mattbierner@gmail.com',
      url='https://github.com/mattbierner/ewb_case.casclient',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ewb_case', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'anz.casclient',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
