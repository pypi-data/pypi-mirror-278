#!/bin/bash

# Extract the current version using basic regular expressions
current_version=$(grep 'version = ' pyproject.toml | sed -E 's/version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/')

# Separate the version into major, minor, and patch numbers
major=$(echo "$current_version" | cut -d '.' -f1)
minor=$(echo "$current_version" | cut -d '.' -f2)
patch=$(echo "$current_version" | cut -d '.' -f3)

# Increment the patch number
new_patch=$((patch + 1))

# Form the new version string
new_version="$major.$minor.$new_patch"

# Replace the old version with the new version in the file
sed -i.bak -E "s/(version = \")$major\.$minor\.$patch/\1$new_version/" pyproject.toml

# Remove the backup file created by sed
rm pyproject.toml.bak

echo "Version bumped from $current_version to $new_version"
