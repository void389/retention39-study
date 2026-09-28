"""Independent public-data arm audit; does not estimate retention or submit work."""
import hashlib
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request

BASE = 'https://1f916.ai/api/'


def collect(endpoint, array, out, extra=None):
    rows, seen, cursors, manifest = [], set(), set(), []
    cursor = 0
    out.mkdir(parents=True, exist_ok=True)
    while True:
        if cursor in cursors:
            raise ValueError('Repeated pagination cursor')
        cursors.add(cursor)
        url = BASE + endpoint + '?' + urllib.parse.urlencode({'since': cursor, **(extra or {})})
        request = urllib.request.Request(url, headers={'User-Agent': 'independent-retention-audit/1'})
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
        page = json.loads(raw)
        name = f'{endpoint}-{len(manifest):04}.json'
        (out / name).write_bytes(raw)
        manifest.append({'url': url, 'file': name, 'sha256': hashlib.sha256(raw).hexdigest(),
                         'total': page['total'], 'has_more': page['has_more']})
        (out / f'{endpoint}-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf8')
        for row in page[array]:
            identity = row['citizen_id'] if array == 'citizens' else row['id']
            if identity in seen:
                raise ValueError('Duplicate row ID; census cannot be certified')
            seen.add(identity)
            rows.append(row)
        if not page['has_more']:
            if len(rows) != page['total']:
                raise ValueError(f"Incomplete {endpoint}: {len(rows)} != {page['total']}")
            return rows
        cursor = page['next_since']
        time.sleep(1)


def assign(citizens, events, start, cutoff):
    first = {}
    for event in events:
        if event['kind'] == 'key-bind':
            cid = event['citizen_id']
            first[cid] = min(first.get(cid, event['created_at']), event['created_at'])
    delays = sorted(set(first[c['citizen_id']] - c['created_at'] for c in citizens
                        if c['citizen_id'] in first and first[c['citizen_id']] > c['created_at']))
    if len(delays) < 2:
        raise ValueError('Insufficient positive bind delays')
    low, high = max(zip(delays, delays[1:]), key=lambda pair: pair[1] / pair[0])
    cohort = []
    for c in citizens:
        if not start <= c['created_at'] < cutoff:
            continue
        bind = first.get(c['citizen_id'])
        delay = None if bind is None else bind - c['created_at']
        if delay is not None and delay < 0:
            raise ValueError('Key bind precedes registration')
        arm = 'none' if delay is None else ('door' if delay <= low else 'sought')
        cohort.append({'id': c['citizen_id'], 'handle': c['handle'],
                       'registered': c['created_at'], 'first_bind': bind, 'arm': arm})
    return {'boundary': {'low_ms': low, 'high_ms': high, 'ratio': high / low}, 'cohort': cohort}


if __name__ == '__main__':
    from datetime import datetime
    stamp = lambda value: int(datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp() * 1000)
    out = Path(__file__).parent / 'data'
    citizens = collect('citizens', 'citizens', out)
    events = collect('events', 'events', out, {'kind': 'key-bind'})
    result = assign(citizens, events, stamp('2026-08-12T21:33:32Z'), stamp('2026-09-12T00:00:00Z'))
    (out / 'arms.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps({'citizens': len(citizens), 'bind_events': len(events),
                      'boundary': result['boundary'],
                      'arms': {a: sum(c['arm'] == a for c in result['cohort']) for a in ['door', 'sought', 'none']}}))
