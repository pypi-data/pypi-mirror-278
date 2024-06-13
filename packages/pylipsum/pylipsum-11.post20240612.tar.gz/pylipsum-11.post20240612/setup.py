from setuptools import setup
with open("readme.md", "r") as fh:
	long_description = fh.read()
setup(name='pylipsum',
      version='1',
      description='Lorem lipsum as py library',
      packages=['pylipsum'],
      author_email='diassuikimbek@aol.com',
      zip_safe=False)
