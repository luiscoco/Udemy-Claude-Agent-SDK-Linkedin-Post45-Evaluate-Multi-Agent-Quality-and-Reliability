"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    records = []
    for case in data['cases']:
        try:
            grade = await agent.ask('grade_' + case['id'], 'Is this a useful nonempty explanation? Return accepted and reason.', case['text'],
                                    {'accepted': bool(case['text'].strip()), 'reason': 'Check for substantive content.'})
            records.append({'id': case['id'], 'correct': grade['accepted'] == case['expected'], 'error': False})
        except Exception:
            records.append({'id': case['id'], 'correct': False, 'error': True})
    n = len(records)
    if not n:
        raise ValueError('At least one case is required')
    return {'records': records, 'accuracy': sum(r['correct'] for r in records) / n,
            'execution_error_rate': sum(r['error'] for r in records) / n, 'denominator': n}
