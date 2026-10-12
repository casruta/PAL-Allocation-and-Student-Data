"""Extract Alberta citizenship rows and published type totals; preserve raw cells."""
from pathlib import Path
from zipfile import ZipFile
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'raw/ircc/EN_ODP-TR-Study-DLI_PT_Inst_type_COC.xlsx'
URL = 'https://www.ircc.canada.ca/opendata-donneesouvertes/data/EN_ODP-TR-Study-DLI_PT_Inst_type_COC.xlsx'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

# Reading the stored worksheet cells avoids expanding blank formatted cells.
with ZipFile(ROOT / SOURCE) as archive:
    workbook = ET.fromstring(archive.read('xl/workbook.xml'))
    sheet_name = workbook.find('m:sheets/m:sheet', NS).get('name')
    sheet = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
    assert 'xl/sharedStrings.xml' not in archive.namelist(), 'Recheck changed XLSX encoding'
    cells = {}
    for row in sheet.findall('m:sheetData/m:row', NS):
        number = int(row.get('r'))
        cells[number] = {}
        for cell in row.findall('m:c', NS):
            address = cell.get('r')
            column = address.rstrip('0123456789')
            if cell.get('t') == 'inlineStr':
                raw = ''.join(t.text or '' for t in cell.findall('m:is//m:t', NS))
            else:
                raw = cell.findtext('m:v', default='', namespaces=NS)
            cells[number][column] = raw

title = cells[1]['A']
assert 'January 2016 - July 2026' in title
totals = [(column, int(raw[:4])) for column, raw in cells[3].items()
          if re.fullmatch(r'20\d\d Total', raw) and int(raw[:4]) >= 2020]
assert [year for _, year in totals] == list(range(2020, 2027))
end = next(n for n, row in cells.items() if row.get('A') == 'Alberta Total')
previous_end = max(n for n, row in cells.items()
                   if n < end and row.get('A', '').endswith(' Total'))
start = previous_end + 1
assert cells[previous_end]['A'] == 'Saskatchewan Total'
type_total_rows = [n for n in range(start, end) if cells[n].get('B')]
assert len(type_total_rows) == 7
records = []
institution_type = None
for number in range(end, start - 1, -1):
    row = cells[number]
    if number == end:
        kind, institution_type, citizenship = 'province_total', 'All institution types', 'All citizenships'
        label_cell = f'A{number}'
    elif row.get('B'):
        kind, institution_type, citizenship = 'institution_type_total', row['B'], 'All citizenships'
        label_cell = f'B{number}'
    elif row.get('C'):
        kind, citizenship = 'citizenship', row['C']
        label_cell = f'C{number}'
        # Independent forward check: each country belongs to the next B subtotal.
        next_total = min(n for n in type_total_rows if n > number)
        assert institution_type == cells[next_total]['B']
    else:
        raise AssertionError(f'Unexpected Alberta row {number}')
    for column, year in totals:
        raw = row.get(column, '')
        if raw == '--':
            value, status = '', 'suppressed'
        elif raw == '':
            value, status = '', 'blank'
        else:
            assert re.fullmatch(r'[\d,]+', raw), (number, column, raw)
            value, status = int(raw.replace(',', '')), 'published_numeric'
        records.append(dict(
            province='Alberta', institution_type=institution_type,
            country_of_citizenship=citizenship, row_type=kind, year=year,
            period='January-July' if year == 2026 else 'Calendar year',
            partial_year=year == 2026, value=value, value_raw=raw,
            value_status=status, suppressed=status == 'suppressed',
            measure='Study permit holders by year permit(s) became effective',
            source_file=SOURCE, source_sheet=sheet_name,
            source_cell=f'{column}{number}', source_label_cell=label_cell,
            source_url=URL, source_as_of='2026-07-31'))

