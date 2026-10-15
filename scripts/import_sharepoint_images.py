#!/usr/bin/env python3
"""Fetch a fixed, approved SharePoint PNG batch and commit it to this repository."""
import json, os, re, struct, sys, urllib.request, urllib.error, base64, hashlib
from pathlib import Path

DRIVE = "b!Ye4_9P0xzk65c6Mj7bUkjX8oaSvbMhpPpVtTZ166XWfmlzKzjwuDSJb2t27rNY48"
ITEMS = {
 "01_launch.png":"01KL4L6A736B5NQEJXEJGLIHYQZUBBDC5N",
 "02_features.png":"01KL4L6A7R5KOFXLBHJBCLGYD7UOAEHH36",
 "03_trees.png":"01KL4L6AY52GRQFFQI5RF3MFHGPIC7VXYV",
 "04_follow.png":"01KL4L6A4JBVAWQ76ETREZFH3ZQC3QZRMZ",
}
DEST = Path("instagram/2026/2026-10-launch")
def download(item, token):
    url = f"https://graph.microsoft.com/v1.0/drives/{DRIVE}/items/{item}/content"
    req = urllib.request.Request(url,headers={"Authorization":"Bearer "+token})
    with urllib.request.urlopen(req,timeout=90) as r:
        return r.read(10_000_001)
def validate(data,name):
    if len(data)>10_000_000 or len(data)<24 or data[:8]!=b"\x89PNG\r\n\x1a\n" or data[12:16]!=b"IHDR":
        raise ValueError(f"Invalid PNG: {name}")
    width,height=struct.unpack(">II",data[16:24])
    if (width,height)!=(1080,1350):
        raise ValueError(f"Unexpected dimensions: {name}: {width}x{height}")
def main():
    if os.environ.get("GITHUB_REPOSITORY")!="MT-Daisuke/midoritech-social-assets":
        raise SystemExit("Unexpected repository")
    token=os.environ.get("GRAPH_ACCESS_TOKEN")
    if not token: raise SystemExit("GRAPH_ACCESS_TOKEN unavailable")
    DEST.mkdir(parents=True,exist_ok=True)
    summary=[]
    for name,item in ITEMS.items():
        data=download(item,token);validate(data,name)
        path=DEST/name
        if path.exists() and path.read_bytes()!=data:
            raise SystemExit(f"Existing asset differs; refusing overwrite: {path}")
        path.write_bytes(data)
        summary.append({"path":str(path),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
