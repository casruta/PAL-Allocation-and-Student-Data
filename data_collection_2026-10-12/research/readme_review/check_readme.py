"""Check documentation paths and unchanged evidence; no dataset transformations."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
doc=ROOT/'README.txt'
text=doc.read_text(encoding='utf-8-sig')
# Match complete relative paths containing the known research folders.
paths=sorted(set(re.findall(r'(?<![\w/])(?:analysis|scripts|research|raw|extracted|focus_2020_latest)/[A-Za-z0-9_./-]+',text)))
paths=sorted(set(p.rstrip('.') for p in paths))
missing=[p for p in paths if not (ROOT/p).exists()]
evidence_files=[
 'analysis/cleaned_file_inventory.csv','source_manifest.json',
 'analysis/validation_checks.json','analysis/notebook_execution.json',
 'analysis/pal_interpretation/notebook_execution.json',
 'analysis/cleaned/annual_enrolment_canada_alberta.csv',
 'analysis/cleaned/pal_before_after_event_matrix.csv',
 'analysis/cleaned/pal_university_utilization_evidence.csv',
 'raw/degree_detail/validation.json',
]
digests={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in evidence_files}
baseline=HERE/'evidence_hashes_before.json'
if not baseline.exists():baseline.write_text(json.dumps(digests,indent=2))
prior=json.loads(baseline.read_text())
result={'readme_sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),
 'word_count':len(text.split()),'referenced_path_count':len(paths),
 'paths_checked':paths,'missing_paths':missing,
 'changed_evidence_files':[p for p in digests if digests[p]!=prior[p]],
 'cleaned_csv_count':len(list((ROOT/'analysis/cleaned').glob('*.csv'))),
 'note':'Path/hash checks support, but do not replace, factual and editorial reviews.'}
(HERE/'latest_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