records.sort(key=lambda r: (r['institution_type'], r['row_type'], r['country_of_citizenship'], r['year']))
keys = [(r['institution_type'], r['row_type'], r['country_of_citizenship'], r['year']) for r in records]
assert len(keys) == len(set(keys))
assert len(records) == (end - start + 1) * 7
assert all(r['value_raw'] == cells[int(re.search(r'\d+$', r['source_cell'])[0])].get(
    r['source_cell'].rstrip('0123456789'), '') for r in records)

out = ROOT / 'analysis/cleaned/ircc_alberta_citizenship_institution_type.csv'
out.parent.mkdir(parents=True, exist_ok=True)
with out.open('w', newline='', encoding='utf-8-sig') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)

notes = [
    'IRCC ALBERTA CITIZENSHIP BY INSTITUTION TYPE: EXTRACTION NOTES',
    f'Source title: {title}', f'Source URL: {URL}', f'Source file: {SOURCE}',
    f'Source sheet: {sheet_name}', f'SHA-256: {hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest()}',
    f'Alberta block: worksheet rows {start}-{end}; preceding subtotal is Saskatchewan at row {previous_end}.',
    f'Extracted {len(records)} observations, 2020-2025 calendar years and January-July 2026.',
    'Annual columns are the publisher\'s annual unique totals; months and quarters were NOT summed.',
    'Seven institution types: Career College, College, Flight School, Language School, Other, Theological School, University.',
    'University is an institution type, not a degree level. Master\'s and PhD recipients cannot be separated here.',
    'Country means citizenship, not birthplace, ethnicity, residence, or country of application.',
    'The metric is holders whose permits became effective; it is NOT approvals, PAL issuance, enrolment, new arrivals, or a current stock.',
    'Exact country spellings and raw cell strings are preserved. Suppressed -- and blank cells have blank numeric values; explicit 0 remains zero.',
    'The workbook says all values between 0 and 5 are --, although it also publishes explicit 0 and 5. Do not infer a precise suppression interval.',
    'Values are rounded to five. Country sums need not match totals. Published institution-type total is the denominator for that type.',
    'Do not sum totals across institution types to estimate distinct people; cross-type uniqueness is not established.',
    'Shares below are approximate descriptive ratios of published rounded country values to the published rounded type total.',
    'All source-cell values were checked. Every country was independently matched to its next following institution-type subtotal.',
    'All output keys are unique and each source row has seven year observations.', '',
    'Publisher footnotes (verbatim stored text):', cells[5810]['A'], cells[5812]['A'], '',
    '2025 TOP COUNTRIES AND DENOMINATORS'
]
for institution_type in ['University', 'College']:
    denominator_record = next(r for r in records if r['institution_type'] == institution_type
                              and r['row_type'] == 'institution_type_total' and r['year'] == 2025)
    denominator = denominator_record['value']
    notes.append(f'{institution_type}: published total {denominator:,}; source {denominator_record["source_cell"]}.')
    selected = sorted((r for r in records if r['institution_type'] == institution_type
                       and r['row_type'] == 'citizenship' and r['year'] == 2025 and isinstance(r['value'], int)),
                      key=lambda r: r['value'], reverse=True)
    for r in selected[:10]:
        notes.append(f'  {r["country_of_citizenship"]}: {r["value"]:,}; approx. {r["value"] / denominator * 100:.2f}%; source {r["source_cell"]}.')
    notes.append(f'  Sum of numeric published country cells: {sum(r["value"] for r in selected):,}; suppressed cells: '
                 f'{sum(r["value_status"] == "suppressed" for r in records if r["institution_type"] == institution_type and r["row_type"] == "citizenship" and r["year"] == 2025)}.')

notes_path = ROOT / 'analysis/citizenship_extraction_notes.txt'
notes_path.write_text('\n'.join(notes) + '\n', encoding='utf-8')
print(json.dumps({'observations': len(records), 'source_rows': [start, end], 'csv': str(out), 'notes': str(notes_path)}))
print('\n'.join(notes[notes.index('2025 TOP COUNTRIES AND DENOMINATORS'):]))
