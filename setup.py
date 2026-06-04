from setuptools import setup, find_packages

setup(
    name="zyp-engine",
    version="0.1.0-alpha",
    description="ZuluYokohama Protocol Edge Execution Engine",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "zyp=zyp_cli.main:main",
        ],
    },
)
