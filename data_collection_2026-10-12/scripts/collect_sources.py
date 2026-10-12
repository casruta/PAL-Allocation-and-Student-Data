"""Download public official sources; preserve originals and a checksum manifest."""
from pathlib import Path
import csv, hashlib, json, urllib.request, sys, subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'source_manifest.json'
entries = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else []

def fetch(source_id, url, relative_path, title, metric_type='', notes=''):
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = next((r for r in entries if r['source_id'] == source_id and r['status'] == 'downloaded'), None)
    if existing and path.exists():
        return path
    record = dict(source_id=source_id, title=title, url=url, local_path=relative_path,
                  metric_type=metric_type, notes=notes, retrieved_at_utc=datetime.now(timezone.utc).isoformat())
    try:
        if '/raw/' in str(path).replace('\\','/') and ('www.canada.ca' in url or relative_path.endswith('.pdf') or 'www.alberta.ca' in url):
            result = subprocess.run(['curl.exe','-L','--fail','--silent','--show-error','--connect-timeout','10','--max-time','40',url], capture_output=True, timeout=45)
            if result.returncode:
                raise RuntimeError(result.stderr.decode('utf-8','replace').strip())
            data=result.stdout
            record.update(final_url=url, content_type='application/pdf' if relative_path.endswith('.pdf') else 'text/html', last_modified='')
        else:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=20) as response:
                data = response.read()
                record.update(final_url=response.url, content_type=response.headers.get('Content-Type',''),
                              last_modified=response.headers.get('Last-Modified',''))
        if relative_path.endswith('.xlsx') and not data.startswith(b'PK'):
            raise ValueError('Expected an XLSX ZIP container')
        if relative_path.endswith('.pdf') and not data.startswith(b'%PDF'):
            raise ValueError('Expected PDF signature')
        path.write_bytes(data)
        record.update(status='downloaded', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        print(source_id, len(data), relative_path, flush=True)
    except Exception as exc:
        record.update(status='failed', error=str(exc))
        print(source_id, 'FAILED', str(exc), flush=True)
    entries[:] = [r for r in entries if r['source_id'] != source_id]
    entries.append(record)
    MANIFEST.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding='utf-8')
    return path if record['status']=='downloaded' else None

if __name__ == '__main__':
    package = fetch('ircc_catalogue', 'https://open.canada.ca/data/api/action/package_show?id=90115b00-f9b8-49e8-afa3-b4cff8facaee', 'raw/metadata/ircc_study_permits_catalogue.json', 'IRCC study permit holders catalogue')
    if package:
        metadata=json.loads(package.read_text(encoding='utf-8'))['result']
        for r in metadata['resources']:
            if r.get('language') == ['en'] and r.get('format') == 'XLSX' and '[ARCHIVED]' not in r['name']:
                kind='year_end_permit_holder_stock' if 'December 31st' in r['name'] else 'permit_holders_by_effective_year'
                fetch('ircc_'+r['id'], r['url'], 'raw/ircc/'+r['url'].split('/')[-1], r['name'], kind,
                      'Original IRCC workbook. Preserve rounding, suppression, population, and period notes. Not a direct enrolment measure or PAL utilization.')
    fetch('alberta_enrolment_catalogue','https://open.alberta.ca/api/3/action/package_show?id=9d5b3f25-3fa5-4600-a48c-ba200ca6c4a8','raw/metadata/alberta_enrolment_catalogue.json','Alberta headcount enrolment catalogue')
    fetch('alberta_international_enrolment','https://open.alberta.ca/dataset/9d5b3f25-3fa5-4600-a48c-ba200ca6c4a8/resource/5776c043-d497-45bb-acb4-f63293443043/download/international-headcount-enrolment-within-the-alberta-post-secondary-education-system.xlsx','raw/alberta/international-headcount-enrolment.xlsx','International headcount enrolment within Alberta post-secondary education system','academic_year_enrolment','Coverage limited to reporting institutions and definitions in source.')
    pages = [
      ('pal_allocations_2024','https://www.canada.ca/en/immigration-refugees-citizenship/news/2024/04/minister-miller-issues-statement-on-international-student-allocations-for-provinces-and-territories.html','2024 provincial allocations','application_space_allocation'),
      ('pal_allocations_2025','https://www.canada.ca/en/immigration-refugees-citizenship/news/notices/2025-provincial-territorial-allocations-under-international-student-cap.html','2025 provincial allocations','application_space_allocation'),
      ('pal_allocations_2026','https://www.canada.ca/en/immigration-refugees-citizenship/news/notices/2026-provincial-territorial-allocations-under-international-student-cap.html','2026 provincial allocations','application_space_allocation'),
      ('oag_audit_2026','https://www.canada.ca/en/immigration-refugees-citizenship/corporate/transparency/committees/cimm-apr-20-2026/oag-report.html','IRCC reproduction of Auditor General International Student Program Reforms report','audit_application_space_usage'),
      ('alberta_pal_process','https://www.alberta.ca/advising-international-students','Alberta advising international students','pal_process'),
      ('alberta_dli_list','https://www.alberta.ca/designated-post-secondary-institutions-alberta','Alberta designated post-secondary institutions','institution_reference'),
    ]
    for sid,url,title,kind in pages:
        if '--skip-web' not in sys.argv:
            fetch(sid,url,'raw/web/'+sid+'.html',title,kind)
    pdfs = [
      ('alberta_annual_report_2024_25','https://open.alberta.ca/dataset/9c785a4b-e79a-465b-8fa9-322a322f1f15/resource/f0581939-0ba9-4bd8-8290-3148f224ec76/download/ae-annual-report-2024-2025.pdf','Alberta Advanced Education Annual Report 2024-25','pal_letters_issued_fiscal_year'),
      ('lethbridge_budget_2024','https://www.ulethbridge.ca/sites/default/files/2024/03/2024-25_budget_message_to_community_mar_1-24_final.pdf','University of Lethbridge 2024-25 budget message','institution_pal_allocation'),
      ('calgary_gaps_2025_01_22','https://www.ucalgary.ca/secretariat/sites/default/files/teams/1/GFC/Standing%20Committee%20Minutes/GAPS/GAPS%20Approved%20Minutes%202025-01-22.pdf','University of Calgary GAPS approved minutes 2025-01-22','qualitative_pal_usage'),
    ]
    for sid,url,title,kind in pdfs:
        fetch(sid,url,'raw/documents/'+sid+'.pdf',title,kind)
