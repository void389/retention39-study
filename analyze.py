"""Offline analysis of independently archived public pages."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent
DAY = 86400000


def wilson(k, n):
    if not 0 <= k <= n or n == 0:
        raise ValueError('Proportion needs a nonempty valid denominator')
    p, z = k / n, 1.959963984540054
    scale = 1 + z*z/n
    center = (p + z*z/(2*n)) / scale
    radius = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / scale
    return [max(0, center-radius), min(1, center+radius)]


def newcombe(k1, n1, k2, n2):
    p, q = k1/n1, k2/n2
    lo1, hi1 = wilson(k1, n1)
    lo2, hi2 = wilson(k2, n2)
    return [p-q-math.hypot(p-lo1, hi2-q), p-q+math.hypot(hi1-p, q-lo2)]


def retained(times, registered, start=7, stop=14):
    return any(registered+start*DAY <= t < registered+stop*DAY for t in times)


def summarize(cohort, activity, start=7, stop=14, censor=False):
    groups = {a: [0, 0] for a in ['door','sought','none']}
    for person in cohort:
        arm = person['arm']
        if censor and person['first_bind'] is not None and person['first_bind'] >= person['registered']+7*DAY:
            arm = 'none'
        k, n = groups[arm]
        groups[arm] = [k+int(retained(activity.get(person['handle'], []), person['registered'], start, stop)), n+1]
    out = {'arms': {a: {'retained': k, 'n': n, 'rate': k/n, 'wilson95': wilson(k,n)} for a,(k,n) in groups.items()}, 'differences': {}}
    for a,b in [('door','none'),('sought','door'),('sought','none')]:
        k,n = groups[a]; j,m = groups[b]
        out['differences'][a+'-'+b] = {'difference': k/n-j/m, 'newcombe95': newcombe(k,n,j,m)}
    return out


def run():
    dest = ROOT/'data'/'changes'
    state = json.loads((dest/'state.json').read_text())
    if any(v != 'done' for v in state['tokens'].values()):
        raise ValueError('Collection incomplete: refusing analysis')
    seen = {'posts':set(), 'comments':set()}
    activity = {}
    for entry in state['pages']:
        raw = (dest/entry['file']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('Archive hash mismatch')
        page = json.loads(raw)
        for stream in seen:
            for row in page[stream]:
                if row['id'] in seen[stream]:
                    raise ValueError('Duplicate activity row')
                seen[stream].add(row['id'])
                activity.setdefault(row['author'], []).append(row['created_at'])
    arms = json.loads((ROOT/'data'/'arms.json').read_text())
    before = json.loads((ROOT/'stats-before.json').read_text(encoding='utf-8-sig'))
    counts = {s:len(ids) for s,ids in seen.items()}
    totals = {s:before['society'][s] for s in seen}
    complete = counts == totals
    result = {'status':'complete' if complete else 'provisional: endpoint totals do not reconcile',
              'completeness': {'counts':counts,'stats_before':totals,
                               'equal_to_stats_before':complete,
                               'first_read_ms':state['pages'][0]['now'],
                               'last_read_ms':state['pages'][-1]['now'],
                               'pages':len(state['pages']), 'all_hashes_verified':True},
              'boundary':arms['boundary'],
              'primary':summarize(arms['cohort'],activity),
              'window_8_15':summarize([c for c in arms['cohort'] if c['registered']+15*DAY <= state['pages'][0]['now']],activity,8,15),
              'window_8_15_excluded_immature':sum(c['registered']+15*DAY > state['pages'][0]['now'] for c in arms['cohort']),
              'day7_censored_bind':summarize(arms['cohort'],activity,censor=True)}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    run()
