from setuptools import setup
with open("readme.md", "r") as fh:
	long_description = fh.read()
setup(name='pylipsum',
      version='1.0.0',
      long_description = long_description,
      long_description_content_type='text/markdown',
      description='Lorem lipsum as py library',
      packages=['pylipsum'],
      author_email='diassuikimbek@aol.com',
      zip_safe=False)
