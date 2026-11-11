import hashlib
import json
from pathlib import Path
import subprocess


def update_hashes(manifest, repo_dir):
    for asset in manifest["Assets"]:
        file_path = asset["FileName"]
        try:
            content = subprocess.check_output(
                ["git", "cat-file", "blob", f":{file_path}"],
                cwd=repo_dir,
            )
        except subprocess.CalledProcessError as exc:
            raise SystemExit(f"Cannot read the staged Git file: {file_path}") from exc

        asset["Hash"] = hashlib.sha1(content).hexdigest().upper()


def main():
    repo_dir = Path(__file__).resolve().parent
    manifest_path = repo_dir / "asset.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    update_hashes(manifest, repo_dir)
    with manifest_path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(manifest, file, indent=4)
        file.write("\n")


if __name__ == "__main__":
    main()
