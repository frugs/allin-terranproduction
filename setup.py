import setuptools

VERSION = "0.0.3"

setuptools.setup(
    name="terranproduction",
    packages=setuptools.find_packages(),
    package_data={"terranproduction": ["templates/*", "static/styles/*", "static/images/*"]},
    version=VERSION,
    description="SC2 Replay Analyser which visualises a player's Terran Production Efficiency",
    author="Hugo Wainwright",
    author_email="wainwrighthugo@gmail.com",
    url="https://github.com/frugs/allin-terranproduction",
    keywords=["sc2", "replay", "sc2reader"],
    classifiers=[],
    install_requires=[
        "techlabreactor", "requests>=2.19.1", "requests-toolbelt>=0.8.0", "pyrebase", "flask", "google-cloud-datastore"
    ],
)
