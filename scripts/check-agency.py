#!/usr/bin/env python3
"""Validate agency wiring, knowledge integrity and website review routing."""
from pathlib import Path
import hashlib
import json
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def check_website_review():
    rubric = 'knowledge/quality/acceptance.md'
    weights = [
        ('Visuele identiteit en originaliteit', 20),
        ('UX en gebruiksvriendelijkheid', 20),
        ('Visuele afwerking en consistentie', 15),
        ('Mobiele ervaring', 15),
        ('Technische kwaliteit', 15),
        ('Performance en toegankelijkheid', 10),
        ('Content en SEO', 5),
    ]
    text = (ROOT / rubric).read_text()
    rows = re.findall(r'^\| ([^|]+) \| (\d+)% \|', text, re.M)
    assert [(criterion, int(weight)) for criterion, weight in rows] == weights, 'Website rubric mismatch'
    assert '8,5/10' in text, 'Missing website quality target'
    for entry in (
        'AGENTS.md',
        '.agents/skills/agency-delivery/SKILL.md',
        '.agents/skills/quality-review/SKILL.md',
        'agency/rules/quality.md',
        'templates/quality-review.md',
        '.codex/agents/critical_reviewer.toml',
        '.codex/agents/qa_security_lead.toml',
    ):
        assert rubric in (ROOT / entry).read_text(), f'Missing website review routing: {entry}'


def check():
    matrix = []
    for line in (ROOT / 'knowledge/agent-matrix.md').read_text().splitlines():
        if line.startswith('| ') and not line.startswith('| Rol'):
            cells = [part.strip() for part in line.strip('|').split('|')]
            matrix.append(cells[0])
    registry = json.loads((ROOT / 'agency/agents.json').read_text())
    config = tomllib.loads((ROOT / '.codex/config.toml').read_text())
    assert config['agents']['max_concurrent_threads_per_session'] == 2, 'Expected at most two configured subagent threads'
    assert config['agents']['max_depth'] == 1, 'Nested delegation must be disabled'
    roles = {key: value for key, value in config['agents'].items() if isinstance(value, dict)}
    assert len(matrix) == len(registry) == len(roles) == 22, 'Expected exactly 22 roles'
    assert [r['name'] for r in registry] == matrix, 'Role matrix mismatch'
    ids = {r['id'] for r in registry}
    assert len(ids) == 22 and ids == set(roles), 'Duplicate or missing roles'
    leads = {'creative_lead', 'technical_team_lead', 'qa_security_lead', 'operations_lead'}
    assert {r['id'] for r in registry if r['parent'] == 'agency_manager'} == leads
    assert sum(r['parent'] in leads for r in registry) == 17
    assert next(r for r in registry if r['id'] == 'agency_manager')['parent'] == 'owner'
    for role in registry:
        path = ROOT / '.codex' / roles[role['id']]['config_file']
        assert path.resolve() == (ROOT / role['config']).resolve()
        instruction = tomllib.loads(path.read_text())['developer_instructions']
        assert role['name'] in instruction and role['parent'] in instruction
        assert 'agency/rules/efficiency.md' in instruction, 'Role missing efficiency policy'
        for doc in role['knowledge']:
            assert (ROOT / doc).is_file(), f'Missing knowledge: {doc}'
            assert doc in instruction, f'Unwired knowledge: {doc}'
        assert 'model' not in tomllib.loads(path.read_text()), 'Do not override models'
    baseline = json.loads((ROOT / 'agency/knowledge-baseline.json').read_text())
    actual = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (ROOT / 'knowledge').rglob('*') if p.is_file()}
    assert actual == baseline, 'Knowledge differs from the recorded baseline'
    for name in ['core', 'task-interpretation', 'delegation', 'quality', 'github', 'efficiency', 'preview', 'design-preferences']:
        assert (ROOT / f'agency/rules/{name}.md').is_file()
    skills = list((ROOT / '.agents/skills').glob('*/SKILL.md'))
    assert len(skills) == 4
    for skill in skills:
        text = skill.read_text()
        assert text.startswith('---\n') and re.search(r'^name: .+', text, re.M)
        assert re.search(r'^description: .+', text, re.M)
        assert len(text.split('---', 2)[-1].strip()) > 100
    for name in ['task-brief', 'architecture-demo', 'quality-review', 'delivery']:
        assert (ROOT / f'templates/{name}.md').is_file()
    check_website_review()
    print(f'PASS: {len(roles)} roles, 4 leads, 17 specialists, {len(baseline)} verified knowledge files, 4 skills, 4 templates, website review routing and rubric')


if __name__ == '__main__':
    check()
