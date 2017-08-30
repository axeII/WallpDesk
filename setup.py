from setuptools import setup

OPTIONS = { 'dist_dir' : 'dist',
            'site_packages' : False,
            'argv_emulation': True, # argv_emulation interferes with gui apps
            'plist': {
                    'LSUIElement': True,
                },
            #'iconfile' : 'resources/WallpDesk.icns',
            'alias': False }

setup(name='WallpDesk',
      app=['WallpDesk/__main__.py'],
      options={'py2app': OPTIONS},
      version='0.1',
      description='A simple os x menu bar application setting wallpapers',
      author='Ales Lerch',
      author_email='secret',
      url='github.com/L3rchal/Wallpdesk',
      python_requires=">=3.5",
      test_suite="tests",
      packages=['WallpDesk'],
     )
