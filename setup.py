from distutils.core import setup


setup(
    name='django-phonefields',
    version='1.3',
    author='Maxim Oransky',
    author_email='maxim.oransky@gmail.com',
    url='https://github.com/shantilabs/django-phonefields',
    packages=[
        'phonefields'
    ],
    package_data={
        'phonefields': ['locale/ru/LC_MESSAGES/*'],
    },
)
