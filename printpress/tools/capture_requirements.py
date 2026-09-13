#!/usr/bin/env python3
"""Capture and verify a grant application's requirements without paraphrase drift.

The JSON ledger is authoritative. APPLICATION_STRUCTURE.md is a generated reading
view. This tool checks fidelity and completeness; it does not decide which language
matters strategically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


# kitlib.py is vendored alongside this file so the tool stands alone inside the
# skill. Upstream copy: rustin-tools/knowledge-layer/tools/kitlib.py — if that one
# changes, re-vendor. Ported into printpress 2026-09-12.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from kitlib import normalize  # noqa: E402  (vendored; see note above)


LEDGER_NAME = "application-requirements.json"
GENERATED_NAME = "APPLICATION_STRUCTURE.md"
SCHEMA_VERSION = 1
KINDS = (
    "prompts",
    "criteria",
    "eligibility",
    "attachments",
    "budget",
    "formatting",
    "submission_mechanics",
    "reporting",
    "decision_timing",
    "ai_use",
    "governance_disclosures",
)
STATUSES = {"captured", "not_published", "unresolved"}
PARTY_TYPES = {"institute", "fiscal_sponsor", "named_leader", "unresolved"}


class LedgerError(ValueError):
    pass


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def ledger_digest(data: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_ledger(app_dir: Path) -> dict[str, Any]:
    path = app_dir / LEDGER_NAME
    if not path.is_file():
        raise LedgerError(f"missing {LEDGER_NAME}; run init first")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LedgerError(f"cannot read {LEDGER_NAME}: {exc}") from exc
    if not isinstance(data, dict):
        raise LedgerError(f"{LEDGER_NAME} must contain one JSON object")
    return data


def write_ledger(app_dir: Path, data: dict[str, Any]) -> None:
    (app_dir / LEDGER_NAME).write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def source_path(app_dir: Path, declared: str) -> Path:
    if not isinstance(declared, str) or not declared.strip():
        raise LedgerError("source path must be a non-empty string")
    candidate = Path(declared)
    resolved = (candidate if candidate.is_absolute() else app_dir / candidate).resolve()
    try:
        resolved.relative_to(app_dir.resolve())
    except ValueError as exc:
        raise LedgerError(f"source must live inside the application folder: {declared}") from exc
    return resolved


def source_spec(source_id: str, path: str, app_dir: Path) -> dict[str, str]:
    resolved = source_path(app_dir, path)
    if not resolved.is_file():
        raise LedgerError(f"source file does not exist: {path}")
    relative = resolved.relative_to(app_dir.resolve()).as_posix()
    return {"id": source_id, "path": relative, "sha256": file_digest(resolved)}


def new_ledger(app_dir: Path, posting: str, portal: str | None) -> dict[str, Any]:
    sources = [source_spec("posting", posting, app_dir)]
    if portal:
        sources.append(source_spec("portal", portal, app_dir))
    requirements = []
    for kind in KINDS:
        requirements.append(
            {
                "id": f"{kind}-001",
                "kind": kind,
                "status": "unresolved",
                "required": True,
                "source": None,
                "verbatim": None,
                "interpretation": "",
                "funder_purpose": "",
                "applies_to": "",
                "notes": "",
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "application": {
            "id": app_dir.name,
            "name": "",
            "funder": "",
            "opportunity_url": "",
            "applicant": {"type": "unresolved", "legal_name": ""},
            "payee": {"type": "unresolved", "legal_name": ""},
        },
        "sources": sources,
        "requirements": requirements,
    }


def validate(
    app_dir: Path,
    data: dict[str, Any],
    *,
    require_resolved: bool,
    check_source_hashes: bool,
) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    application = data.get("application")
    if not isinstance(application, dict):
        errors.append("application must be an object")
        application = {}
    if require_resolved:
        for field in ("id", "name", "funder"):
            value = application.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"application.{field} must be resolved before check")
    for role in ("applicant", "payee"):
        party = application.get(role)
        if not isinstance(party, dict):
            errors.append(f"application.{role} must be an object")
            continue
        if party.get("type") not in PARTY_TYPES:
            errors.append(
                f"application.{role}.type must be one of {sorted(PARTY_TYPES)}"
            )
        elif require_resolved and party.get("type") == "unresolved":
            errors.append(f"application.{role}.type remains unresolved")
        if require_resolved:
            legal_name = party.get("legal_name")
            if not isinstance(legal_name, str) or not legal_name.strip():
                errors.append(f"application.{role}.legal_name must be resolved before check")

    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
        sources = []
    source_map: dict[str, dict[str, Any]] = {}
    for index, spec in enumerate(sources):
        where = f"sources[{index}]"
        if not isinstance(spec, dict):
            errors.append(f"{where} must be an object")
            continue
        source_id = spec.get("id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"{where}.id must be a non-empty string")
            continue
        if source_id in source_map:
            errors.append(f"duplicate source id: {source_id}")
            continue
        source_map[source_id] = spec
        try:
            path = source_path(app_dir, spec.get("path"))
        except LedgerError as exc:
            errors.append(f"{where}: {exc}")
            continue
        if not path.is_file():
            errors.append(f"missing source file: {spec.get('path')}")
        elif check_source_hashes and spec.get("sha256") != file_digest(path):
            errors.append(
                f"source changed since the ledger was built: {spec.get('path')}"
            )
    if "posting" not in source_map:
        errors.append("sources must retain the required posting source")

    requirements = data.get("requirements")
    if not isinstance(requirements, list):
        errors.append("requirements must be a list")
        requirements = []
    seen_ids: set[str] = set()
    represented_kinds: set[str] = set()
    source_text_cache: dict[str, str] = {}

    for index, requirement in enumerate(requirements):
        where = f"requirements[{index}]"
        if not isinstance(requirement, dict):
            errors.append(f"{where} must be an object")
            continue
        requirement_id = requirement.get("id")
        if not isinstance(requirement_id, str) or not requirement_id:
            errors.append(f"{where}.id must be a non-empty string")
        elif requirement_id in seen_ids:
            errors.append(f"duplicate requirement id: {requirement_id}")
        else:
            seen_ids.add(requirement_id)

        kind = requirement.get("kind")
        if kind not in KINDS:
            errors.append(f"{where} has invalid kind {kind!r}")
        else:
            represented_kinds.add(kind)

        status = requirement.get("status")
        if status not in STATUSES:
            errors.append(f"{where} has invalid status {status!r}")
            continue
        required = requirement.get("required")
        if not isinstance(required, bool):
            errors.append(f"{where}.required must be true or false")
        if require_resolved and required is True and status == "unresolved":
            errors.append(
                f"required category remains unresolved: {kind} ({requirement_id})"
            )

        if status == "captured":
            source_id = requirement.get("source")
            excerpt = requirement.get("verbatim")
            if source_id not in source_map:
                errors.append(f"{where} cites unknown source {source_id!r}")
                continue
            if not isinstance(excerpt, str) or not excerpt.strip():
                errors.append(f"{where} is captured but has no verbatim excerpt")
                continue
            if source_id not in source_text_cache:
                try:
                    path = source_path(app_dir, source_map[source_id].get("path"))
                    source_text_cache[source_id] = path.read_text(
                        encoding="utf-8", errors="replace"
                    )
                except (LedgerError, OSError) as exc:
                    errors.append(f"{where} cannot read source {source_id!r}: {exc}")
                    continue
            if normalize(excerpt) not in normalize(source_text_cache[source_id]):
                errors.append(
                    f"{where} verbatim excerpt not found in source {source_id!r}: "
                    f"{excerpt[:80]!r}"
                )
        elif status == "not_published":
            if requirement.get("verbatim") not in (None, ""):
                errors.append(f"{where} is not_published but contains a verbatim excerpt")

    missing = [kind for kind in KINDS if kind not in represented_kinds]
    if missing:
        errors.append(f"missing required categories: {', '.join(missing)}")
    return errors


def refreshed_sources(app_dir: Path, data: dict[str, Any]) -> None:
    for spec in data.get("sources", []):
        path = source_path(app_dir, spec.get("path"))
        if not path.is_file():
            raise LedgerError(f"missing source file: {spec.get('path')}")
        spec["sha256"] = file_digest(path)


def blockquote(text: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def render(data: dict[str, Any]) -> str:
    digest = ledger_digest(data)
    app = data["application"]
    sources = {item["id"]: item for item in data["sources"]}
    lines = [
        f"<!-- generated-from-sha256: {digest} -->",
        "# Application structure",
        "",
        "> Generated from `application-requirements.json`. Edit the JSON, then run",
        "> `python3 workflows/tools/capture_requirements.py build APP_DIR`.",
        "",
        "## Application identity",
        "",
        f"- Application: {app.get('name') or '[unresolved]'}",
        f"- Funder: {app.get('funder') or '[unresolved]'}",
        f"- Applicant: {app.get('applicant', {}).get('type')} — "
        f"{app.get('applicant', {}).get('legal_name') or '[name unresolved]'}",
        f"- Payee: {app.get('payee', {}).get('type')} — "
        f"{app.get('payee', {}).get('legal_name') or '[name unresolved]'}",
        "",
        "## Captured sources",
        "",
    ]
    for source in data["sources"]:
        lines.append(f"- `{source['id']}`: `{source['path']}` (`{source['sha256'][:12]}…`)")
    lines.append("")

    for kind in KINDS:
        lines.extend([f"## {kind.replace('_', ' ').title()}", ""])
        for item in (req for req in data["requirements"] if req.get("kind") == kind):
            lines.append(f"### {item.get('id', '[missing id]')} — {item.get('status')}")
            lines.append("")
            if item.get("status") == "captured":
                source = sources[item["source"]]
                lines.append(f"Source: `{source['path']}`")
                lines.append("")
                lines.append(blockquote(item["verbatim"]))
                lines.append("")
            for field, label in (
                ("funder_purpose", "Why/how the funder uses it"),
                ("interpretation", "Interpretation"),
                ("applies_to", "Applies to"),
                ("notes", "Notes"),
            ):
                if item.get(field):
                    lines.append(f"- {label}: {item[field]}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def init_command(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).resolve()
    app_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = app_dir / LEDGER_NAME
    if ledger_path.exists():
        raise LedgerError(f"refusing to overwrite existing {ledger_path}")
    data = new_ledger(app_dir, args.posting, args.portal)
    write_ledger(app_dir, data)
    print(f"Created {ledger_path}")
    print("All requirement categories begin unresolved; capture or mark not_published before check.")
    return 0


def build_command(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).resolve()
    data = load_ledger(app_dir)
    refreshed_sources(app_dir, data)
    errors = validate(
        app_dir, data, require_resolved=False, check_source_hashes=True
    )
    if errors:
        raise LedgerError("\n".join(errors))
    write_ledger(app_dir, data)
    output = app_dir / GENERATED_NAME
    output.write_text(render(data), encoding="utf-8")
    print(f"Built {output}")
    return 0


def generated_digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    first = path.read_text(encoding="utf-8", errors="replace").splitlines()[0:1]
    if not first or not first[0].startswith("<!-- generated-from-sha256: "):
        return None
    return first[0].removeprefix("<!-- generated-from-sha256: ").removesuffix(" -->")


def check_command(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).resolve()
    data = load_ledger(app_dir)
    errors = validate(app_dir, data, require_resolved=True, check_source_hashes=True)
    expected = ledger_digest(data)
    actual = generated_digest(app_dir / GENERATED_NAME)
    if actual != expected:
        errors.append(
            f"{GENERATED_NAME} is stale or missing; run build after editing {LEDGER_NAME}"
        )
    if errors:
        raise LedgerError("\n".join(errors))
    print(f"PASS — {len(data['requirements'])} requirement records verified on {date.today()}")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="create the authoritative JSON ledger")
    init.add_argument("app_dir")
    init.add_argument("--posting", required=True)
    init.add_argument("--portal")
    init.set_defaults(function=init_command)
    for name, function, help_text in (
        ("build", build_command, "generate APPLICATION_STRUCTURE.md from the ledger"),
        ("check", check_command, "verify completeness, fidelity, and freshness"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("app_dir")
        command.set_defaults(function=function)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.function(args)
    except LedgerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
