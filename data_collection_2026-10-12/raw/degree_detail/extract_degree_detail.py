"""Stream official StatCan CSV cubes into focused raw-record subsets; no values recoded."""
from pathlib import Path
import csv, io, json, zipfile, hashlib
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
results=[]
for table in ['37100163','37100232']:
    archive=ROOT/f'{table}-eng.zip'
    with zipfile.ZipFile(archive) as z:
        members=z.namelist()
        for name in members:
            if 'MetaData' in name:
                (ROOT/name).write_bytes(z.read(name))
        data_name=next(n for n in members if n.endswith('.csv') and 'MetaData' not in n)
        with z.open(data_name) as binary, io.TextIOWrapper(binary,encoding='utf-8-sig',newline='') as stream:
            reader=csv.DictReader(stream)
            outfile=ROOT/f'{table}_international_canada_alberta_2019_latest.csv'
            n=0; scanned=0; years=set(); geos=set(); statuses=set()
            with outfile.open('w',encoding='utf-8-sig',newline='') as out:
                writer=csv.DictWriter(out,fieldnames=reader.fieldnames);writer.writeheader()
                print(table,reader.fieldnames,flush=True)
                for row in reader:
                    scanned+=1
                    if row['REF_DATE'][:4]<'2019':continue
                    geo=row['GEO']
                    if geo not in ['Canada','Alberta'] and not geo.endswith(', Alberta'):continue
                    if row['Status of student in Canada'].lower()!='international students':continue
                    writer.writerow(row);n+=1;years.add(row['REF_DATE']);geos.add(geo);statuses.add(row['STATUS'])
            results.append({'table':table,'source_member':data_name,'source_rows':scanned,'selected_rows':n,'years':sorted(years),'geographies':sorted(geos),'status_codes':sorted(statuses),'csv':outfile.name,'schema':reader.fieldnames})
            print(results[-1],flush=True)
sources=[]
for path in ROOT.iterdir():
    if path.name=='provenance.json' or not path.is_file():continue
    if path.suffix=='.zip':url=f'https://www150.statcan.gc.ca/n1/tbl/csv/{path.name}'
    elif path.name.endswith('_metadata.json'):url='https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata'
    elif ('_detail_response_' in path.name or path.name=='37100232_degree_response.json'):url='https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods'
    elif path.suffix=='.html':url='https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid='+path.stem
    elif path.name=='37100163_download_response.json':url='https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/37100163/en'
    else:url=None
    sources.append({'file':path.name,'source_url':url,'retrieved_or_generated_utc':datetime.now(timezone.utc).isoformat(),'bytes':path.stat().st_size,'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest()})
(ROOT/'provenance.json').write_text(json.dumps({'purpose':'Enrolment context only. These are not PAL or study permit recipients.','filter':'REF_DATE starts 2019 or later; GEO Canada or Alberta or institution ending , Alberta; status international students case-insensitive. All other dimensions and status flags retained unchanged.','extractions':results,'files':sources},indent=2),encoding='utf-8')
