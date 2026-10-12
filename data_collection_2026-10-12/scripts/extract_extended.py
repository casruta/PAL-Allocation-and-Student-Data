"""Focused 2020-latest files and complementary source families."""
from pathlib import Path
import csv,json,zipfile,re,hashlib
import pandas as pd
from pypdf import PdfReader
from lxml import html

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'extracted'; FOCUS=ROOT/'focus_2020_latest'; FOCUS.mkdir(exist_ok=True)
manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
sources={r['source_id']:r for r in manifest}
inventory=[]

def save(frame,name,notes,source_id=None,folder=OUT):
    if source_id:
        frame=frame.copy(); frame['source_url']=sources[source_id]['url'];frame['source_file']=sources[source_id]['local_path']
    frame.to_csv(folder/name,index=False,encoding='utf-8-sig')
    inventory.append(dict(file=str((folder/name).relative_to(ROOT)),rows=len(frame),notes=notes))

# Preserve provider CSV metadata without unpacking the large full PSIS table.
for cube in ['17100121','37100086']:
    with zipfile.ZipFile(ROOT/f'raw/statcan/{cube}-eng.zip') as z:
        assert z.testzip() is None
        (ROOT/f'raw/statcan/{cube}_MetaData.csv').write_bytes(z.read(f'{cube}_MetaData.csv'))

with zipfile.ZipFile(ROOT/'raw/statcan/37100086-eng.zip') as z:
    selected=[]
    for chunk in pd.read_csv(z.open('37100086.csv'),dtype=str,keep_default_na=False,chunksize=100000):
        keep=(chunk['REF_DATE']>='2019/2020') & (chunk['Status of student in Canada']=='International Students') & (chunk['Country of citizenship']=='Total, country of citizenship') & (chunk['Gender']=='Total, gender')
        selected.append(chunk.loc[keep])
    psis=pd.concat(selected,ignore_index=True)
save(psis,'statcan_psis_international_enrolments_2019_2024.csv','Academic 2019/20-2024/25; fall snapshot program enrolments, not unique student headcount. Includes all Canadian provinces and institution types.','statcan_37100086_zip',FOCUS)

with zipfile.ZipFile(ROOT/'raw/statcan/17100121-eng.zip') as z:
    npr=pd.read_csv(z.open('17100121.csv'),dtype=str,keep_default_na=False)
selected=npr[npr['Non-permanent resident types'].isin([
 'Study permit holders only','Work and study permit holders',
 'Asylum claimants, protected persons and related groups with study permit only',
 'Asylum claimants, protected persons and related groups with work and study permits'])]
save(selected,'statcan_study_related_resident_estimates_2021_2026.csv','Usual-resident estimates. Separate study-only, work-and-study and asylum-related categories. Not institutional enrolment.','statcan_17100121_zip',FOCUS)

sid='ircc_current_stock_arrivals'; tables=pd.read_html(ROOT/sources[sid]['local_path'])
for i,name,notes in [
 (1,'ircc_national_new_arrivals_annual_2024_2026.csv','New arrivals excluding permit extensions; 2026 January-July only.'),
 (2,'ircc_national_new_student_arrivals_monthly.csv','New student arrivals December2023-July2026; excludes asylum claimants and extensions.'),
 (4,'ircc_national_study_permit_stock_monthly.csv','Monthly stock December2023-July2026; includes dual work-study holders, excludes asylum claimants/protected persons/related groups. Different scope from older year-end workbook.'),
]: save(tables[i],name,notes,sid,FOCUS)

sid='statcan_feasibility_methods'
for i,table in enumerate(pd.read_html(ROOT/sources[sid]['local_path'])):
    table.columns=[' | '.join(dict.fromkeys(map(str,c))) if isinstance(c,tuple) else c for c in table.columns]
    save(table,f'statcan_preliminary_estimates_source_table_{i+1}.csv','Observed and modelled values in one source table. 2024/25 and 2025/26 are preliminary estimates in this May2026 study; observed 2024/25 PSIS later published October2026. Prairies is not Alberta.',sid)

# Filter copies; retain the original full-history extracts and source values.
for name in ['ircc_year_end_permit_holders.csv','ircc_permit_effective_year_province_study_level.csv','ircc_alberta_institution_permit_effective_year.csv','pal_provincial_allocations_2024_2026.csv']:
    frame=pd.read_csv(OUT/name,dtype=str,keep_default_na=False)
    save(frame[frame['year'].astype(int)>=2020],name,'Focused calendar2020-latest copy; original full-history file retained.',folder=FOCUS)
