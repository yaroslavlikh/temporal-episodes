"""Read-only verification of the preprint's experimental inputs. No API imports.

Writes only a new editorial report beside this file. Existing run files are
hashed before and after inspection and never opened for writing.
"""
import collections
import hashlib
import json
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = HERE.parents[1] / '.research_runs'
INPUTS = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    path = RUNS / path
    INPUTS[path] = digest(path)
    return json.loads(path.read_text()) if path.suffix == '.json' else [
        json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def arm(rows, condition):
    result = {r['qa_key']: r for r in rows if r['condition'] == condition}
    assert len(result) == sum(r['condition'] == condition for r in rows)
    return result


def main():
    original = read('evermembench_temporal_episodes_official_v1/results.jsonl')
    events = read('final_sprint_A_events_full_v1/results.jsonl')
    arms = {'RAW': arm(original, 'RAW'), 'EVENTS': arm(events, 'RAW+EVENTS'),
            'EPISODES': arm(original, 'RAW+EPISODES')}
    preds = read('evermembench_temporal_episodes_official_v1/predictions.jsonl')
    event_preds = read('final_sprint_A_events_full_v1/predictions.jsonl')
    predictions = {'RAW': arm(preds, 'RAW'), 'EVENTS': arm(event_preds, 'RAW+EVENTS'),
                   'EPISODES': arm(preds, 'RAW+EPISODES')}
    gold = {}
    for topic in ('01', '02', '03', '04', '05'):
        for row in read(f'official_sources/EverMemBench-Dynamic/{topic}/qa_{topic}.json'):
            sources = set()
            for ref in row.get('R', []):
                for part in str(ref.get('message_index', '')).split(','):
                    part = part.strip()
                    match = re.fullmatch(r'(\d+)\s*-\s*(\d+)', part)
                    indexes = range(int(match[1]), int(match[2]) + 1) if match else ([int(part)] if part.isdigit() else [])
                    sources.update(f"{topic}|{ref['date']}|{ref['group']}|{index}" for index in indexes)
            gold[f"{topic}:{row['id']}"] = sources
    keys = sorted(gold)
    assert len(keys) == 2400
    report = {'ever': {}, 'same_sources_without_derived': 'B1 prepared; no completed artifacts found'}
    for name, rows in arms.items():
        assert set(rows) == set(gold) == set(predictions[name])
        counts, hits, correct_without = [], [], 0
        for key in keys:
            exposed = set(predictions[name][key]['exposed_source_ids'])
            overlap = len(exposed & gold[key])
            precision = overlap / len(exposed) if exposed else 0.
            recall = overlap / len(gold[key]) if gold[key] else 1.
            assert abs(precision - rows[key]['evidence_precision']) < 1e-12
            assert abs(recall - rows[key]['evidence_recall']) < 1e-12
            counts.append(len(exposed)); hits.append(overlap)
            correct_without += bool(rows[key]['correct']) and overlap == 0
        categories = collections.defaultdict(list)
        for row in rows.values():
            categories[row['minor']].append(row['correct'])
        report['ever'][name] = {
            'n': len(rows), 'micro': np.mean([r['correct'] for r in rows.values()]),
            'macro': np.mean([np.mean(v) for v in categories.values()]),
            'precision': np.mean([r['evidence_precision'] for r in rows.values()]),
            'recall': np.mean([r['evidence_recall'] for r in rows.values()]),
            'sources': np.mean(counts), 'gold_hits': np.mean(hits),
            'correct_with_zero_gold_hits': int(correct_without)}
    lengths = [len(gold[k]) for k in keys]
    report['gold_anchor_counts'] = {'min': min(lengths), 'median': float(np.median(lengths)),
                                   'mean': float(np.mean(lengths)), 'max': max(lengths),
                                   'q25_q75': np.quantile(lengths, [.25, .75]).tolist()}
    report['project_effects'] = []
    for topic in ('01', '02', '03', '04', '05'):
        ks = [k for k in keys if arms['RAW'][k]['topic'] == topic]
        report['project_effects'].append({'topic': topic, 'n': len(ks), **{
            f'delta_{field}_pp': 100 * np.mean([arms['EVENTS'][k][field] - arms['RAW'][k][field] for k in ks])
            for field in ('evidence_precision', 'evidence_recall', 'correct')}})
    report['leave_one_project_out_precision_pp'] = [
        float(100 * np.mean([arms['EVENTS'][k]['evidence_precision'] - arms['RAW'][k]['evidence_precision']
                             for k in keys if arms['RAW'][k]['topic'] != topic]))
        for topic in ('01', '02', '03', '04', '05')]
    report['accuracy_by_category'] = {
        category: {name: float(np.mean([row['correct'] for row in rows.values()
                                       if row['minor'] == category]))
                   for name, rows in arms.items()}
        for category in sorted({row['minor'] for row in arms['RAW'].values()})}
    social = read('frozen/socialmembench_full_official_v1_20260911_184037_MSK/run/results.jsonl')
    social += read('socialmembench_temporal_episodes_official_harness_v1/episode_results.jsonl')
    raw = arm(social, 'RAW')
    report['social_network_bootstrap'] = {}
    networks = sorted({r['network_id'] for r in raw.values()})
    assert len(raw) == 1031 and len(networks) == 43
    for condition in ('RAW+FLAT', 'RAW+VERSIONED', 'RAW+EPISODES'):
        other = arm(social, condition)
        assert set(raw) == set(other)
        totals = np.array([[sum(other[k]['evidence_precision'] - raw[k]['evidence_precision']
                                for k in raw if raw[k]['network_id'] == net),
                            sum(raw[k]['network_id'] == net for k in raw)] for net in networks])
        draws = np.random.default_rng(20260917).integers(43, size=(10000, 43))
        sampled = totals[draws].sum(axis=1)
        report['social_network_bootstrap'][condition] = {
            'delta_precision_pp': float(100 * totals[:, 0].sum() / totals[:, 1].sum()),
            'ci_pp': (100 * np.quantile(sampled[:, 0] / sampled[:, 1], [.025, .975])).tolist()}
    group_gold = []
    for path in sorted((RUNS / 'official_sources/GroupMemBench/questions').rglob('*.jsonl')):
        group_gold.extend(read(str(path.relative_to(RUNS))))
    fields = collections.Counter(key for row in group_gold for key in row)
    assert len(group_gold) == 745 and set(fields) == {'id', 'question', 'answer', 'asking_user_id'}
    repaired = read('final_sprint_D_groupmembench_repair_v2/predictions_v2.jsonl')
    previous = read('groupmembench_temporal_episodes_official_v1/predictions.jsonl')
    prev = {(r['qa_key'], r['condition']): r for r in previous}
    assert len(prev) == len(repaired) == 1490
    unchanged = 0
    for row in repaired:
        old = prev[(row['qa_key'], row['condition'])]
        if old['answer'].strip():
            assert row['answer'] == old['answer']; unchanged += 1
        assert row['answer'].strip()
        assert row['exposed_source_ids'] == old['exposed_source_ids']
    assert unchanged == 1388
    group_source_ids = set()
    for domain in ('Finance', 'Technology', 'Healthcare', 'Manufacturing'):
        channels = read(f'official_sources/GroupMemBench/data/final/{domain}/synthetic_domain_channels_rolevariants_{domain}.json')
        for messages in channels.values():
            group_source_ids.update(f"{domain}|{message['msg_node']}" for message in messages)
    assert len(group_source_ids) == 120000
    exposed_ids = {source for row in repaired for source in row['exposed_source_ids']}
    assert exposed_ids <= group_source_ids
    group_results = read('final_sprint_D_groupmembench_repair_v2/results_v2.jsonl')
    report['group'] = {'gold_fields': dict(fields), 'evidence_gap': 'No gold source IDs or spans in all 745 QA; recall/precision undefined',
                       'unchanged_answers': unchanged, 'repaired_answers': 1490 - unchanged,
                       'exposed_ids_valid': len(exposed_ids), 'corpus_source_ids': len(group_source_ids),
                       'accuracy': {cond: float(np.mean([r['correct'] for r in group_results if r['condition'] == cond]))
                                    for cond in ('RAW', 'RAW+EPISODES')}}
    for dirname, results_name, predictions_name in (
        ('evermembench_temporal_episodes_official_v1', 'results', 'predictions'),
        ('final_sprint_A_events_full_v1', 'results', 'predictions'),
        ('final_sprint_D_groupmembench_repair_v2', 'results_v2', 'predictions_v2')):
        for stem in (results_name, predictions_name):
            meta = read(f'{dirname}/{stem}_meta.json')
            path = RUNS / dirname / f'{stem}.jsonl'
            assert digest(path) == meta['sha256']
    report['temporal_accuracy'] = {}
    for dirname in ('evermembench_temporal_budget_control_v1',
                    'evermembench_unlinked_events_control_v1',
                    'evermembench_chronological_order_control_v2',
                    'final_sprint_B2_episodes_chrono_v1',
                    'final_sprint_C_hyde_raw_v1', 'final_sprint_C2_hyde_token_matched_v1'):
        rows = read(f'{dirname}/results.jsonl')
        for condition in sorted({r['condition'] for r in rows}):
            selected = [r for r in rows if r['condition'] == condition]
            assert len(selected) == 300
            report['temporal_accuracy'][condition] = float(np.mean([r['correct'] for r in selected]))
    chronological = read('evermembench_chronological_order_control_v2/predictions.jsonl')
    budgets = {
        'RAW': arm(chronological, 'RAW-token-matched-chrono'),
        'EVENTS': arm(chronological, 'RAW+EVENTS-token-matched-chrono'),
        'HyDE': arm(read('final_sprint_C2_hyde_token_matched_v1/predictions.jsonl'),
                    'HyDE-RAW-token-matched-chrono'),
        'EPISODES': arm(read('final_sprint_B2_episodes_chrono_v1/predictions.jsonl'),
                        'RAW+EPISODES-chrono')}
    report['token_matching'] = {'encoding': 'o200k_base', 'context_only': True,
                                'conditions': {}, 'comparisons': {}}
    for name, rows in budgets.items():
        tokens = np.array([r['context_tokens'] for r in rows.values()])
        assert len(rows) == 300 and np.all(tokens > 0)
        report['token_matching']['conditions'][name] = {
            'n': len(rows), 'mean': float(tokens.mean()), 'median': float(np.median(tokens)),
            'min': int(tokens.min()), 'max': int(tokens.max())}
    for left, right in (('RAW', 'EPISODES'), ('EVENTS', 'EPISODES'),
                        ('HyDE', 'EVENTS'), ('EVENTS', 'RAW'), ('EVENTS', 'HyDE')):
        a, b = budgets[left], budgets[right]
        assert set(a) == set(b)
        ks = sorted(a)
        signed = np.array([a[k]['context_tokens'] - b[k]['context_tokens'] for k in ks])
        absolute = np.abs(signed)
        relative = 100 * absolute / np.array([b[k]['context_tokens'] for k in ks])
        report['token_matching']['comparisons'][f'{left} - {right}'] = {
            'n': len(ks), 'median_signed': float(np.median(signed)),
            'median_abs': float(np.median(absolute)),
            'iqr_abs': np.quantile(absolute, [.25, .75]).tolist(),
            'p95_abs': float(np.quantile(absolute, .95)), 'max_abs': int(absolute.max()),
            'median_abs_percent': float(np.median(relative)),
            'p95_abs_percent': float(np.quantile(relative, .95)),
            'max_abs_percent': float(relative.max())}
    for path, before in INPUTS.items():
        assert digest(path) == before, path
    report['inputs_sha256'] = {str(p.relative_to(RUNS)): value for p, value in INPUTS.items()}
    report['verification'] = 'All read inputs unchanged; exact gold intersections independently verified; no API calls'
    (HERE / 'editorial_verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False, default=float) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'inputs_sha256'}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
