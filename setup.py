from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jasper_embed",
    version="0.2.0",
    description="Embed JasperReports Server outputs inside ERPNext/Frappe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Neotec",
    packages=find_packages(include=["jasper_embed", "jasper_embed.*"]),
    include_package_data=True,
    install_requires=[],
    license="MIT",
)
