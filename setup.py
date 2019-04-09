from setuptools import setup, find_packages

setup(name="ontology-clean",
      version="0.1",
      author="Ginkgo Bioworks",
      description="Scripts for cleaning input key/values and applying ontologies",
      license="MIT",
      packages=find_packages(exclude=["tests"]),
      scripts=["scripts/oclean_unstructured.py"])
