"""Search the cold skill/command catalog without loading recipe bodies."""
import argparse
import json
from pathlib import Path
import re


def search(root, query, limit=12):
    entries = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))['entries']
    words = re.findall(r'[\w-]+', query.casefold())
    ranked = []
    for entry in entries:
        name = entry['name'].casefold()
        haystack = (name + ' ' + entry['description']).casefold()
        score = sum(3 if word in name else 1 for word in words if word in haystack)
        if score or not words:
            ranked.append((score, entry))
    return [entry for _, entry in sorted(ranked, key=lambda item: (-item[0], item[1]['id']))[:limit]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error('--limit must be between 1 and 100')
    print(json.dumps(search(args.root, args.query, args.limit), ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
