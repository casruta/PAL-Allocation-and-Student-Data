"""Create traceable CSV extracts without changing any downloaded original."""
from pathlib import Path
import csv, json, re, hashlib, zipfile
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import pandas as pd
from lxml import html
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'extracted'
OUT.mkdir(exist_ok=True)
manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
sources={r['local_path']:r for r in manifest if r['status']=='downloaded'}
inventory=[]

def write_csv(name, fields, rows, description):
    rows=list(rows)
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    inventory.append(dict(file='extracted/'+name,rows=len(rows),description=description))

def number(value):
    value=str(value).strip() if value is not None else ''
    return int(value.replace(',','')) if re.fullmatch(r'[\d,]+',value) else ''

def origin(path,sheet,row,column):
    return dict(source_file=path,source_sheet=sheet,source_cell=f'{get_column_letter(column+1)}{row+1}',source_url=sources[path]['url'])

# Enrolment: retain all institutional, sector, system, and demographic distinctions.
path='raw/alberta/international-headcount-enrolment.xlsx'
wb=load_workbook(ROOT/path,read_only=True,data_only=True)
for ws in wb:
    vals=list(ws.values)
    slug=re.sub(r'[^a-z0-9]+','_',ws.title.lower()).strip('_')
    if ws.title.startswith('By '):
        fields=list(vals[0])+['source_file','source_sheet','source_row','source_url']
        rows=[dict(zip(fields,list(r)+[path,ws.title,i+1,sources[path]['url']])) for i,r in enumerate(vals[1:],start=1) if any(v is not None for v in r)]
    else:
        width=max(map(len,vals)); fields=[f'column_{i+1}' for i in range(width)]
        rows=[dict(zip(fields,r)) for r in vals]
    write_csv('alberta_enrolment_'+slug+'.csv',fields,rows,'Direct sheet export; read Dictionary and Reporting Changes before comparison. Totals are unique counts and must not be recreated by summing institutions.')

# Year-end stocks, with province labels resolved from the following subtotal row.
path='raw/ircc/EN_ODP_annual-TR-Study-IS_PT_study_level_year_end.xlsx'
ws=load_workbook(ROOT/path,read_only=True,data_only=True).active
vals=list(ws.values); years=vals[2]; region=None; records=[]
for i in range(len(vals)-1,2,-1):
    row=vals[i]
    if len(row)<3: continue
    label=row[0]
    if label=='Total': region='Canada'; level='All study levels'; kind='national_total'
    elif label=='Province / Territory not stated': region=label; level='All study levels'; kind='province_total'
    elif label and str(label).endswith(' Total'): region=str(label)[:-6]; level='All study levels'; kind='province_total'
    elif row[1] and region: level=row[1]; kind='study_level'
    else: continue
    for j in range(2,len(years)):
        raw=row[j] if j<len(row) else None
        records.append(dict(province=region,study_level=level,row_type=kind,year=int(years[j]),as_of=f'{years[j]}-12-31',value=number(raw),value_raw=raw,suppressed=raw=='--',**origin(path,ws.title,i,j)))
records.sort(key=lambda r:(r['province'],r['study_level'],r['year']))
fields=list(records[0]); write_csv('ircc_year_end_permit_holders.csv',fields,records,'Year-end valid permit holder stock, 2000-2024; province of intended destination; rounded to 5, suppressed cells retained.')

