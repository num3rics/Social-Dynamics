import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='social_dynamics',  
     version='0.1',
     scripts=['sd'] ,
     author="Pablo Lozano",
     author_email="pablo.lozano@uc3m.es",
     description="Model for fake reputation in a network",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/palozano/Social-Dynamics",
     packages=setuptools.find_packages(),
     classifiers=[
     ],
 )
