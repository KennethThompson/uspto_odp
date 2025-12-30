#!/bin/bash

# Script to create v1.0.0 release tag
# This script will:
# 1. Commit version changes
# 2. Create an annotated git tag
# 3. Push the tag to GitHub

set -e

VERSION="1.0.0"
TAG_NAME="v${VERSION}"

echo "🚀 Creating release ${TAG_NAME}"

# Check if we're on the main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "⚠️  Warning: You're not on the main branch. Current branch: $CURRENT_BRANCH"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "📝 Staging changes..."
    git add pyproject.toml RELEASE_NOTES_v1.0.0.md
    echo "💾 Committing version bump..."
    git commit -m "Bump version to ${VERSION} and add release notes"
fi

# Check if tag already exists
if git rev-parse "${TAG_NAME}" >/dev/null 2>&1; then
    echo "⚠️  Tag ${TAG_NAME} already exists!"
    read -p "Delete and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "${TAG_NAME}"
        git push origin :refs/tags/"${TAG_NAME}" 2>/dev/null || true
    else
        exit 1
    fi
fi

# Create annotated tag with release notes
echo "🏷️  Creating annotated tag ${TAG_NAME}..."
git tag -a "${TAG_NAME}" -F RELEASE_NOTES_v1.0.0.md

echo "✅ Tag created successfully!"
echo ""
echo "📤 To push the tag to GitHub, run:"
echo "   git push origin ${TAG_NAME}"
echo "   git push origin main"
echo ""
echo "🌐 Then create a GitHub release at:"
echo "   https://github.com/KennethThompson/uspto_odp/releases/new"
echo ""
echo "   Tag: ${TAG_NAME}"
echo "   Title: Release ${TAG_NAME}"
echo "   Description: Copy contents from RELEASE_NOTES_v1.0.0.md"