# Permit effective-year annual/YTD totals. Do not add months to create annual unique totals.
for filename,dimensions,header_idx,output in [
 ('EN_ODP-TR-Study-IS_PT_study_level_sign.xlsx',2,3,'ircc_permit_effective_year_province_study_level.csv'),
 ('EN_ODP-TR-Study-DLI_name_PT_Admin_type.xlsx',3,2,'ircc_alberta_institution_permit_effective_year.csv'),
]:
    path='raw/ircc/'+filename
    ws=load_workbook(ROOT/path,read_only=True,data_only=True).active
    vals=list(ws.values)
    totals=[(j,int(str(v).split()[0])) for j,v in enumerate(vals[header_idx]) if re.fullmatch(r'20\d{2} Total',str(v))]
    region=None; admin=None; rows=[]
    for i in range(len(vals)-1,header_idx+1,-1):
        row=vals[i]
        if len(row)<=dimensions: continue
        first=row[0]
        if first=='Total':
            region='Canada'; kind='national_total'; member='All study levels' if dimensions==2 else 'All institutions'; admin='All types'
        elif first and str(first).endswith(' Total'):
            region=str(first)[:-6]; kind='province_total'; member='All study levels' if dimensions==2 else 'All institutions'; admin='All types'
        elif dimensions==2 and first=='Province / Territory not stated':
            region=first; kind='province_total'; member='All study levels'
        elif dimensions==3 and row[1] in ['Public Institution','Private Institution','Not Stated']:
            admin=row[1]; kind='administrative_type_total'; member='All institutions'
        elif dimensions==3 and row[2] and region:
            kind='institution'; member=row[2]
        elif dimensions==2 and row[1] and region:
            kind='study_level'; member=row[1]
        else: continue
        if dimensions==3 and region!='Alberta': continue
        for j,year in totals:
            raw=row[j] if j<len(row) else None
            record=dict(province=region,**({'institution':member,'administrative_type':admin} if dimensions==3 else {'study_level':member}),row_type=kind,year=year,period='January-July' if year==2026 else 'Calendar year',value=number(raw),value_raw=raw,suppressed=raw=='--',**origin(path,ws.title,i,j))
            rows.append(record)
    rows.sort(key=lambda r:(r['province'],r.get('institution',r.get('study_level')),r['year']))
    write_csv(output,list(rows[0]),rows,'Holders by year permit became effective; includes annual totals and partial January-July 2026. This is not current stock, enrolment, or PAL usage. Preserve original rounded values.')

# Preserve all HTML source tables before selecting comparable allocation fields.
pal=[]
for year in [2024,2025,2026]:
    path=f'raw/web/pal_allocations_{year}.html'
    tables=pd.read_html(ROOT/path)
    for idx,df in enumerate(tables):
        df.to_csv(OUT/f'pal_{year}_source_table_{idx+1}.csv',index=False,encoding='utf-8-sig')
        inventory.append(dict(file=f'extracted/pal_{year}_source_table_{idx+1}.csv',rows=len(df),description=f'Verbatim parsed table {idx+1}, {path}; retain multirow headers and published inconsistencies.'))
    allocations=tables[2]
    if year==2024: allocations=allocations.iloc[1:]
    targets=tables[1] if year>2024 else None
    for _,r in allocations.iterrows():
        province=re.sub(r'Footnote.*','',str(r.iloc[0])).strip()
        target=number(r.iloc[6]) if year==2024 else number(targets.loc[targets.iloc[:,0]==province].iloc[0,-1])
        pal.append(dict(year=year,province=province,application_spaces=number(r.iloc[5] if year==2024 else r.iloc[-1]),expected_permits_pal_required=target,graduate_application_spaces=number(r.iloc[1]) if year==2025 else '',other_application_spaces=number(r.iloc[2]) if year==2025 else '',scope='Final allocation after adjustments and top-ups; generally excludes graduate students and extensions' if year==2024 else ('Graduate and other PAL-required cohorts; exemptions differ from 2024' if year==2025 else 'PAL-required cohorts; masters and doctoral students at public DLIs exempt'),source_file=path,source_table='3 (final allocations); 2 (expected permits)' if year>2024 else '3 (final allocations and projected permits)',source_url=sources[path]['url']))
write_csv('pal_provincial_allocations_2024_2026.csv',list(pal[0]),pal,'Published application-space allocations and expected permits, not letters issued or spaces used. Annual scope differs.')

