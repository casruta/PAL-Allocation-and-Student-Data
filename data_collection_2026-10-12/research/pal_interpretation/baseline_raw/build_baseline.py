from pathlib import Path
import csv, hashlib, json
from pypdf import PdfReader

root=Path(__file__).resolve().parents[3]
out=root/'research/pal_interpretation'
rows=list(csv.DictReader((root/'analysis/cleaned/annual_student_count_outline.csv').open(encoding='utf-8-sig')))
for r in rows:
    r['evidence_status']='Existing cleaned source; measure is not necessarily arrivals'
    r['source_page']=''
url='https://sencanada.ca/media/yzjh5dlm/clrk_tabling_2026-04-02_senate-question-n-32-1_downe_b_e.pdf'
pdf=out/'baseline_raw/senate_s32_ircc_reply_2026_04_02.pdf'
texts=[p.extract_text() for p in PdfReader(pdf).pages]
(out/'baseline_raw/senate_s32_extracted.txt').write_text('\n\n'.join('PDF PAGE '+str(i+1)+'\n'+t for i,t in enumerate(texts)),encoding='utf-8')
series=[('IRCC annual study permit holders excluding extensions (Senate S-32 vintage)',[243995,64545,314180,395385,495860,293260,115460],4,'Confirmed permits/arrival context; preserve exact source measure, not identical to revised new-arrivals dashboard'),('IRCC new study permit applications approved by decision year',[252920,110345,328070,411705,508865,263225,109375],2,'Decisions in year; not arrivals; not a received-year cohort; excludes extensions'),('IRCC new study permit applications received by receipt year',[425550,315760,556015,713770,914250,471675,262900],1,'Applications received in year; not approved permits or arrivals; excludes extensions')]
for metric,values,page,interpretation in series:
    for year,value in zip(range(2019,2026),values):
        # Validate manually transcribed numbers against independently extracted PDF text.
        assert f'{value:,}'.replace(',',' ') in texts[page-1],(year,value,page)
        rows.append(dict(geography='Canada',period=str(year),metric=metric,student_count=value,coverage='Full calendar year; preliminary to December 31, 2025',population='All study levels; new permits/applications excluding extensions',interpretation=interpretation,source_file=str(pdf.relative_to(root)),source_url=url,evidence_status='Verified against downloaded original PDF',source_page=page))
for r in csv.DictReader((root/'analysis/cleaned/ircc_national_new_arrivals_annual_2024_2026.csv').open(encoding='utf-8-sig')):
    rows.append(dict(geography='Canada',period=r['month'],metric='IRCC revised new student arrivals',student_count=r['study_permit_holders'],coverage='January-July only' if '2026' in r['month'] else 'Full calendar year',population='New student arrivals; all study levels',interpretation='Published current dashboard arrival series; do not splice without vintage caveat with Senate S-32 series',source_file=r['source_file'],source_url=r['source_url'],evidence_status='Existing downloaded dashboard extract',source_page=''))
with (out/'pre_pal_baseline.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'baseline_raw/provenance.json').write_text(json.dumps(dict(url=url,local_path=str(pdf.relative_to(root)),retrieved_date='2026-10-12',sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),bytes=pdf.stat().st_size,validation='All 21 manually transcribed new observations verified as present on specified PDF pages',rows=len(rows)),indent=2),encoding='utf-8')
print('Validated and wrote',len(rows),'rows')
