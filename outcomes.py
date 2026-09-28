"""Resumable anonymous ID-mode changes walk. No external writes or credentials."""
import hashlib
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).parent


def advance(page, tokens):
    if not set(page['has_more_streams']).issubset(page['continuation_covers']):
        raise ValueError('Continuation does not cover all streams')
    result = {}
    for stream in ('posts', 'comments'):
        token = page[f'next_{stream}_since']
        if tokens[stream] == 'done':
            result[stream] = 'done'
        elif token.startswith('id:'):
            # Snapshot drained. Do not chase new activity while the other drains.
            result[stream] = 'done'
        elif token.startswith('snapi:') and token != tokens[stream]:
            result[stream] = token
        else:
            raise ValueError('Invalid or non-advancing cursor')
    return result


def run():
    dest = ROOT / 'data' / 'changes'
    dest.mkdir(parents=True, exist_ok=True)
    statefile = dest / 'state.json'
    state = json.loads(statefile.read_text()) if statefile.exists() else {
        'tokens': {'posts': 'init', 'comments': 'init'}, 'pages': []}
    while any(t != 'done' for t in state['tokens'].values()):
        params = {'since': 0, 'nulls_since': 'done',
                  **{k + '_since': v for k, v in state['tokens'].items()}}
        url = 'https://1f916.ai/api/changes?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={'User-Agent': 'independent-retention-audit/1'})
        with urllib.request.urlopen(req, timeout=45) as response:
            raw = response.read()
        page = json.loads(raw)
        tokens = advance(page, state['tokens'])
        name = f"{len(state['pages']):04}.json"
        (dest / name).write_bytes(raw)
        state['pages'].append({'file': name, 'url': url, 'sha256': hashlib.sha256(raw).hexdigest(),
                               'now': page['now'], 'counts': page['rows_returned'],
                               'has_more': page['has_more'],
                               'next_posts_since': page['next_posts_since'],
                               'next_comments_since': page['next_comments_since']})
        state['tokens'] = tokens
        temp = dest / 'state.tmp'
        temp.write_text(json.dumps(state, indent=2), encoding='utf8')
        temp.replace(statefile)
        if len(state['pages']) % 20 == 0:
            print(f"Archived {len(state['pages'])} pages", flush=True)
        time.sleep(1)
    print(f"Snapshot drained: {len(state['pages'])} pages", flush=True)


if __name__ == '__main__':
    run()
