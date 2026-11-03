"""Allowlisted, hash-verified trusted fixtures only. Arbitrary patches are disabled."""
import argparse
import ast
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
TASK_IDS = ('SEC-411', 'DB-307', 'FILE-101')
CANDIDATES = ('reference', 'faulty', 'regression')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def task_spec(task_id):
    if task_id not in TASK_IDS:
        raise ValueError('Unknown task; arbitrary file paths are not accepted')
    directory = ROOT / 'benchmarks' / task_id
    spec = json.loads((directory / 'task.json').read_text())
    for name, expected in spec['sha256'].items():
        if Path(name).name != name or (directory / name).is_symlink():
            raise ValueError('Invalid fixture path')
        if digest((directory / name).read_bytes()) != expected:
            raise ValueError('Fixture hash mismatch; review the change before updating its manifest')
    return spec


def materialize(task_id, candidate_id, destination):
    if candidate_id not in CANDIDATES:
        raise ValueError('Untrusted candidates disabled; choose a bundled fixture')
    spec = task_spec(task_id)
    directory = ROOT / 'benchmarks' / task_id
    # Replacement patch format is constrained to solution.py and an allowlisted hash.
    shutil.copyfile(directory / spec['baseline'], destination / 'solution.py')
    candidate = directory / spec['candidates'][candidate_id]['file']
    (destination / 'solution.py').write_bytes(candidate.read_bytes())
    shutil.copyfile(directory / spec['checks'], destination / 'checks.py')
    shutil.copyfile(ROOT / 'research' / 'child.py', destination / 'child.py')
    return spec


def run_group(task_id, candidate_id, group):
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='agentbench-') as temporary:
        directory = Path(temporary)
        materialize(task_id, candidate_id, directory)
        try:
            ast.parse((directory / 'solution.py').read_text())
        except SyntaxError as error:
            return {'status': 'build_failure', 'exit_code': None, 'tests': [], 'log': str(error)[:1000], 'duration_ms': 0}
        with (directory / 'output.log').open('wb') as output:
            process = subprocess.Popen([sys.executable, '-I', str(directory / 'child.py'), group], cwd=directory, env={'PATH': os.defpath, 'LANG': 'C.UTF-8'}, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                exit_code = process.wait(timeout=5)
                timeout = False
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                exit_code, timeout = process.returncode, True
        with (directory / 'output.log').open('rb') as log_file:
            raw = log_file.read(32768).decode(errors='replace')
        if timeout:
            result = {'status': 'timeout', 'tests': []}
        elif exit_code < 0:
            result = {'status': 'resource_exhaustion', 'tests': []}
        else:
            try:
                result = json.loads(raw)
                if not isinstance(result, dict) or result.get('status') not in {'pass', 'test_failure', 'build_failure', 'infrastructure_failure'}:
                    raise ValueError('Malformed result')
            except (ValueError, TypeError):
                result = {'status': 'infrastructure_failure', 'tests': []}
        return {**result, 'exit_code': exit_code, 'duration_ms': round((time.monotonic()-started)*1000, 2), 'log': raw[:4000], 'log_truncated': (directory/'output.log').stat().st_size > 4000}


def evaluate(task_id, candidate_id, label='synthetic-fixture', repeat=1):
    if os.name != 'posix':
        raise RuntimeError('Trusted runner requires POSIX resource controls; use Linux or macOS')
    if len(label) > 100:
        raise ValueError('Label too long')
    spec = task_spec(task_id)
    if candidate_id not in CANDIDATES:
        raise ValueError('Untrusted candidates disabled')
    groups = {name: run_group(task_id, candidate_id, name) for name in ('visible', 'security', 'regression')}
    categories = []
    for group, result in groups.items():
        if result['status'] == 'test_failure':
            categories.append({'visible': 'correctness_failure', 'security': 'security_failure', 'regression': 'regression_failure'}[group])
        elif result['status'] != 'pass':
            categories.append(result['status'])
    candidate_file = ROOT/'benchmarks'/task_id/spec['candidates'][candidate_id]['file']
    source = candidate_file.read_text()
    warnings = ['Long source line (>100 characters)'] if any(len(line)>100 for line in source.splitlines()) else []
    return {'task_id': task_id, 'title': spec['title'], 'candidate_id': candidate_id, 'label': label, 'repeat': repeat, 'provenance': 'synthetic, locally authored fixture; not a real model evaluation', 'benchmark_version': spec['benchmark_version'], 'candidate_sha256': digest(source.encode()), 'fixture_sha256': spec['sha256'], 'manifest_sha256': digest((ROOT/'benchmarks'/task_id/'task.json').read_bytes()), 'runner_sha256': digest(Path(__file__).read_bytes()), 'worker_sha256': digest((ROOT/'research'/'child.py').read_bytes()), 'groups': groups, 'failure_categories': sorted(set(categories)), 'maintainability_warnings': warnings, 'release_ready': not categories, 'mode': 'trusted_fixture_only', 'isolation': 'POSIX subprocess guardrails; not a malicious-code sandbox', 'observed_at': datetime.now(timezone.utc).isoformat(), 'environment': {'python': platform.python_version(), 'platform': platform.platform(), 'cpu_seconds':2, 'memory_mb':192, 'wall_seconds_per_group':5, 'network_isolated': False, 'arbitrary_execution_enabled':False}}


def compare(task_ids=TASK_IDS, candidates=CANDIDATES, repeats=1, label='synthetic-fixture'):
    if not 1 <= repeats <= 10:
        raise ValueError('repeats must be 1..10')
    runs = [evaluate(task, candidate, label, repeat) for task in task_ids for candidate in candidates for repeat in range(1, repeats+1)]
    summary = {}
    for group in ('visible', 'security', 'regression'):
        known = [r['groups'][group] for r in runs if r['groups'][group]['status'] in ('pass','test_failure')]
        tests = [t for g in known for t in g['tests']]
        summary[group] = {'evaluated_runs':len(known), 'unavailable_runs':len(runs)-len(known), 'failed_runs':sum(g['status']=='test_failure' for g in known), 'tests':len(tests), 'passed_tests':sum(t['passed'] for t in tests)}
    return {'schema_version':1,'project':'AgentBench Research Edition','data_kind':'executed synthetic fixtures','generated_at':datetime.now(timezone.utc).isoformat(),'summary':summary,'tasks':[task_spec(t) for t in task_ids], 'runs':runs}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task', choices=TASK_IDS, action='append')
    parser.add_argument('--candidate', choices=CANDIDATES, action='append')
    parser.add_argument('--repeats',type=int,default=1)
    parser.add_argument('--label',default='synthetic-fixture')
    parser.add_argument('--output',type=Path,default=ROOT/'frontend/public/data/benchmark.json')
    args=parser.parse_args()
    report=compare(args.task or TASK_IDS,args.candidate or CANDIDATES,args.repeats,args.label)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    with args.output.with_suffix('.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['task_id','candidate_id','repeat','visible','security','regression','release_ready','failure_categories'])
        for r in report['runs']:
            w.writerow([r['task_id'],r['candidate_id'],r['repeat'],*[r['groups'][g]['status'] for g in ('visible','security','regression')],r['release_ready'],';'.join(r['failure_categories'])])
    print(json.dumps({'runs':len(report['runs']),'summary':report['summary'],'output':str(args.output)},indent=2))

if __name__ == '__main__': main()