for path in OUT.glob('alberta_enrolment_by_*.csv'):
    frame=pd.read_csv(path,dtype=str,keep_default_na=False)
    if 'Academic Year' in frame:
        save(frame[frame['Academic Year']>='2019-2020'],path.name,'Six complete academic years2019/20-2024/25; reporting changes apply.',folder=FOCUS)

evidence=[]
for sid,term,entity,period,metric,value,quote,notes in [
 ('lethbridge_gfc_2025_02','1,784','University of Lethbridge','2024 (last year in February2025 minutes)','PALs issued',1784,'We issued 1,784 PALS last year','Letters issued, not applications submitted; do not compute utilization against a differently dated allocation.'),
 ('macewan_gfc_2025_02','1,500','MacEwan University','2025 expected','Expected PAL allocation',1500,'the university expects 1,500 letters to support recruitment efforts.','Expectation, not confirmed allocation or issuance.'),
 ('lethbridge_fees_2025_26','used them','University of Lethbridge','2024 admissions context','PAL submission count unknown','','we don’t know how many used them to apply for a study permit','Explicit distinction between letters issued and used. Fall307 registrants not a matched cohort for1784 PALs.'),
]:
    source=sources[sid]; pdf=PdfReader(ROOT/source['local_path'])
    matches=[(i+1,' '.join(p.extract_text().split())) for i,p in enumerate(pdf.pages) if term in p.extract_text()]
    assert matches
    page,text=matches[0]; assert quote in text
    evidence.append(dict(entity=entity,period=period,metric=metric,value=value,quote=quote,pdf_page=page,source_file=source['local_path'],source_url=source['url'],notes=notes))
save(pd.DataFrame(evidence),'pal_additional_verified_evidence.csv','New verified institutional issuance/expected-allocation records; incompatible denominators must not be joined.')

comparators=[]
for sid,page,entity,period,metric,value,quote,notes in [
 ('usask_pal_council_2025',1024,'University of Saskatchewan','2024; endorsements as of December3','PALs endorsed',1623,'as of December 3, 2024, had endorsed 1,623 PALs.','Same passage reports2958 allocated and approximately55% utilization. Endorsement is not proven IRCC submission.'),
 ('manitoba_pal_senate_2025',4,'University of Manitoba','2024 retrospective in February2025','PAL usage bound','','received 7,540 PALs but had used fewer than half','7540 allocated; fewer than half is not an exact count.'),
]:
    s=sources[sid];txt=' '.join(PdfReader(ROOT/s['local_path']).pages[page-1].extract_text().split());assert quote in txt
    comparators.append(dict(entity=entity,period=period,metric=metric,value=value,quote=quote,pdf_page=page,source_file=s['local_path'],source_url=s['url'],notes=notes))
sid='mcmaster_pal_2024';s=sources[sid];txt=' '.join(html.parse(ROOT/s['local_path']).getroot().text_content().split())
quote='90 per cent of PALs were issued to eligible applicants with a utilization rate of 70 per cent';assert quote in txt
comparators.append(dict(entity='McMaster University',period='2024 award account published May16 2025',metric='Reported PAL issuance and utilization percentages',value='',quote=quote,pdf_page='',source_file=s['local_path'],source_url=s['url'],notes='90%issued and70%utilization; absolute denominator and utilization definition unspecified.'))
save(pd.DataFrame(comparators),'pal_other_province_institution_evidence.csv','Selected official institution examples, not province-wide or exhaustive. Definitions differ.')

# Validate canonical PSIS and stock cells, record provider geography/types/periods.
def get_psis(geo,kind):
    r=psis[(psis['REF_DATE']=='2024/2025')&(psis['GEO']==geo)&(psis['Institution type']==kind)]
    assert len(r)==1;return int(r.iloc[0]['VALUE'])
assert get_psis('Canada','University')==266874
assert get_psis('Canada','College')==266508
assert int(tables[4].iloc[-1,1])==590205
summary=dict(psis_rows=len(psis),psis_years=sorted(psis.REF_DATE.unique().tolist()),psis_geographies=sorted(psis.GEO.unique().tolist()),npr_rows=len(selected),npr_periods=sorted(selected.REF_DATE.unique().tolist()),npr_types=sorted(selected['Non-permanent resident types'].unique().tolist()),alberta_psis_2024_25={k:get_psis('Alberta',k) for k in ['Total, institution type','University','College']},checks=['PSIS Canada university266874 and college266508 match October1,2026 official release','IRCC July2026 national stock590205 matches published page','Both compressed CSV archives pass ZIP integrity test','All new PAL evidence quotes verified in original PDF pages'])
(ROOT/'extended_validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
save(pd.DataFrame(inventory),'extended_file_inventory.csv','Index of focused and additional extracts.')
print(json.dumps(summary,indent=2))
