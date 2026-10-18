#!/usr/bin/env python3
"""Checks package structure and local Markdown link targets without mutation."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


class UniqueLoader(yaml.SafeLoader):
    """Rejects duplicate mapping keys instead of silently replacing values."""


def unique_mapping(loader, node):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in mapping:
            raise ValueError(f'duplicate YAML key: {key}')
        mapping[key] = loader.construct_object(value_node)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_mapping(text):
    value = yaml.load(text, Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError('expected a YAML mapping')
    return value


def markdown_prose(text):
    """Removes fenced examples before inspecting Markdown links."""
    output = []
    fence = None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not match[2].strip():
                fence = None
            continue
        if fence is None:
            output.append(line)
    return re.sub(r'(`+)(.+?)\1', '', '\n'.join(output))


def validate(root: Path) -> list[str]:
    errors = []
    required = ('SKILL.md', 'agents/openai.yaml', 'README.md', 'README.zh-CN.md',
                'CONTRIBUTING.md', 'CONTRIBUTING.zh-CN.md', 'LICENSE',
                'scripts/pr-analyzer.py', 'assets/review-checklist.md',
                'assets/pr-review-template.md')
    for name in required:
        if not (root / name).is_file():
            errors.append(f'missing package file: {name}')
    if not list((root / 'reference').glob('*.md')):
        errors.append('missing reference guides')
    try:
        skill = (root / 'SKILL.md').read_text(encoding='utf-8')
        front = re.match(r'\A---\n(.*?)\n---(?:\n|$)', skill, re.S)
        if not front:
            raise ValueError('missing or malformed frontmatter')
        metadata = load_mapping(front[1])
        if metadata.get('name') != 'code-review-codex':
            errors.append('skill name differs from package identity code-review-codex')
        allowed = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
        if set(metadata) - allowed:
            errors.append('unsupported frontmatter keys')
        description = metadata.get('description')
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append('description must be non-empty text of at most 1024 characters')
        interface = load_mapping((root / 'agents/openai.yaml').read_text(encoding='utf-8')).get('interface')
        if not isinstance(interface, dict):
            raise ValueError('interface must be a mapping')
        if interface.get('display_name') != 'Code Review Codex':
            errors.append('display_name differs from package identity Code Review Codex')
        short = interface.get('short_description')
        if not isinstance(short, str) or not short.strip() or len(short) > 64:
            errors.append('short_description must contain 1–64 characters')
    except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
        errors.append(f'metadata: {error}')
    for path in sorted(root.rglob('*.md')):
        relative = path.relative_to(root)
        if any(part.startswith('.') for part in relative.parts):
            continue
        try:
            prose = markdown_prose(path.read_text(encoding='utf-8'))
            targets = re.findall(r'\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"\n]*")?\)', prose)
            targets += re.findall(r'^\s{0,3}\[[^\]\n]+\]:\s*(<[^>]+>|\S+)', prose, re.M)
            for target in targets:
                url = urlsplit(target.strip('<>'))
                if url.scheme or url.netloc or not url.path:
                    continue
                destination = (path.parent / unquote(url.path)).resolve()
                if not destination.is_relative_to(root) or not destination.exists():
                    errors.append(f'{relative}: missing or out-of-package link: {target}')
        except (OSError, ValueError) as error:
            errors.append(f'{relative}: {error}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('Skill structure and local link targets are valid (review quality is not evaluated).')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
