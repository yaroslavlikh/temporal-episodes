"""Download the SocialMemBench parquet files used by these runs and verify SHA-256.

The runners were executed against anon4data/socialmembench at revision
ea7e4acf502df3eda484d56165ec594d6f4c138f. At that revision the files live under
`<name>/train/0000.parquet`; the runners expect `<data-dir>/<name>.parquet`.

    python3 fetch_socialmembench.py --data-dir /tmp/socialmembench
"""
from __future__ import annotations

import argparse
import hashlib
import urllib.request
from pathlib import Path

REVISION = "ea7e4acf502df3eda484d56165ec594d6f4c138f"
BASE_URL = f"https://huggingface.co/datasets/anon4data/socialmembench/resolve/{REVISION}"
FILES = {
    "conversations.parquet": ("conversations/train/0000.parquet",
                              "f9ed5d10501cd8a46ca09bb914866ae3069136c259d99ee24dd175e30c90c88d"),
    "qa.parquet": ("qa/train/0000.parquet",
                   "98990f88a25df0d9a017488d39ca50e76f432b6554c67b2beafa5f9421ee3f5e"),
    "personas.parquet": ("personas/train/0000.parquet",
                         "723d941291a0c5ce30c9892670cd7571796d6e0b0b6487212009c3a1ed026a62"),
    "networks.parquet": ("networks/train/0000.parquet",
                         "e85e7bfd5fd61bf4d5cbd7ad49b3c57a945198480e6c2dba46499fba1ced1a57"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("/tmp/socialmembench"))
    args = parser.parse_args()
    args.data_dir.mkdir(parents=True, exist_ok=True)
    for local_name, (remote_path, expected) in FILES.items():
        target = args.data_dir / local_name
        if not target.exists():
            urllib.request.urlretrieve(f"{BASE_URL}/{remote_path}", target)
        actual = sha256(target)
        if actual != expected:
            raise SystemExit(f"checksum mismatch for {target}: {actual} != {expected}")
        print(f"ok  {local_name}  {actual}")


if __name__ == "__main__":
    main()
