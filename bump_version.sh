#!/bin/bash

# Script to bump version in pyproject.toml
# Usage: ./bump_version.sh [major|minor|patch]

set -e

PYPROJECT_FILE="pyproject.toml"

if [ ! -f "$PYPROJECT_FILE" ]; then
    echo "Error: $PYPROJECT_FILE not found"
    exit 1
fi

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep -E '^version = ' "$PYPROJECT_FILE" | sed -E 's/version = "([^"]+)"/\1/')

if [ -z "$CURRENT_VERSION" ]; then
    echo "Error: Could not find version in $PYPROJECT_FILE"
    exit 1
fi

# Parse version components
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Determine which part to bump
BUMP_TYPE=${1:-patch}

case "$BUMP_TYPE" in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "Error: Invalid bump type '$BUMP_TYPE'"
        echo "Usage: $0 [major|minor|patch]"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Update version in pyproject.toml
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"
else
    # Linux
    sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"
fi

echo "Version bumped: $CURRENT_VERSION -> $NEW_VERSION ($BUMP_TYPE)"
echo ""
echo "Updated $PYPROJECT_FILE"
echo ""
echo "Note: __init__.py uses importlib.metadata to get version dynamically, so no update needed there."
