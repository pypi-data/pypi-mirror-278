from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='ease_mailer',
    version='1.2',
    packages=['ease_mailer'],
    url='',
    license='MIT',
    author='Tech Smit',
    author_email='techsmitdevloper@gmail.com',
    description='ease_mailer is the easiest way for email sending.',
    keywords=['Email Sending', 'Send Mail', 'Easy Email Sender', 'Send Multiple Mail'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
