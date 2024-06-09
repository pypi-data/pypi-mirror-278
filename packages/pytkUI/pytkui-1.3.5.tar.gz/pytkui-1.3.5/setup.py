import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytkUI",
    version="1.3.5",
    author="iamxcd",
    description="TkinterHelper布局助手官方拓展和工具库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.pytk.net",
    packages=setuptools.find_packages(),
    package_data={
        'pytkUI.icons': ['bootstrap-icons.json', 'bootstrap-icons.woff']
    }
)
