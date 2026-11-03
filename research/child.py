"""Trusted-fixture worker. Resource limits are guardrails, NOT a security boundary."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import time


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    resource.setrlimit(resource.RLIMIT_AS, (192 * 1024**2, 192 * 1024**2))
    resource.setrlimit(resource.RLIMIT_FSIZE, (65536, 65536))
    resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
    resource.setrlimit(resource.RLIMIT_NPROC, (32, 32))
    root = Path(__file__).parent
    try:
        candidate = load('candidate', root / 'solution.py')
    except Exception as error:
        print(json.dumps({'status': 'build_failure', 'error': type(error).__name__}))
        return 2
    try:
        checks = load('checks', root / 'checks.py')
        names = sorted(n for n in vars(checks) if n.startswith(sys.argv[1] + '_'))
        if not names:
            raise ValueError('No tests collected')
    except Exception as error:
        print(json.dumps({'status': 'infrastructure_failure', 'error': type(error).__name__}))
        return 3
    results = []
    for name in names:
        start = time.monotonic()
        try:
            getattr(checks, name)(candidate)
            results.append({'name': name, 'passed': True, 'duration_ms': round((time.monotonic()-start)*1000, 3)})
        except Exception as error:
            results.append({'name': name, 'passed': False, 'error': type(error).__name__, 'message': str(error)[:500], 'duration_ms': round((time.monotonic()-start)*1000, 3)})
    print(json.dumps({'status': 'pass' if all(x['passed'] for x in results) else 'test_failure', 'tests': results}))
    return 0 if all(x['passed'] for x in results) else 1


if __name__ == '__main__':
    sys.exit(main())
