"""Download every attachment of one Jira issue (screenshots, inline images, PDFs, xlsx).

Usage: python -I fetch_attachments.py ABC-123 [--out DIR]
       python -I fetch_attachments.py --maid   (War Room maid: delete downloads of finished tickets)
Needs JIRA_READ_EMAIL, JIRA_READ_TOKEN (a scoped read:jira-work API token) and JIRA_CLOUD_ID.
"""
import argparse
import base64
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request

# Scoped API tokens only work through api.atlassian.com, not <your-site>.atlassian.net.
CLOUD_ID = os.environ.get("JIRA_CLOUD_ID", "")
API = f"https://api.atlassian.com/ex/jira/{CLOUD_ID}/rest/api/3"
KEY = re.compile(r"[A-Z][A-Z0-9]+-\d+")
ROOT = os.path.join(tempfile.gettempdir(), "jira-attachments")


def get(url, auth):
    req = urllib.request.Request(url, headers={"Authorization": auth, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def safe_name(att):
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", os.path.basename(att["filename"])).strip(" .")
    return f"{att['id']}-{name or 'file'}"


def maid(auth):
    """Delete ROOT/<KEY> folders whose ticket is Done or no longer assigned to me."""
    me = json.loads(get(f"{API}/myself", auth))["accountId"]
    keys = sorted(d for d in os.listdir(ROOT) if KEY.fullmatch(d)) if os.path.isdir(ROOT) else []
    print(f"maid: {len(keys)} ticket folder(s) in {ROOT}")
    for key in keys:
        try:
            fields = json.loads(get(f"{API}/issue/{key}?fields=status,assignee", auth))["fields"]
        except urllib.error.HTTPError as e:
            print(f"kept\t{key}\tHTTP {e.code}, status unknown")
            continue
        assignee = fields.get("assignee") or {}
        state = f"{fields['status']['name']}, assignee {assignee.get('displayName', 'none')}"
        if fields["status"]["statusCategory"]["key"] == "done" or assignee.get("accountId") != me:
            shutil.rmtree(os.path.join(ROOT, key))
            print(f"deleted\t{key}\t{state}")
        else:
            print(f"kept\t{key}\t{state}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("key", nargs="?")
    parser.add_argument("--out")
    parser.add_argument("--maid", action="store_true")
    args = parser.parse_args()

    if not args.maid and not (args.key and KEY.fullmatch(args.key)):
        sys.exit(f"Not an issue key: {args.key}")
    email, token = os.environ.get("JIRA_READ_EMAIL"), os.environ.get("JIRA_READ_TOKEN")
    if not (email and token and CLOUD_ID):
        sys.exit("JIRA_READ_EMAIL / JIRA_READ_TOKEN / JIRA_CLOUD_ID are not set (restart Claude Code after setting them).")
    auth = "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()

    try:
        if args.maid:
            return maid(auth)
        issue = json.loads(get(f"{API}/issue/{args.key}?fields=attachment,summary", auth))
    except urllib.error.HTTPError as e:
        sys.exit(f"{args.key or 'maid'}: HTTP {e.code} (401 = token expired or wrong email, 404 = no access or no such issue)")

    out = args.out or os.path.join(ROOT, args.key)
    os.makedirs(out, exist_ok=True)
    attachments = issue["fields"].get("attachment") or []
    print(f"{args.key}: {issue['fields']['summary']}")
    print(f"{len(attachments)} attachment(s) -> {out}")
    for att in sorted(attachments, key=lambda a: a["created"]):
        path = os.path.join(out, safe_name(att))
        if not (os.path.exists(path) and os.path.getsize(path) == att["size"]):
            with open(path, "wb") as f:
                f.write(get(f"{API}/attachment/content/{att['id']}", auth))
        print(f"{att['mimeType']}\t{att['size']}\t{att['created'][:16]}\t{att['author']['displayName']}\t{path}")


if __name__ == "__main__":
    main()
