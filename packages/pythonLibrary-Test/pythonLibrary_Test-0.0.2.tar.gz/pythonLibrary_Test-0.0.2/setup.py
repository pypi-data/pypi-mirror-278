from setuptools import setup, find_packages

#to copy the cotent of the README.md file in the virable description
with open("README.md", "r") as f:
    description = f.read()

setup(
	name = 'pythonLibrary_Test',
	version = '0.0.2',	
	packages = find_packages(),
	install_requires = [
	#Add dependencies here.
	#e.g. "numpy >= 1.11.1'
	],
    long_description=description,
    long_description_content_type="text/markdown",

        # entry_points = {
    #     "console_scripts" = [
    #         "pythonLibrary = pythonLibrary_hello:hello",
    #         ],
    # },
)