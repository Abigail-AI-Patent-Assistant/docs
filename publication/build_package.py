"""Validate and package only the explicit public plugin files; never crawl a repo."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import zipfile

import jsonschema


def canonical_text_bytes(file):
    """All seven allowlisted files are UTF-8 text; normalize checkout newlines."""
    return file.read_text(encoding="utf-8").encode("utf-8")


def validate_openai_mcp(document):
    """Strict local contract for the documented OpenAI DCR example.

    Separate from the unchanged portable schema; not an official host validator.
    """
    def obj(properties):
        return {"type": "object", "properties": properties,
                "required": list(properties), "additionalProperties": False}

    auth = obj({"type": {"const": "oauth"},
                "client": obj({"mode": {"const": "dcr"}})})
    server = obj({"type": {"const": "streamable-http"},
                  "url": {"const": "https://mcp.abigail.app/mcp"},
                  "extensions": obj({"com.openai": obj({"auth": auth})})})
    contract = obj({"$schema": {"const": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"},
                    "mcpServers": obj({"abigail": server})})
    jsonschema.Draft202012Validator(contract).validate(document)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--schema-dir", required=True, type=Path)
    parser.add_argument("--target", choices=("portable", "openai"), default="portable")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "plugins" / "abigail"
    names = ["plugin.json", "mcp.json", ".claude-plugin/plugin.json", ".mcp.json",
             "skills/abigail-prosecution/SKILL.md", "LICENSE.md", "README.md"]
    for name in names:
        file = root / name
        if file.is_symlink() or not file.is_file():
            raise ValueError(f"Missing or linked package file: {name}")
        file.read_bytes().decode("utf-8")
    for name in ("plugin", "mcp"):
        schema = json.loads((args.schema_dir / f"{name}.schema.json").read_text())
        if schema.get("$id") != f"https://agent-plugins.org/schemas/1.0.0/{name}.schema.json":
            raise ValueError(f"Unexpected schema identity: {name}")
        jsonschema.Draft202012Validator(schema).validate(json.loads((root / f"{name}.json").read_text()))
    portable = json.loads((root / "plugin.json").read_text())
    legacy = json.loads((root / ".claude-plugin/plugin.json").read_text())
    for key in ("name", "version", "license"):
        if portable[key] != legacy[key]:
            raise ValueError(f"Host manifest mismatch: {key}")
    endpoints = [json.loads((root / name).read_text())["mcpServers"]["abigail"]["url"]
                 for name in ("mcp.json", ".mcp.json")]
    if endpoints != ["https://mcp.abigail.app/mcp"] * 2:
        raise ValueError("Unexpected public endpoint")
    payload = {name: canonical_text_bytes(root / name) for name in names}
    if args.target == "openai":
        settings = json.loads((Path(__file__).parent / "openai-auth-settings.json").read_text())
        if settings["endpoint"] != endpoints[0]:
            raise ValueError("OAuth configuration endpoint differs from packaged server")
        hosted = copy.deepcopy(json.loads(payload["mcp.json"]))
        hosted["mcpServers"]["abigail"]["extensions"] = {
            "com.openai": {"auth": settings["auth"]}}
        validate_openai_mcp(hosted)
        payload["mcp.json"] = (json.dumps(hosted, indent=2) + "\n").encode("utf-8")
    if args.output.exists():
        raise FileExistsError("Choose a new output filename; preserve prior package receipts")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, payload[name])
    with zipfile.ZipFile(args.output) as archive:
        if archive.testzip() or set(archive.namelist()) != set(names):
            raise ValueError("ZIP integrity or allowlist mismatch")
    receipt = {"artifact": args.output.name, "target": args.target,
               "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
               "files": {name: hashlib.sha256(payload[name]).hexdigest() for name in names},
               "validation": ("Portable schemas, identity/endpoint parity, ZIP allowlist/integrity passed."
                   if args.target == "portable" else
                   "Portable source schemas plus separate strict OpenAI documented-DCR contract, identity/endpoint and ZIP checks passed. Emitted OpenAI mcp.json has vendor extensions and is NOT certified by the portable MCP schema."),
               "host_acceptance": "NOT RUN: no authenticated portal scan, install, submission or OAuth connection claimed."}
    args.output.with_suffix(".receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
