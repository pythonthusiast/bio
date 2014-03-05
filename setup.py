from setuptools import setup

setup(name='Bio',
      version='1.0',
      description="Let's you have a fully interactive Curriculum Vitae",
      author='Eko S. Wibowo',
      author_email='swdev.bali@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=
      [
        'Flask==0.10.1',
        'Flask-SQLAlchemy==1.0',
        'Flask-Login==0.2.7',
        'Flask-WTF==0.9.2',
        'alembic'
      ],
     )
