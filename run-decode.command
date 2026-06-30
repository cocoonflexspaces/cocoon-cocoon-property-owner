#!/bin/bash
cd "$(dirname "$0")"
echo "🔍 Looking for downloaded Drive images..."
python3 decode-images.py
echo ""
echo "✅ Done. You can close this window."
