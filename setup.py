from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jasper_embed",
    version="0.2.0",
    description="Embed JasperReports Server reports inside ERPNext/Frappe with per-Doctype mappings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Company",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
