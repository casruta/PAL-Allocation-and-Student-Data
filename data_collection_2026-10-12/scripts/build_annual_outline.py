"""Create annual student outlines without combining unlike populations or periods."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT/'analysis/cleaned'
def read(name): return pd.read_csv(CLEAN/(name+'.csv'))
def save(df,name):
    for col in df:
        if len(str(col)) == 9 and str(col)[4:5] == '-' and str(col)[:4].isdigit():
            df[col]=pd.to_numeric(df[col],errors='raise').astype('Int64')
    df.to_csv(CLEAN/(name+'.csv'),index=False,encoding='utf-8-sig')

inst=read('alberta_enrolment_by_sector_and_institution')
system=inst[inst.record_role.eq('system_total')&inst.status.eq('Total')].sort_values('academic_year')
psis=read('statcan_psis_international_enrolments_2019_2024')
psis=psis[psis.geo.isin(['Canada','Alberta'])&psis.institution_type.eq('Total, institution type')].copy()
psis['academic_year']=psis.ref_date.str.replace('/','-',regex=False)
wide=psis.pivot(index='academic_year',columns='geo',values='value').rename(columns={'Alberta':'alberta_psis_fall_program_enrolments','Canada':'canada_psis_fall_program_enrolments'}).reset_index()
wide=wide.merge(system[['academic_year','headcount']].rename(columns={'headcount':'alberta_lers_annual_unique_headcount'}),on='academic_year',validate='one_to_one')
wide['alberta_share_of_canada_psis_pct']=100*wide.alberta_psis_fall_program_enrolments/wide.canada_psis_fall_program_enrolments
wide['note']='PSIS is a fall program count; LERS is annual headcount. Do not add or substitute these measures.'
wide['psis_source_url']=psis.source_url.iloc[0]
wide['lers_source_url']=system.source_url.iloc[0]
save(wide,'annual_enrolment_canada_alberta')

rows=[]
def add(source, geography, period, metric, count, completeness, population, note):
    rows.append({'geography':geography,'period':str(period),'metric':metric,'student_count':count,
        'coverage':completeness,'population':population,'interpretation':note,
        'source_file':source.get('source_file',''),'source_url':source.get('source_url','')})
for _,r in system.iterrows():
    add(r,'Alberta',r.academic_year,'LERS annual international student headcount',r.headcount,'Published academic-year reporting period',
        'Reporting institutions and provincially approved programs','Annual unique system headcount; reporting changes apply, including Athabasca 16-month 2024-25 period.')
for _,r in psis.iterrows():
    add(r,r.geo,r.academic_year,'PSIS international program enrolments',r.value,'Fall snapshot',
        'Post-secondary international program enrolments','Program counts, not unique people; rounded to three.')
for _,r in read('ircc_year_end_permit_holders').query("province in ['Alberta','Canada'] and study_level == 'All study levels'").iterrows():
    add(r,r.province,r.as_of,'IRCC year-end study permit holders (2024 vintage)',r.value,'December 31 snapshot',
        'All study levels; administrative permit-holder stock','Not current attendance; do not splice with revised monthly-stock series.')
for _,r in read('ircc_permit_effective_year_province_study_level').query("province in ['Alberta','Canada'] and study_level == 'All study levels'").iterrows():
    add(r,r.province,str(int(r.year))+(' January-July' if int(r.year)==2026 else ''),'IRCC permit-effective-year holders, all study levels',r.value,
        'Partial calendar year: January-July' if int(r.year)==2026 else 'Full calendar year',
        'All study levels; permits becoming effective','Not initial approvals, arrivals, enrolments or PAL recipients; rounded to five.')
for _,r in read('ircc_alberta_institution_permit_effective_year').query("row_type == 'province_total'").iterrows():
    add(r,'Alberta',str(int(r.year))+(' January-July' if int(r.year)==2026 else ''),'IRCC post-secondary DLI permit-effective-year holders',r.value,
        'Partial calendar year: January-July' if int(r.year)==2026 else 'Full calendar year',
        'Post-secondary DLI series','Different coverage from all-study-level series; not initial approvals or PAL usage.')
monthly=read('ircc_national_study_permit_stock_monthly')
monthly['date']=pd.to_datetime(monthly.month,format='%b-%y')
# December observations are year-end; latest 2026 observation stays explicitly mid-year.
selected=monthly[monthly.date.dt.month.eq(12)|(monthly.date.eq(monthly.date.max()))]
for _,r in selected.iterrows():
    date=r.date+pd.offsets.MonthEnd(0)
    add(r,'Canada',date.strftime('%Y-%m-%d'),'IRCC revised monthly study permit-holder stock',r.number_of_permit_holders,
        'December 31 snapshot' if date.month==12 else 'Mid-year snapshot; not year-end',
        'Study permit holders, including dual work/study; excludes asylum-related groups',
        'Retain separate series: scope/vintage differ from older year-end workbook.')
outline=pd.DataFrame(rows).sort_values(['metric','geography','period'])
outline['student_count']=pd.to_numeric(outline.student_count,errors='raise').astype('Int64')
save(outline,'annual_student_count_outline')

# Do not sum institutions: retain the independently reported unique system total.
details=inst[inst.record_role.eq('institution')&inst.status.eq('Total')]
institution=details.pivot(index=['sector','post_secondary_institution'],columns='academic_year',values='headcount').reset_index()
institution.columns.name=None
institution['metric']='LERS annual international headcount per institution'
institution['note']='People may attend multiple institutions. Do not sum to estimate unique Alberta students. Blank means no published observation, not zero.'
institution['source_url']=system.source_url.iloc[0]
save(institution,'annual_alberta_enrolment_by_institution')
credential=read('alberta_enrolment_by_credential_and_program_type')
detail=credential[credential.record_role.eq('program_detail')]
study=detail.pivot(index=['credential_type','program_type'],columns='academic_year',values='headcount').reset_index()
study.columns.name=None
study['metric']='LERS annual international headcount by credential/program'
study['note']='Program memberships overlap. Graduate certificates/diplomas are not masters degrees. Blank is unavailable, not zero.'
study['source_url']=system.source_url.iloc[0]
save(study,'annual_alberta_enrolment_by_study_level')

checks={
    'six_academic_years':len(wide)==6,
    'annual_outline_keys_unique':not outline.duplicated(['geography','period','metric']).any(),
    'no_missing_overview_counts':outline.student_count.notna().all(),
    'lers_totals_match_original':wide.alberta_lers_annual_unique_headcount.tolist()==system.headcount.tolist(),
    'institution_rows_match':len(institution)==details.post_secondary_institution.nunique(),
    'credential_rows_match':len(study)==len(detail[['credential_type','program_type']].drop_duplicates()),
    'partial_2026_is_labelled':outline[outline.period.str.startswith('2026')].coverage.isin(['Partial calendar year: January-July','Mid-year snapshot; not year-end']).all(),
}
checks={k:bool(v) for k,v in checks.items()}
(ROOT/'analysis/annual_outline_validation.json').write_text(json.dumps(checks,indent=2))
assert all(checks.values()),checks
print(wide.iloc[:,:5].to_string(index=False))
print(json.dumps({'outline_rows':len(outline),'institution_rows':len(institution),'study_level_rows':len(study),'checks':checks},indent=2))
