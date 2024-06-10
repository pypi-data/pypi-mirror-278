from setuptools import find_packages, setup

setup(
    package_dir={"oasysnow": "oasysnow"},
    packages=find_packages(
        where=".",
        include=[
            "*",
        ],
        exclude=["tests", "tests.*"],
    ),
    package_data={
        "": ["*.npz"],
    },
    include_package_data=True,
)
