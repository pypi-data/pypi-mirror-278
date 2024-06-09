from setuptools import setup, find_packages

with open("README.md", "r") as file:
	readme = file.read()

setup(
  name='hamsterpy',
  version='0.0.1',
  author='KirbyRedius',
  description='HamsterPy is created for auto-farming coins in Hamster Kombat (Telegram game)',
  long_description=readme,
  long_description_content_type='text/markdown',
  url="https://github.com/KirbyRedius/HamsterPy",
  packages=find_packages(),
  install_requires=['requests>=2.32.3'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords=[
	"Hamster",
	"HamsterKombat",
	"Hamster Kombat",
	"api.hamsterkombat.io"
  ],
  project_urls={
    'GitHub': 'https://github.com/KirbyRedius/HamsterPy'
  },
  python_requires='>=3.6'
)