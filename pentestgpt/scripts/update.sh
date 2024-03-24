#!/bin/bash

# This script updates the requirements.txt and setup.py files with the version and dependencies from pyproject.toml
# as a part of the development pipeline of pentestgpt.

# Convert pyproject.toml to JSON using python (requires toml package)
PYPROJECT_JSON=$(python -c 'import toml; import json; import sys; print(json.dumps(toml.load(sys.stdin)))' < pyproject.toml)

# Extract the version from pyproject.toml
VERSION=$(echo "$PYPROJECT_JSON" | jq -r '.tool.poetry.version')

# Update requirements.txt with poetry
poetry export --without-hashes --format=requirements.txt > requirements.txt


# Update setup.py
sed -i '' "s/version=\"[^\"]*\"/version=\"$VERSION\"/" setup.py

# Update version in pentestgpt/_version.py
echo "__version__ = '\"$VERSION\"'" > pentestgpt/_version.py

echo "Updated requirements.txt and setup.py with version $VERSION."