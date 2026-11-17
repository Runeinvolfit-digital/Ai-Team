#!/usr/bin/env python3
"""Validate agency wiring and preservation; never claim live agent activation."""
from pathlib import Path
import hashlib
import json
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def check():
    matrix = []
    for line in (ROOT / 'knowledge/agent-matrix.md').read_text().splitlines():
        if line.startswith('| ') and not line.startswith('| Rol'):
            cells = [part.strip() for part in line.strip('|').split('|')]
            matrix.append(cells[0])
    registry = json.loads((ROOT / 'agency/agents.json').read_text())
    config = tomllib.loads((ROOT / '.codex/config.toml').read_text())
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
        for doc in role['knowledge']:
            assert (ROOT / doc).is_file(), f'Missing knowledge: {doc}'
            assert doc in instruction, f'Unwired knowledge: {doc}'
        assert 'model' not in tomllib.loads(path.read_text()), 'Do not override models'
    baseline = json.loads((ROOT / 'agency/knowledge-baseline.json').read_text())
    actual = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (ROOT / 'knowledge').rglob('*') if p.is_file()}
    assert actual == baseline, 'Existing knowledge changed, missing, or added'
    for name in ['core', 'task-interpretation', 'delegation', 'quality', 'github']:
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
    print(f'PASS: {len(roles)} roles, 4 leads, 17 specialists, {len(baseline)} unchanged knowledge files, 4 skills, 4 templates')


if __name__ == '__main__':
    check()
