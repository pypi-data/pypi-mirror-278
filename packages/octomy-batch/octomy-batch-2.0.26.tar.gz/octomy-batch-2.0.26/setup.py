#!/usr/bin/env python

import re
import os
import pprint
from setuptools import setup, find_namespace_packages

import logging

logger = logging.getLogger(__name__)

setup_requirements = ["pytest-runner", "setuptools_scm"]

release_branch = "development"
beta_branch = "beta"

version_file = "./VERSION"
license_file = "./LICENSE"
changelog_file = "./CHANGELOG"
readme_file = "./README.md"
package_dir = "./" # Must be relative to the director where setup.py resides
python_version = "3.9"

group_base_name = "octomy"
base_name = "batch"
modules = ["octomy"] # group_base_name
short_description = (group_base_name+"/"+base_name),
package_name = f"{group_base_name}-{base_name}"

author_name = "OctoMY"
author_email = "pypi@octomy.org"


def read_file(fname, strip=True):
	fn = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname))
	data = ""
	if os.path.exists(fn):
		with open(fn) as f:
			data = f.read()
			data = data.strip() if strip else data
			# logger.info(f"Got data '{data}' from '{fn}'")
	else:
		logger.error(f"Could not find file {fn}")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	return data


def write_file(fname, data, do_overwrite=False):
	fn = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname))
	if not os.path.exists(fn) or do_overwrite:
		with open(fn, "w") as f:
			f.write(data)
	else:
		logger.warning(f"File {fn} already exists")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	return data


def remove_comment(line, sep="#"):
	i = line.find(sep)
	if i >= 0:
		line = line[:i]
	return line.strip()


def read_requirements_file(fname: str, do_strip: bool = True):
	fn = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname))
	print(f"Reading requirements from {fn} with do_strip = {do_strip}")
	lines = []
	if os.path.exists(fn):
		with open(fn) as f:
			for r in f.readlines():
				r = r.strip()
				if len(r) < 1:
					continue
				r = remove_comment(r)
				if len(r) < 1:
					continue
				lines.append(r)
	else:
		logger.error(f"Could not find requirements file {fn}")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	# logger.warning(f"Full content of '{fname}' was: \n{lines}")
	if not do_strip:
		return lines
	out = []
	for line in lines:
		if line and not line.startswith("-"):
			out.append(line)
	return out


def debug_repo(repo):
	if not repo:
		print(f"No repo")
		return
	print(f"Repository head commit: {repo.head.commit}")
	print(f"Found {len(repo.branches)} branches:")
	for branch in repo.branches:
		print(f" + {branch}({branch.commit})")
	remote = repo.remote()
	print(f"Found {len(remote.refs)} remote refs:")
	for ref in remote.refs:
		print(f" + {ref}({ref.commit})")


def get_git_branch_from_env():
	branch_env = "FK_GIT_ACTUAL_BRANCH"
	branch = os.environ.get(branch_env, None)
	if branch is not None:
		print(f"Using {branch_env} = {branch} from environment")
	else:
		print(f"No value for {branch_env} found")
	return branch


def get_license_name():
	fn = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), license_file))
	print(f"Reading license from {fn}")
	if os.path.exists(fn):
		with open(fn) as f:
			for r in f.readlines():
				r = r.strip()
				if len(r) < 1:
					continue
				# Return first non-empty line
				return r
	else:
		logger.error(f"Could not find license file {fn}")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	return "Proprietary" # Fall back to something safe


def generate_version_string(version=None, branch=None):
	version = read_file(version_file) if version is None else version
	branch = get_git_branch_from_env() if branch is None else branch
	full_version = ""
	# Calculate the version string based on current branch and bare version
	# TODO: Not tested
	if branch == release_branch:
		full_version = version
	elif branch == beta_branch:
		full_version = f"{version}b"
	elif "feature-" in branch:
		feature_branch_name = branch.replace("feature-", "")
		full_version = f"{version}-{feature_branch_name}"
	else:
		full_version = f"{version}-nonprod"
	print(f"Using full version = {full_version}")
	return full_version

