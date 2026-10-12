from pathlib import Path
import csv,json,hashlib
from datetime import datetime,timezone
p=Path(__file__).resolve().parent
read=lambda name:list(csv.DictReader((p/name).open(encoding='utf-8-sig',newline='')))
def write(name,rows):
    with (p/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
degree='International Standard Classification of Education (ISCED)'
field='Classification of Instructional Programs, STEM and BHASE groupings'
r=read('37100163_international_canada_alberta_2019_latest.csv')
count=[x for x in r if x['Selected statistics']=='Number' and x['Institution type']=='Total, institution type' and x['Selected academic period']=='Fall snapshot']
age=[x for x in count if x[field]=='Total, instructional program']
fields=[x for x in count if x['Age group']=='Total, age group' and x['Gender']=='Total, gender']
write('37100163_international_age_gender_degree.csv',age)
write('37100163_international_field_degree.csv',fields)
r=read('37100232_international_canada_alberta_2019_latest.csv')
inst=[x for x in r if x['Institution type']=='Total, institution type' and x['Registration status']=='Total, registration status' and x['Gender']=='Total, gender']
write('37100232_international_institution_field_degree.csv',inst)
cube={(x['COORDINATE'],x['REF_DATE']):x for x in r}
api=read('37100232_international_degrees_canada_alberta_2019_2024.csv')
checks=[]
for a in api:
    coord='.'.join(a['coordinate'].split('.')[:7]); year=a['academic_year']; c=cube.get((coord,year))
    match=c is not None and c['VALUE']!='' and float(c['VALUE'])==float(a['value'])
    checks.append({'coordinate':coord,'academic_year':year,'match':match,'api_value':a['value'],'csv_value':c['VALUE'] if c else None})
report={'api_degree_rows':len(api),'matched':sum(x['match'] for x in checks),'mismatches':[x for x in checks if not x['match']],'age_gender_degree_rows':len(age),'field_degree_rows':len(fields),'institution_field_degree_rows':len(inst),'notes':'API and bulk CSV independently retrieved. Empty/status flags preserved. Totals and subtotals retained; use explicit filters, never sum the complete file.'}
(p/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
prov=json.loads((p/'provenance.json').read_text(encoding='utf8'))
known={x['file']:x for x in prov['files']}
prov['files']=[]
for path in p.iterdir():
    if path.is_file() and path.name!='provenance.json':
        entry=known.get(path.name,{'file':path.name,'source_url':None})
        entry.update({'retrieved_or_generated_utc':datetime.now(timezone.utc).isoformat(),'bytes':path.stat().st_size,'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest()})
        prov['files'].append(entry)
(p/'provenance.json').write_text(json.dumps(prov,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
