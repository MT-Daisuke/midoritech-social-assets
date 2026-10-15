#!/usr/bin/env python3
"""Import explicitly approved SharePoint PNG assets described in a reviewed manifest."""
import argparse
import hashlib
import json
import os
import re
import struct
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "manifests"
TARGET = ROOT / "instagram"
MAX_BYTES = 10_000_000
DRIVE_RE = re.compile(r"^[A-Za-z0-9!_-]{12,200}$")
ITEM_RE = re.compile(r"^[A-Za-z0-9_-]{10,160}$")
BATCH_RE = re.compile(r"^20[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]{0,55}$")
NAME_RE = re.compile(r"^[0-9]{2}_[a-z0-9_-]+\.png$")


def validate_png(data, filename, expected):
    if not 24 <= len(data) <= MAX_BYTES or data[:8] != bytes.fromhex("89504e470d0a1a0a") or data[12:16] != b"IHDR":
        raise ValueError(f"Invalid PNG: {filename}")
    dims = struct.unpack(">II", data[16:24])
    if tuple(expected) != dims:
        raise ValueError(f"Image dimensions mismatch: {filename}: {dims}")


def load_manifest(batch):
    if not BATCH_RE.fullmatch(batch):
        raise ValueError("Invalid batch name")
    path = MANIFESTS / (batch + ".json")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("batch") != batch or data.get("approved") is not True:
        raise ValueError("Batch manifest not approved")
    if data.get("destination") != f"instagram/{batch[:4]}/{batch}":
        raise ValueError("Invalid destination")
    if not DRIVE_RE.fullmatch(data.get("drive_id", "")):
        raise ValueError("Invalid drive ID")
    images = data.get("images")
    if not isinstance(images, list) or not 1 <= len(images) <= 10:
        raise ValueError("Expected 1 to 10 images")
    seen = set()
    for index, image in enumerate(images, 1):
        name = image.get("filename", "")
        if not NAME_RE.fullmatch(name) or not name.startswith(f"{index:02d}_") or name in seen:
            raise ValueError("Invalid or unordered filename")
        seen.add(name)
        if not ITEM_RE.fullmatch(image.get("item_id", "")):
            raise ValueError("Invalid SharePoint item ID")
        dims = image.get("dimensions")
        if not isinstance(dims, list) or len(dims) != 2 or any(type(v) is not int or v < 1 or v > 4096 for v in dims):
            raise ValueError("Invalid dimensions")
        sha = image.get("sha256")
        if sha is not None and not re.fullmatch(r"[a-f0-9]{64}", sha):
            raise ValueError("Invalid SHA-256")
    return data


def fetch(drive_id, item_id, token):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content"
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read(MAX_BYTES + 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True)
    args = parser.parse_args()
    if os.getenv("GITHUB_REPOSITORY") != "MT-Daisuke/midoritech-social-assets":
        raise SystemExit("Unexpected repository")
    token = os.getenv("GRAPH_ACCESS_TOKEN")
    if not token:
        raise SystemExit("GRAPH_ACCESS_TOKEN missing")
    manifest = load_manifest(args.batch)
    destination = ROOT / manifest["destination"]
    # Download and validate entire batch before writing anything.
    pending = []
    for image in manifest["images"]:
        data = fetch(manifest["drive_id"], image["item_id"], token)
        validate_png(data, image["filename"], image["dimensions"])
        digest = hashlib.sha256(data).hexdigest()
        if image.get("sha256") and image["sha256"] != digest:
            raise ValueError("Approved checksum mismatch: " + image["filename"])
        output = destination / image["filename"]
        if output.exists() and output.read_bytes() != data:
            raise ValueError("Refusing to overwrite existing published image: " + str(output))
        pending.append((output, data, digest))
    destination.mkdir(parents=True, exist_ok=True)
    for output, data, digest in pending:
        output.write_bytes(data)
        print(json.dumps({"path": str(output.relative_to(ROOT)), "bytes": len(data), "sha256": digest}))


if __name__ == "__main__":
    main()