def generate_development_status(version=None, branch=None):
	version = read_file(version_file) if version is None else version
	branch = get_git_branch_from_env() if branch is None else branch
	development_status = ""
	# Calculate the version string based on current branch and bare version
	if branch == release_branch:
		development_status = "Development Status :: 5 - Production/Stable"
	elif branch == beta_branch:
		development_status = "Development Status :: 4 - Beta"
	elif "feature-" in branch:
		development_status = "Development Status :: 3 - Alpha"
	else:
		development_status = "Development Status :: 1 - Planning"
	return development_status

def get_version_string():
	# Not viable
	# return generate_version_string();
	return read_file(version_file)


def get_development_status():
	# Not viable
	# return generate_development_status();
	return "Development Status :: 1 - Planning"


def get_packages():
	return find_namespace_packages(where=package_dir, include=[module+".*" for module in modules])


# Function to recursively list all files in a directory
def list_files(directory, base):
	paths = list()
	for (path, directories, filenames) in os.walk(directory):
		for filename in filenames:
			paths.append(os.path.relpath(os.path.join(path, filename), base))
	return paths


def get_package_data():
	data_filters = [
		re.compile(r'.*/sql(?:/sql)*/[^/]+\.sql$')
	]
	out = dict()
	for module in modules:
		modules_data_files = list_files(module, os.path.join(package_dir))
		data_files = list()
		for data_file in modules_data_files:
			for data_filter in data_filters:
				if data_filter.match(data_file):
					data_files.append(data_file)
					p = os.path.dirname(data_file)
					f = os.path.basename(data_file)
					m = ".".join(p.split("/"))
					ms = out.get(m, list())
					ms.append(f)
					out[m] = ms
					#print(f"########## FOUND: {data_file}    (p={p}, f={f}, m={m})")
					break

	print("Datafiles:---")
	print(pprint.pformat(out))
	print("-------------")
	return out

# From https://pypi.org/pypi?%3Aaction=list_classifiers
def get_classifiers():
	return [
		get_development_status()
		, "Intended Audience :: Developers"
		, "Intended Audience :: Information Technology"
		, "Intended Audience :: Science/Research"
		, "Intended Audience :: Other Audience"
		, "Topic :: Utilities"
		, "Natural Language :: English"
		, "Operating System :: POSIX :: Linux"
		, "Programming Language :: Python :: " + python_version
		, "Topic :: Other/Nonlisted Topic"
	]

package = {
	  "name": package_name
	, "version": get_version_string()
	, "author": author_name
	, "author_email": author_email
	, "maintainer": author_name
	, "maintainer_email": author_email
	, "description": short_description
	, "license": get_license_name()
	, "platforms": ["Linux"]
	, "keywords": "software"
	, "url": f"https://gitlab.com/{group_base_name}/{base_name}"
	# We use namespace packages to allow multiple packages to use the octomy prefix
	# We omit __init__.py tio accomplish this
	# See https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
	, "namespace_packages": modules
	, "packages": get_packages()
	, "package_dir": {'': package_dir}
	, "long_description": read_file(readme_file)
	, "long_description_content_type": "text/markdown"
	, "setup_requires": setup_requirements
	, "zip_safe": True
	# Allow flexible deps for install
	, "install_requires": read_requirements_file("requirements/requirements.in")
	# Use flexible deps for testing
	, "tests_require": read_requirements_file("requirements/test_requirements.in")
	, "test_suite": os.path.join(package_dir, "tests")
	, "python_requires": ">=" + python_version
	# NOTE: "data_files" is deprecated
	# NOTE: "package_data" need to reside inside a package, in other words a directory with __init__.py
	, "package_data": get_package_data()
	, "include_package_data": True
	, "classifiers": get_classifiers()
}

print("-------------------------------------------------------")
print("setup.py package:")
print(pprint.pformat(package))
print("-------------------------------------------------------")

# pprint.pprint(package)
setup(**package)
