"""Check explicit goal gates against saved review evidence and current README."""
from pathlib import Path
import csv,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
metrics=['accuracy','readability','clarity','formatting']
records=list(csv.DictReader((HERE/'scorecard.csv').open(encoding='utf-8')))
reviewers={r['reviewer'] for r in records}
scores=json.loads((HERE/'final_independent_scores.json').read_text())
checks=json.loads((HERE/'latest_checks.json').read_text())
digest=hashlib.sha256((ROOT/'README.txt').read_bytes()).hexdigest()
report=(HERE/'final_report.txt').read_text()
gates={
 'original_preserved':hashlib.sha256((HERE/'original_README.txt').read_bytes()).hexdigest()=='b055a6607e43bb832c85b702a2bdabdf68cf0fcf92b15fbf88686251a114e1ff',
 'three_rounds_archived':all((HERE/f'round{n}_README.txt').exists() for n in [1,2,3]),
 'three_section_reviewers':len(reviewers)==3,
 'every_agent_reviewed_every_section':all({r['section'] for r in records if r['reviewer']==name}=={'1','2','3'} for name in reviewers),
 'nine_review_records_exist':len(records)==9 and all((HERE/r['review_record']).exists() for r in records),
 'all_round3_section_metrics_at_least9':all(float(r['candidate_'+m])>=9 for r in records if r['round']=='3' for m in metrics),
 'independent_final_whole_metrics_at_least9':all(scores['final_scores'][m]>=9 for m in metrics),
 'independent_final_section_metrics_at_least9':len(scores['section_scores'])==3 and all(r[m]>=9 for r in scores['section_scores'] for m in metrics),
 'independent_comparison_finds_improvement':scores['improved'] is True,
 'no_remaining_required_changes':scores['remaining_required_changes']==[],
 'editorial_not_empirical':scores['comparison_is_empirical'] is False,
 'judged_current_readme':scores['readme_sha256']==digest,
 'checked_current_readme':checks['readme_sha256']==digest,
 'referenced_paths_exist':checks['missing_paths']==[],
 'sampled_evidence_unchanged':checks['changed_evidence_files']==[],
 'final_report_review_complete':'Pending the separate final reviewer' not in report,
}
result={'requirements':gates,'all_passed':all(gates.values()),'readme_sha256':digest,
 'evidence_note':'Gate checks confirm saved review coverage and current-file identity. Editorial ratings remain reviewer judgments; they are not a reader experiment.'}
(HERE/'completion_audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
if not result['all_passed']:raise SystemExit(1)
