#!/usr/bin/env python3
"""Check domain availability with priority global TLDs and bonus .cz."""

from __future__ import annotations

import argparse
import csv
import socket
import sys
from dataclasses import dataclass


DEFAULT_GLOBAL_TLDS = ["com", "io", "ai", "app", "dev"]
DEFAULT_TIMEOUT_SECONDS = 6.0

WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "io": "whois.nic.io",
    "ai": "whois.nic.ai",
    "app": "whois.nic.google",
    "dev": "whois.nic.google",
    "cz": "whois.nic.cz",
}

FREE_PATTERNS = {
    "com": ["no match for"],
    "io": ["is available for purchase", "not found"],
    "ai": ["domain status: available", "no match"],
    "app": ["domain not found"],
    "dev": ["domain not found"],
    "cz": ["no entries found"],
}

TAKEN_PATTERNS = {
    "com": ["domain name:"],
    "io": ["domain name:"],
    "ai": ["domain:"],
    "app": ["domain name:"],
    "dev": ["domain name:"],
    "cz": ["domain:"],
}


@dataclass
class Result:
    status: str
    note: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check domain availability, prioritize free global TLDs, and treat free .cz as a bonus."
    )
    parser.add_argument(
        "--names",
        required=True,
        help="Comma-separated candidate names without TLDs, e.g. 'lumo,verigo,fluxora'",
    )
    parser.add_argument(
        "--global-tlds",
        default=",".join(DEFAULT_GLOBAL_TLDS),
        help="Comma-separated priority global TLDs, default: com,io,ai,app,dev",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Socket timeout in seconds for WHOIS requests",
    )
    parser.add_argument(
        "--format",
        choices=("table", "csv"),
        default="table",
        help="Output format",
    )
    return parser.parse_args()


def normalize_name(raw: str) -> str:
    return "".join(ch for ch in raw.strip().lower() if ch.isalnum() or ch == "-")


def whois_query(server: str, domain: str, timeout: float) -> str:
    with socket.create_connection((server, 43), timeout=timeout) as conn:
        conn.sendall((domain + "\r\n").encode("utf-8"))
        chunks: list[bytes] = []
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8", errors="replace")


def classify_domain(tld: str, body: str) -> Result:
    lowered = body.lower()

    for pattern in FREE_PATTERNS.get(tld, []):
        if pattern in lowered:
            return Result("free", "WHOIS indicates no registration")

    for pattern in TAKEN_PATTERNS.get(tld, []):
        if pattern in lowered:
            return Result("taken", "WHOIS indicates an existing registration")

    return Result("unknown", "WHOIS response could not be classified reliably")


def check_domain(name: str, tld: str, timeout: float) -> Result:
    server = WHOIS_SERVERS.get(tld)
    if not server:
        return Result("unknown", f"No WHOIS server configured for .{tld}")

    domain = f"{name}.{tld}"
    try:
        body = whois_query(server, domain, timeout)
    except OSError as exc:
        return Result("unknown", f"WHOIS query failed: {exc}")

    return classify_domain(tld, body)


def pick_best_global(name: str, tlds: list[str], timeout: float) -> tuple[str, Result, dict[str, Result]]:
    results: dict[str, Result] = {}
    for tld in tlds:
        result = check_domain(name, tld, timeout)
        results[tld] = result
        if result.status == "free":
            return tld, result, results
    first_tld = tlds[0]
    return first_tld, results[first_tld], results


def build_rows(names: list[str], global_tlds: list[str], timeout: float) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for name in names:
        best_tld, best_result, global_results = pick_best_global(name, global_tlds, timeout)
        cz_result = check_domain(name, "cz", timeout)

        if best_result.status == "free" and cz_result.status == "free":
            status = "bonus"
            notes = "priority global domain appears free and .cz is also free"
        elif best_result.status == "free":
            status = "keep"
            notes = f"priority global domain appears free; .cz={cz_result.status}"
        elif best_result.status == "unknown" or cz_result.status == "unknown":
            status = "unknown"
            notes = f"global={best_result.note}; cz={cz_result.note}"
        else:
            status = "reject"
            notes = f"best global .{best_tld}={best_result.status}; .cz={cz_result.status}"

        rows.append(
            {
                "name": name,
                "best_global": f".{best_tld}",
                "best_global_status": best_result.status,
                "cz_status": cz_result.status,
                "status": status,
                "notes": notes,
                "checked_globals": ", ".join(
                    f".{tld}:{result.status}" for tld, result in global_results.items()
                ),
            }
        )
    return rows


def print_table(rows: list[dict[str, str]]) -> None:
    headers = ["name", "best_global", "best_global_status", "cz_status", "status", "notes"]
    widths = {
        header: max(len(header), *(len(row[header]) for row in rows)) if rows else len(header)
        for header in headers
    }
    header_line = "  ".join(header.ljust(widths[header]) for header in headers)
    print(header_line)
    print("  ".join("-" * widths[header] for header in headers))
    for row in rows:
        print("  ".join(row[header].ljust(widths[header]) for header in headers))


def print_csv(rows: list[dict[str, str]]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()) if rows else [])
    if not rows:
        return
    writer.writeheader()
    writer.writerows(rows)


def main() -> int:
    args = parse_args()
    names = [normalize_name(raw) for raw in args.names.split(",")]
    names = [name for name in names if name]
    global_tlds = [tld.strip().lower().lstrip(".") for tld in args.global_tlds.split(",")]
    global_tlds = [tld for tld in global_tlds if tld]

    if not names:
        print("No valid names were provided.", file=sys.stderr)
        return 2
    if not global_tlds:
        print("No global TLDs were provided.", file=sys.stderr)
        return 2

    rows = build_rows(names, global_tlds, args.timeout)

    if args.format == "csv":
        print_csv(rows)
    else:
        print_table(rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
