import setuptools

from version_text import text

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()
    for version, description in text:
        long_description += f"\n- {version} {description}"

with open("requirements.txt", "r", encoding='utf8') as fh:
    requires = fh.read().replace('==', '>=')

setuptools.setup(
    name="AngularCurdGen",
    version=text[-1][0],
    author="Steven Wang",
    author_email="brightstar8284@icloud.com",
    description="Use for generate angular curd codes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StevenLianaL/angular_curd_gen",
    # packages=setuptools.find_packages(exclude=["tests*"]),
    # install_requires=requires,
    package_data={
        'angular_curd_gen': ['templates/**/*.jinja'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)
