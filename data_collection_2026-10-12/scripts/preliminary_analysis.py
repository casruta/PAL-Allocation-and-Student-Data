"""Clean preserved public extracts and build bounded, source-linked analysis tables.
Run from any directory. Originals are never changed. No network is used.
"""
from pathlib import Path
import hashlib
import json
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis'
CLEAN = OUT / 'cleaned'
TABLES = OUT / 'tables'
for folder in (CLEAN, TABLES):
    folder.mkdir(parents=True, exist_ok=True)

def snake(s):
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')

def save(df, name):
    df.to_csv(TABLES / (name + '.csv'), index=False, encoding='utf-8-sig')
    return df

datasets = {}
profiles = []
checks = []
def check(name, passed, detail):
    checks.append({'check': name, 'passed': bool(passed), 'detail': detail})

for path in sorted((ROOT / 'focus_2020_latest').glob('*.csv')):
    df = pd.read_csv(path, keep_default_na=False)
    df.columns = [snake(c) for c in df.columns]
    trimmed = 0
    for col in [c for c in df if pd.api.types.is_string_dtype(df[c])]:
        before = df[col].copy()
        df[col] = df[col].str.strip()
        trimmed += int((df[col] != before).sum())
    value_cols = [c for c in ['value', 'headcount', 'application_spaces',
        'expected_permits_pal_required', 'graduate_application_spaces',
        'other_application_spaces'] if c in df]
    for col in value_cols:
        df[col] = pd.to_numeric(df[col].replace('', pd.NA), errors='raise').astype('Int64')
    if 'academic_year' in df:
        df['period_type'] = 'academic_year'
        df['period_complete'] = True
        df['metric_family'] = 'annual_international_enrolment_headcount'
    elif 'period' in df:
        df['period_type'] = df['period'].map(lambda x: 'calendar_year' if x == 'Calendar year' else 'partial_calendar_year')
        df['period_complete'] = df['period_type'].eq('calendar_year')
    if path.name.startswith('ircc_') and 'effective_year' in path.name:
        df['metric_family'] = 'study_permit_holders_by_effective_year'
    if path.name == 'ircc_year_end_permit_holders.csv':
        df['metric_family'] = 'year_end_permit_holder_stock'
        df['source_vintage'] = '2024-12-31'
    if path.name.startswith('pal_provincial'):
        df['metric_family'] = 'planned_pal_required_application_spaces'
        df['actual_recipients_available'] = False
    # Explicitly identify rows that must not be added to their constituent details.
    if 'program_type' in df:
        df['record_role'] = df['program_type'].map(lambda x: 'system_total' if x == 'All Program Types' else ('credential_total' if x.endswith(' Total') else 'program_detail'))
    if 'post_secondary_institution' in df:
        df['record_role'] = df['post_secondary_institution'].map(lambda x: 'system_total' if x == 'All Post-Secondary Institutions' else ('sector_total' if x.endswith(' Total') else 'institution'))
    # Preserve the file's actual observation grain. Source locations are not keys.
    if 'academic_year' in df:
        keys = [c for c in df.columns if c not in value_cols and not c.startswith('source_') and c not in ['period_type','period_complete','metric_family','record_role']]
    elif 'row_type' in df:
        keys = [c for c in ['province','institution','administrative_type','study_level','row_type','year'] if c in df]
    elif 'application_spaces' in df:
        keys = ['year','province']
    elif 'vector' in df:
        keys = ['ref_date','vector']
    else:
        keys = [c for c in df if not c.startswith('source_') and c not in value_cols]
    dup = int(df.duplicated(keys).sum())
    check(path.stem + ': unique keys', dup == 0, {'keys': keys, 'duplicate_rows': dup})
    for col in value_cols:
        check(path.stem + ': nonnegative ' + col, not (df[col].dropna() < 0).any(), {'missing': int(df[col].isna().sum())})
    if 'suppressed' in df and 'value' in df:
        mask = df['suppressed'].astype(str).str.lower().eq('true')
        check(path.stem + ': suppression preserved', df.loc[mask,'value'].isna().all(), {'suppressed_rows': int(mask.sum())})
    df.to_csv(CLEAN / path.name, index=False, encoding='utf-8-sig')
    datasets[path.stem] = df
    profiles.append({'file': path.name, 'rows': len(df), 'trimmed_cells': trimmed,
        'key_columns': '|'.join(keys), 'duplicate_keys': dup,
        'missing_numeric_cells': int(df[value_cols].isna().sum().sum()),
        'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

cred = datasets['alberta_enrolment_by_credential_and_program_type']
system = cred[cred.program_type.eq('All Program Types')][['academic_year','headcount']].rename(columns={'headcount':'system_headcount'})
degree = cred[cred.credential_type.eq('Degree') & cred.program_type.isin(["Bachelor's", "Master's", 'Doctoral'])].copy()
degree = degree.merge(system, on='academic_year', validate='many_to_one')
degree['share_of_system_pct'] = 100 * degree.headcount / degree.system_headcount
degree['share_note'] = 'Membership share; program categories may overlap. Not PAL/permit recipients.'
save(degree, 'alberta_degree_enrolment_trend')
trend = system.sort_values('academic_year').copy()
trend['year_over_year_pct'] = trend.system_headcount.pct_change() * 100
save(trend, 'alberta_system_enrolment_trend')

inst = datasets['alberta_enrolment_by_sector_and_institution']
latest_inst = inst[inst.academic_year.eq('2024-2025') & inst.status.eq('Total') & inst.record_role.eq('institution')].sort_values('headcount',ascending=False)
save(latest_inst, 'alberta_institution_enrolment_2024_25')
instsum = int(latest_inst.headcount.sum())
syslatest = int(system.loc[system.academic_year.eq('2024-2025'),'system_headcount'].iloc[0])
check('LERS overlapping institution memberships retained', instsum == 50606 and syslatest == 50164,
      {'institution_sum': instsum, 'published_unique_system_total': syslatest, 'excess_memberships': instsum-syslatest})

permits = datasets['ircc_alberta_institution_permit_effective_year']
pdetail = permits[permits.row_type.eq('institution')].copy()
wide = pdetail[pdetail.year.isin([2020,2021,2022,2023,2024,2025])].pivot(index=['institution','administrative_type'], columns='year', values='value').reset_index()
wide.columns = [str(c) for c in wide.columns]
wide['change_2024_to_2025'] = wide['2025']-wide['2024']
wide['change_2024_to_2025_pct'] = 100*(wide['2025']/wide['2024'].replace(0,pd.NA)-1)
wide['metric_note'] = 'Holders whose permits became effective in the year; not initial approvals, PAL recipients or current enrolment.'
save(wide.sort_values('2025',ascending=False), 'alberta_institution_permit_effective_2020_2025')
save(permits[permits.row_type.ne('institution')], 'alberta_postsecondary_permit_effective_totals')
save(datasets['ircc_permit_effective_year_province_study_level'].query("study_level == 'All study levels'"), 'canada_province_permit_effective_totals')
save(datasets['ircc_year_end_permit_holders'].query("study_level == 'All study levels'"), 'canada_province_year_end_stock_2020_2024')

pal = datasets['pal_provincial_allocations_2024_2026']
grad = pal[pal.year.eq(2025)].copy()
grad['graduate_share_of_allocation_pct'] = 100*grad.graduate_application_spaces/grad.application_spaces
save(grad, 'pal_2025_graduate_allocation_by_province')
save(pal[pal.province.eq('Alberta')], 'alberta_pal_allocations_2024_2026')
check('2025 allocation graduate + other', (grad.graduate_application_spaces + grad.other_application_spaces == grad.application_spaces).all(), 'All published province/territory and total rows')
for y in [2024,2025,2026]:
    rows=pal[pal.year.eq(y)]
    total=rows[rows.province.eq('Total')]
    if len(total):
        difference = int(rows.loc[~rows.province.eq('Total'),'application_spaces'].sum()-total.application_spaces.iloc[0])
        checks.append({'check':f'{y} provincial allocation sum minus published total','passed':difference==0,'detail':difference,'severity':'source_discrepancy' if difference else 'info'})
evidence = pd.concat([pd.read_csv(ROOT/'extracted'/f) for f in ['pal_verified_evidence.csv','pal_additional_verified_evidence.csv']],ignore_index=True)
save(evidence, 'alberta_pal_actuals_and_evidence')

for dim in ['age_group','gender','field_of_study','2_digit_cip_code']:
    d=datasets['alberta_enrolment_by_'+dim]
    save(d[d.academic_year.eq('2024-2025')], 'alberta_2024_25_'+dim)

pd.DataFrame(profiles).to_csv(OUT/'cleaning_profile.csv',index=False)
# Additional degree context: retain the publisher's exact classification names.
pspath = ROOT/'raw/degree_detail/37100232_international_degrees_canada_alberta_2019_2024.csv'
if pspath.exists():
    ps = pd.read_csv(pspath)
    ps.columns = [snake(c) for c in ps.columns]
    ps['value'] = pd.to_numeric(ps['value'],errors='raise').astype('Int64')
    ps['source_url'] = 'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710023201'
    ps['source_file'] = str(pspath.relative_to(ROOT)).replace('\\','/')
    ps['record_role'] = ps.geography_and_institutions.map(lambda s: 'geography_total' if s in ['Canada','Alberta'] else 'institution')
    ps.to_csv(CLEAN/'statcan_international_degree_institution.csv',index=False,encoding='utf-8-sig')
    check('PSIS degree unique keys', not ps.duplicated(['academic_year','coordinate']).any(), 'academic_year + coordinate')
    q = ps[ps.academic_year.eq('2024/2025') & ps.international_standard_classification_of_education_isced.isin(["Bachelor\'s or equivalent","Master\'s or equivalent",'Doctoral or equivalent'])]
    save(q,'statcan_degree_by_institution_2024_25')
    save(ps[ps.geography_and_institutions.isin(['Canada','Alberta'])], 'statcan_canada_alberta_degree_trend')
citpath=CLEAN/'ircc_alberta_citizenship_institution_type.csv'
if citpath.exists():
    cit=pd.read_csv(citpath)
    q=cit[cit.year.eq(2025)&cit.row_type.eq('citizenship')].copy()
    den=cit[cit.year.eq(2025)&cit.row_type.eq('institution_type_total')][['institution_type','value']].rename(columns={'value':'published_type_total'})
    q=q.merge(den,on='institution_type',validate='many_to_one')
    q['share_of_type_pct']=100*q.value/q.published_type_total
    save(q.sort_values(['institution_type','value'],ascending=[True,False]),'alberta_citizenship_profile_2025')
for filename, table_id in [
    ('37100163_international_age_gender_degree.csv','3710016301'),
    ('37100163_international_field_degree.csv','3710016301'),
    ('37100232_international_institution_field_degree.csv','3710023201')]:
    path=ROOT/'raw/degree_detail'/filename
    if path.exists():
        q=pd.read_csv(path,keep_default_na=False)
        q.columns=[snake(c) for c in q.columns]
        q['value']=pd.to_numeric(q['value'].replace('',pd.NA),errors='raise').astype('Int64')
        q['source_file']=path.relative_to(ROOT).as_posix()
        q['source_url']='https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid='+table_id
        q['metric_family']='fall_snapshot_international_program_enrolments'
        q['record_role']=q.classification_of_instructional_programs_stem_and_bhase_groupings.map(lambda x:'total' if x.startswith('Total,') else ('field_subtotal' if x in ['STEM [a]','BHASE [b]'] else 'field_detail'))
        check(filename+': unique coordinates',not q.duplicated(['ref_date','coordinate']).any(),'Published coordinate + reference period')
        if 'selected_statistics' in q:
            check(filename+': counts only',q.selected_statistics.eq('Number').all(),'No percentage rows mixed with counts')
        q.to_csv(CLEAN/filename,index=False,encoding='utf-8-sig')
        if 'field_degree' in filename and table_id=='3710016301':
            save(q[q.geo.eq('Alberta')&q.ref_date.eq('2024/2025')&q.international_standard_classification_of_education_isced.isin(["Master's or equivalent",'Doctoral or equivalent'])], 'alberta_graduate_fields_2024_25')
(OUT/'validation_checks.json').write_text(json.dumps(checks,indent=2,default=str),encoding='utf-8')
hard_fail = [c for c in checks if not c['passed'] and c.get('severity') != 'source_discrepancy']
if hard_fail:
    raise AssertionError(hard_fail)
print(json.dumps({'cleaned_files':len(profiles),'cleaned_rows':sum(p['rows'] for p in profiles),
    'checks':len(checks),'source_discrepancies':[c for c in checks if not c['passed']],
    'alberta_system_trend':trend.to_dict('records'),
    'latest_degree_counts':degree[degree.academic_year.eq('2024-2025')][['program_type','headcount','share_of_system_pct']].to_dict('records')},indent=2,default=str))
