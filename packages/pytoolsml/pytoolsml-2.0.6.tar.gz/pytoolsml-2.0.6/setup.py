from distutils.core import setup

setup(
  name = 'pytoolsml',         # How you named your package folder (MyLib)
  packages = ['pytoolsml'],   # Chose the same as "name"
  version = '2.0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Machine Learning wrapper for scaled prediction',   # Give a short description about your library
  author = 'Collins',                   # Type in your name
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)