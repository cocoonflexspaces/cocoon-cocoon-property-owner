#!/usr/bin/env python3
"""
Run once to decode Drive images into img/spaces/.
Usage: python3 decode-images.py
"""
import json, base64, os, glob, sys

TEMP_DIR = "/var/folders/8c/gk6b2v5s3j78jh7r8rzxy2ym0000gn/T/claude-hostloop-plugins/ae6b471fb56e864b/projects/-Users-eduardmonteagudomartin-Library-Application-Support-Claude-local-agent-mode-sessions-ddbe9cc6-4295-4fa3-909e-1efe05b5ccdc-db67cb29-f1e1-4021-a272-cf20d48e48ad-local-01754788-c897-41e5-a33b-f90c3-vz9uim/8df74dc5-c258-4f8f-91fc-38b48ec1730e/tool-results"
OUT_DIR  = os.path.join(os.path.dirname(__file__), "img", "spaces")

# Map Drive file titles → output filenames
# Only the 3 new images needed — others already saved from previous run
TITLE_MAP = {
    "cocoon-casa-maxima-sitting-room-large-yellow-circular-couch-large-windows.jpg":     "faq-hero.jpg",
    "cocoon-casa-diamond-second-floor-office-lounge-area.jpg":                           "who-we-are.jpg",
    "cocoon-casa-diamond-first-floor-entrance-fireplace.jpg":                            "who-we-are-alt.jpg",
}

files = glob.glob(os.path.join(TEMP_DIR, "mcp-d6fe47d9*download_file_content*.txt"))
if not files:
    print(f"No temp files found in:\n  {TEMP_DIR}")
    print("The session may have been cleaned up. Re-run the Drive downloads.")
    sys.exit(1)

os.makedirs(OUT_DIR, exist_ok=True)
saved = []

for path in files:
    try:
        with open(path) as f:
            data = json.load(f)
        title   = data.get("title", "")
        content = data.get("content", "")
        mime    = data.get("mimeType", "image/jpeg")
        if title in TITLE_MAP and content:
            out_name = TITLE_MAP[title]
            out_path = os.path.join(OUT_DIR, out_name)
            img_bytes = base64.b64decode(content)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            size_kb = len(img_bytes) // 1024
            print(f"  ✓  {out_name}  ({size_kb} KB)  ← {title}")
            saved.append(out_name)
    except Exception as e:
        print(f"  ✗  {os.path.basename(path)}: {e}")

print(f"\nDone — {len(saved)}/{len(TITLE_MAP)} images saved to img/spaces/")
if len(saved) < len(TITLE_MAP):
    missing = [v for k,v in TITLE_MAP.items() if v not in saved]
    print("Missing:", ", ".join(missing))
