from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='eenhoorntje_llm_lib',
    version='0.20',
    description='A lib for cached LLM calling and translation',
    author='Dmitrii Lukianov',
    author_email='unicornporated@gmil.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["openai", "google-generativeai", "google-cloud-translate"],
)