for sid in ['alberta_dli_list','oag_audit_2026']:
    path=f'raw/web/{sid}.html'
    tables=pd.read_html(ROOT/path)
    for i,df in enumerate(tables):
        if sid=='oag_audit_2026' and i!=2: continue
        name='oag_2025_approvals_as_percent_of_forecast_NOT_pal_usage.csv' if sid=='oag_audit_2026' else f'alberta_dli_register_table_{i+1}.csv'
        df['source_url']=sources[path]['url']
        df.to_csv(OUT/name,index=False,encoding='utf-8-sig')
        inventory.append(dict(file='extracted/'+name,rows=len(df),description='OAG Exhibit 7, approvals versus forecast as of September 2025, NOT PAL utilization.' if sid=='oag_audit_2026' else 'Alberta DLI register.'))

# Small verified excerpts for institution and provincial PAL availability.
evidence=[]
for sid,term,entity,period,metric,value,quote,notes in [
 ('alberta_annual_report_2024_25','26,089','Alberta','Fiscal 2024-25','PALs issued by provincial portal',26089,'In 2024-25, the portal issued 26,089 provincial attestation letters to designated learning institutions.','Portal issuance, not IRCC submissions or permits. Do not divide this fiscal-year count by a calendar-year quota.'),
 ('lethbridge_budget_2024','2,687','University of Lethbridge','2024-01-22 to 2025-01-21','Allocated study permit applications',2687,'study permit applications for January 22, 2024 to January 21, 2025 is 2,687','Institution allocation, not actual PAL issuance or utilization.'),
 ('calgary_gaps_2025_01_22','use up','University of Calgary','2024 allocation cycle','Qualitative PAL underuse','','the University was not able to use up its 2024 allocation of PALs.','No numerator, denominator or utilization percentage disclosed.'),
]:
    path='raw/documents/'+sid+'.pdf'; pdf=PdfReader(ROOT/path)
    found=[(i+1,' '.join(p.extract_text().split())) for i,p in enumerate(pdf.pages) if term in p.extract_text()]
    assert found, (sid,term)
    page,text=found[0]
    # PDF extraction sometimes inserts spaces around punctuation; retain original PDF as controlling evidence.
    assert str(value)=='' or term in text
    evidence.append(dict(entity=entity,period=period,metric=metric,value=value,quote=quote,pdf_page=page,source_file=path,source_url=sources[path]['url'],notes=notes))
write_csv('pal_verified_evidence.csv',list(evidence[0]),evidence,'Verified short quotations and page references. Incomplete institution coverage; missing values are unknown, never zero.')

write_csv('file_inventory.csv',['file','rows','description'],inventory,'Index of derived CSV files.')

# File integrity and parse checks. Report rounding/source discrepancies, never silently correct them.
checks=[]
for row in manifest:
    if row['status']!='downloaded':
        checks.append(dict(source_id=row['source_id'],status='UNAVAILABLE',detail=row.get('error'))); continue
    p=ROOT/row['local_path']; actual=hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual==row['sha256'], p
    detail='SHA-256 matches download manifest'
    if p.suffix=='.xlsx':
        with zipfile.ZipFile(p) as z: assert z.testzip() is None
        book=load_workbook(p,read_only=True,data_only=True)
        detail+='; valid XLSX; '+str(len(book.sheetnames))+' sheets'
    elif p.suffix=='.pdf': detail+='; '+str(len(PdfReader(p).pages))+' PDF pages'
    checks.append(dict(source_id=row['source_id'],status='PASS',detail=detail))
for year in [2024,2025,2026]:
    rows=[r for r in pal if r['year']==year]
    published=next(r['application_spaces'] for r in rows if r['province']=='Total')
    summed=sum(r['application_spaces'] for r in rows if r['province']!='Total')
    checks.append(dict(source_id=f'pal_allocations_{year}_sum',status='PASS' if published==summed else 'SOURCE_DISCREPANCY',detail=f'Published national total {published}; sum of provincial/territorial rows {summed}. Originals preserved.'))
(ROOT/'validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
with (ROOT/'source_manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:
    fields=list(dict.fromkeys(k for r in manifest for k in r)); w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(manifest)
print(json.dumps({'sources':len(manifest),'extracted_files':len(inventory),'checks':checks[-3:]},indent=2))
