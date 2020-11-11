import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

opt_pkgs = ["gdspy", "Shapely", "matplotlib", "cycler"]

setuptools.setup(
    name="nextnanopy",
    version="0.1.0a3",
    author="nextnano GmbH",
    author_email="python@nextnano.com",
    license='BSD-3-Clause',
    description="Useful tools to interface the nextnano software (https://www.nextnano.com/)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="nextnano",
    url="https://github.com/**",
    # packages=setuptools.find_packages(),
    packages=setuptools.find_packages(exclude=["tests"]),
    # packages=["nextnanopy"],
    # package_dir={"nextnanopy": "nextnanopy"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
    python_requires='>=3.8',
    install_requires=["numpy"],
)
