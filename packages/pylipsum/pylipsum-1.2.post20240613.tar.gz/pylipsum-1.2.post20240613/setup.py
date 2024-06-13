from setuptools import setup
with open("README.md", "r") as fh:
	long_description = fh.read()
setup(name='pylipsum',
      version='1.2',
      long_description = long_description,
      long_description_content_type='text/markdown',
      description='Lorem ipsum as py library (from lipsum.com)',
      packages=['pylipsum'],
      author_email='diassuikimbek@aol.com',
      install_requires=['beautifulsoup4', 'requests'],
      url = 'https://github.com/itsnaks/pylipsum',
      license = "Apache 2.0",
      zip_safe=False)
