"""Consolidate independent ATIP provenance and validate all retained originals."""
from pathlib import Path
import json,csv,hashlib,zipfile
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'source_manifest.json';rows=json.loads(p.read_text(encoding='utf-8'))
prov=json.loads((ROOT/'research/atip/provenance.json').read_text(encoding='utf-8-sig'))
extra=[dict(source_id='ati_bulk_summaries',title=prov['source_name'],url=prov['source_url'],local_path=prov['raw_relative_path'],metric_type='completed_request_metadata_only',notes=prov['limitations'],retrieved_at_utc=prov['collected_date_utc'],status='downloaded',bytes=prov['raw_bytes'],sha256=prov['raw_sha256'])]
for r in json.loads((ROOT/'research/atip/record_download_receipts.json').read_text(encoding='utf-8-sig')):
    extra.append(dict(source_id='ati_'+r['request_number'],title='Completed ATI summary '+r['request_number'],url=r['url'],local_path=r['path'].split('data_collection_2026-10-12/',1)[1],metric_type='completed_request_metadata_only',notes='Summary only; underlying released package not obtained.',retrieved_at_utc=r['collected_date_utc'],status='downloaded',bytes=r['bytes'],sha256=r['sha256']))
existing={r['source_id']:r for r in rows};existing.update({r['source_id']:r for r in extra});rows=list(existing.values())
for r in rows:
    if r['source_id']=='oag_audit_2026':r['metric_type']='audit_approvals_and_allocation_context'
p.write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
fields=list(dict.fromkeys(k for r in rows for k in r))
with (ROOT/'source_manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
checks=[]
for r in rows:
    if r['status']!='downloaded':checks.append(dict(source_id=r['source_id'],status='NOT_OBTAINED',detail=r.get('error','')));continue
    path=ROOT/r['local_path'];assert path.exists()
    assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256'],path
    if path.suffix.lower() in ['.zip','.xlsx']:
        with zipfile.ZipFile(path) as z:assert z.testzip() is None
    if path.suffix.lower()=='.pdf':assert len(PdfReader(path).pages)>0
    checks.append(dict(source_id=r['source_id'],status='PASS',detail='Checksum, existence and applicable container/PDF checks pass'))
result=dict(original_sources_obtained=sum(r['status']=='downloaded' for r in rows),unavailable_sources=sum(r['status']!='downloaded' for r in rows),focus_csv_files=len(list((ROOT/'focus_2020_latest').glob('*.csv'))),extracted_csv_files=len(list((ROOT/'extracted').glob('*.csv'))),raw_bytes=sum(r.get('bytes',0) for r in rows if r['status']=='downloaded'),checks=checks)
(ROOT/'collection_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
