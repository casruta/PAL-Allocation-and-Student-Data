"""Combine three research tracks into clearly scoped before/after matrices."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'research/pal_interpretation'
C=ROOT/'analysis/cleaned'
OUT=ROOT/'analysis/pal_interpretation'
OUT.mkdir(parents=True,exist_ok=True)
b=pd.read_csv(R/'pre_pal_baseline.csv')
u=pd.read_csv(R/'utilization_evidence.csv')
events=pd.read_csv(R/'events_and_drivers.csv').fillna('')
pal=pd.read_csv(C/'pal_provincial_allocations_2024_2026.csv')
senate='IRCC annual study permit holders excluding extensions (Senate S-32 vintage)'
abmetric='IRCC post-secondary DLI permit-effective-year holders'
stockmetric='IRCC year-end study permit holders (2024 vintage)'
annual=[]
for year in range(2020,2026):
    def get(geo,metric):
        q=b[b.geography.eq(geo)&b.period.astype(str).eq(str(year))&b.metric.eq(metric)]
        assert len(q)<=1
        return q.iloc[0] if len(q) else None
    can=get('Canada',senate); ab=get('Alberta',abmetric); stock=get('Alberta',stockmetric)
    allocation=pal[pal.province.eq('Alberta')&pal.year.eq(year)]
    annual.append({'year':year,'pal_regime':'Before PAL' if year<2024 else 'PAL era (from January 22, 2024)',
        'canada_holders_excluding_extensions':can.student_count if can is not None else pd.NA,
        'alberta_postsecondary_permit_effective_holders':ab.student_count if ab is not None else pd.NA,
        'alberta_december_31_permit_stock_old_vintage':stock.student_count if stock is not None else pd.NA,
        'alberta_pal_application_allocation':allocation.application_spaces.iloc[0] if len(allocation) else pd.NA,
        'allocation_status':'Not applicable: PAL system not introduced' if year<2024 else 'Planned application spaces, not actual admissions',
        'national_measure_note':'Initial permit-holder series excluding extensions; arrival-relevant administrative measure, not a harmonized border-crossing census.',
        'alberta_measure_note':'DLI permit-effective holders include extensions; not new arrivals. Alberta annual new arrivals not located.',
        'canada_source_url':can.source_url if can is not None else '',
        'alberta_source_url':ab.source_url if ab is not None else '',
        'pal_source_url':allocation.source_url.iloc[0] if len(allocation) else ''})
a=pd.DataFrame(annual)
for col in ['canada_holders_excluding_extensions','alberta_postsecondary_permit_effective_holders','alberta_december_31_permit_stock_old_vintage','alberta_pal_application_allocation']:
    a[col]=pd.to_numeric(a[col],errors='raise').astype('Int64')
a.to_csv(C/'pal_before_after_annual_counts.csv',index=False,encoding='utf-8-sig')

matrix=[]
for _,row in a.iterrows():
    matrix.append({'date_or_period':str(row.year),'row_type':'Annual baseline' if row.year<2024 else 'Annual observed outcomes',
        'event_or_observation':row.pal_regime,
        'canada_count':row.canada_holders_excluding_extensions,'canada_metric':'All study levels: annual study permit holders excluding extensions (Senate S-32 vintage)',
        'alberta_count':row.alberta_postsecondary_permit_effective_holders,'alberta_metric':'Post-secondary DLI permit-effective holders, including extensions',
        'policy_or_institution_number':f'Alberta application allocation {row.alberta_pal_application_allocation}' if pd.notna(row.alberta_pal_application_allocation) else 'PAL: not applicable',
        'affected_cohort':'National initial holders and Alberta DLI permit-effective holders are DIFFERENT populations',
        'what_this_tells_us':'Descriptive annual comparison; not an estimate of the causal PAL effect.',
        'limitations':'Do not compare national/Alberta counts as matching arrivals. 2020 affected by pandemic travel restrictions; 2024 starts before Jan22 implementation.',
        'source_url':' | '.join(x for x in [row.canada_source_url,row.alberta_source_url,row.pal_source_url] if x),
        'evidence_type':'Published administrative counts',
        'short_quote':''})
for _,row in events.iterrows():
    matrix.append({'date_or_period':row.date,'row_type':'Policy event or institutional disclosure',
        'event_or_observation':row.event,'canada_count':pd.NA,'canada_metric':'','alberta_count':pd.NA,'alberta_metric':'',
        'policy_or_institution_number':row.measured_number,'affected_cohort':row.affected_cohort,
        'what_this_tells_us':row.mechanism,'limitations':row.limitations,'source_url':row.url,
        'evidence_type':row.evidence_strength,'short_quote':row.quote})
matrix.append({'date_or_period':'2026-01 to 2026-07','row_type':'Partial-year observed outcomes',
    'event_or_observation':'Latest available administrative period; not full-year 2026',
    'canada_count':28200,'canada_metric':'Revised explicit new student arrivals, January-July',
    'alberta_count':8505,'alberta_metric':'Post-secondary DLI permit-effective holders, January-July',
    'policy_or_institution_number':'Alberta 2026 allocation: 32,271 application spaces',
    'affected_cohort':'Different national-arrival and provincial-DLI populations',
    'what_this_tells_us':'Incomplete period; cannot calculate a full-year quota utilization rate.',
    'limitations':'Do not splice current arrivals with Senate series or annualize partial totals.',
    'source_url':b[b.metric.eq('IRCC revised new student arrivals')].source_url.iloc[0]+' | '+b[b.metric.eq(abmetric)].source_url.iloc[0],
    'evidence_type':'Published partial-year administrative counts','short_quote':''})
matrix.append({'date_or_period':'2020-10-20','row_type':'Pre-PAL context',
    'event_or_observation':'COVID travel exemption expanded for students attending DLIs with approved readiness plans',
    'canada_count':pd.NA,'canada_metric':'','alberta_count':pd.NA,'alberta_metric':'',
    'policy_or_institution_number':'No PAL system', 'affected_cohort':'International students travelling during pandemic restrictions',
    'what_this_tells_us':'2020 is an unusual pre-PAL baseline, not a normal recruitment benchmark.',
    'limitations':'No numerical causal effect estimated.',
    'source_url':'https://www.canada.ca/en/immigration-refugees-citizenship/news/2020/10/update-on-travel-restriction-exemptions-for-international-students.html',
    'evidence_type':'Verified historical policy','short_quote':''})
m=pd.DataFrame(matrix).sort_values('date_or_period',kind='stable')
for col in ['canada_count','alberta_count']:m[col]=pd.to_numeric(m[col],errors='raise').astype('Int64')
m.to_csv(C/'pal_before_after_event_matrix.csv',index=False,encoding='utf-8-sig')
u['percentage_interpretation']=u.rate_status
# Explicitly render a reported upper bound rather than exporting an apparent exact 50%.
def rate_label(row):
    if pd.isna(row.percentage):return 'Not established'
    if 'bound' in str(row.rate_status).lower() or 'less than' in str(row.rate_status).lower():return '<'+str(round(row.percentage,2))+'% (reported bound)'
    return str(round(row.percentage,2))+'% ('+str(row.rate_status)+')'
u['display_percentage']=u.apply(rate_label,axis=1)
u.to_csv(C/'pal_university_utilization_evidence.csv',index=False,encoding='utf-8-sig')
events.to_csv(C/'pal_policy_events_and_drivers.csv',index=False,encoding='utf-8-sig')
b.to_csv(C/'pal_baseline_source_observations.csv',index=False,encoding='utf-8-sig')
checks={
 'baseline_six_years':a.year.tolist()==list(range(2020,2026)),
 'pre_pal_allocation_missing_not_zero':a.loc[a.year<2024,'alberta_pal_application_allocation'].isna().all(),
 'event_rows_preserved':len(m)==len(events)+8,
 'matrix_numeric_counts_nonnegative':not (m[['canada_count','alberta_count']]<0).any().any(),
 'all_source_urls_present':m.source_url.str.startswith('http').all(),
 '2025_counts_match_senate_and_dli':int(a.loc[a.year.eq(2025),'canada_holders_excluding_extensions'].iloc[0])==115460 and int(a.loc[a.year.eq(2025),'alberta_postsecondary_permit_effective_holders'].iloc[0])==17250,
}
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values()),checks
(OUT/'matrix_validation.json').write_text(json.dumps({'matrix_rows':len(m),'events':len(events),'utilization_evidence_rows':len(u),'checks':checks},indent=2))
print(json.dumps({'matrix_rows':len(m),'events':len(events),'checks':checks},indent=2))
