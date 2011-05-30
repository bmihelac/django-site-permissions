from setuptools import setup, find_packages
import os


VERSION = __import__("site_permissions").__version__

setup(
    name="django-site-permissions",
    description="Per site permissions in django",
    long_description=open(os.path.join(os.path.dirname(__file__), 
        'README.rst')).read(),
    version=VERSION,
    author="Bojan Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://bmihelac@github.com/bmihelac/django-site-permissions.git",
    install_requires=[
        'django-guardian',
        ],
    packages=find_packages(exclude=["example", "example.*"]),
)

