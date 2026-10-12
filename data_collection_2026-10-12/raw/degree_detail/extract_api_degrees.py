from pathlib import Path
import json,csv,hashlib
from datetime import datetime,timezone
p=Path(__file__).resolve().parent
m=json.loads((p/'37100232_metadata.json').read_text(encoding='utf8'))[0]['object']
dims=m['dimension']; maps=[{x['memberId']:x['memberNameEn'] for x in d['member']} for d in dims]
rows=[]; failures=[]
for r in json.loads((p/'37100232_degree_response.json').read_text(encoding='utf8')):
    o=r.get('object',{})
    if r['status']!='SUCCESS':failures.append(r);continue
    ids=[int(x) for x in o['coordinate'].split('.')]
    for point in o.get('vectorDataPoint',[]):
        row={d['dimensionNameEn']:maps[i][ids[i]] for i,d in enumerate(dims)}
        row.update(point)
        row.update(academic_year=point['refPer'][:4]+'/'+point['refPer2'][:4],coordinate=o['coordinate'],vector_id=o['vectorId'],source_table='37-10-0232-01',measure='International enrolments (program count), fall snapshot; NOT PAL or permit recipients')
        rows.append(row)
unavailable=[r for r in rows if r['value'] is None or r['value']=='']
rows=[r for r in rows if r['value'] is not None and r['value']!='']
with (p/'37100232_api_unavailable_observations.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(unavailable[0]));w.writeheader();w.writerows(unavailable)
with (p/'37100232_international_degrees_canada_alberta_2019_2024.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(p/'37100232_api_failures.json').write_text(json.dumps(failures,indent=2),encoding='utf8')
print('Numeric rows',len(rows),'Unavailable observations',len(unavailable),'Failed series',len(failures))
for row in rows:
    if row['Geography and institutions'] in ['Alberta','Canada'] and row['academic_year'] in ['2019/2020','2024/2025']:
        print(row['Geography and institutions'],row['academic_year'],row['International Standard Classification of Education (ISCED)'],row['value'],row['statusCode'])
