#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
OUTPUT="$PROJECT_DIR/android/app/build/outputs/bundle/release/app-release.aab"

echo "=== YT Player AAB 빌드 ==="
echo "프로젝트: $PROJECT_DIR"
echo ""

cd "$PROJECT_DIR/android"
ANDROID_HOME="$ANDROID_HOME" ./gradlew bundleRelease

echo ""
echo "=== 빌드 완료 ==="
echo "파일: $OUTPUT"
echo "크기: $(du -sh "$OUTPUT" | cut -f1)"
