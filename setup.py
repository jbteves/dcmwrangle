from setuptools import setup, find_packages
setup(name='dicomorg',
      version='0.1',
      description='helps organize and convert MRI dicoms',
      author='Joshua B. Teves',
      author_email='jbtevespro@gmail.com',
      python_requires='>=3.6',
      install_requires='pydicom',
      entry_points={'console_scripts':
          ['dicomorg=dicomorg.workflows:main']}
      )
