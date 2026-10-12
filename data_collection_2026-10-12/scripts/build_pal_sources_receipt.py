from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'analysis/cleaned';D=ROOT/'analysis/pal_interpretation'
def query(qid,label,file,columns,definition,period,caveats,df=None):
    if df is None:df=pd.read_csv(file)
    return {'id':qid,'source':{'label':label,'files':[{'label':file.name}],
        'metricDefinitions':[{'label':label,'definition':definition}],'caveats':caveats},
        'reportingPeriod':period,'columns':columns,'rows':json.loads(df[columns].to_json(orient='records'))}
items=[
 {'id':'university-pal-use','title':'What proportion of university PAL allocations was used?','queries':[
 query('usage-evidence','University disclosures',C/'pal_university_utilization_evidence.csv',
 ['entity','period','stage','numerator','denominator','display_percentage','limitation'],
 'Use is retained at the stage reported by each institution: endorsement, issuance or unspecified utilization.',
 '2024 activity reported in 2024–2025',
 ['These selected institutions are not a representative sample.','Calgary and Lethbridge do not have validated same-period numerical utilization rates in the retrieved sources.','Manitoba is a less-than-50% bound; Toronto is an all-used statement without counts.'])]},
 {'id':'before-after-students','title':'Student numbers before and after PAL introduction','queries':[
 query('annual-counts','IRCC national and Alberta series',C/'pal_before_after_annual_counts.csv',
 ['year','canada_holders_excluding_extensions','alberta_postsecondary_permit_effective_holders','alberta_pal_application_allocation'],
 'National counts exclude permit extensions; Alberta DLI permit-effective counts include extensions and have different scope.',
 'Calendar 2020–2025',
 ['No comparable public annual Alberta new-arrivals series was located.','National initial-holder and Alberta DLI counts must not be divided to estimate Alberta’s share of arrivals.','PAL did not exist before January 22, 2024; missing allocations are not zero.','2020 was affected by pandemic travel restrictions.'])]},
 {'id':'pal-policy-timeline','title':'Policy events and graduate allocation interpretation','queries':[
 query('events','Official policy and institutional records',C/'pal_policy_events_and_drivers.csv',
 ['date','event','affected_cohort','measured_number','evidence_strength','limitations'],
 'The timeline distinguishes policy effective dates, announcements and institutional reports.',
 'January 2024–September 2026',
 ['Verified policy mechanisms do not establish quantified causal effects on admissions.','Master’s and doctoral PAL coverage changed in 2024, 2025 and 2026.','The financial-threshold historical-date discrepancy is retained in the detailed matrix.'])]},
 {'id':'shortfall-drivers','title':'Fewer applications and lower approval yield','queries':[
 query('audit-outcomes','Auditor General study-permit cohorts',D/'audit_new_permit_outcomes.csv',
 ['year','applications_received','applications_approved','approval_yield_pct','period_scope'],
 'Approval yield is approvals divided by applications received in the audit’s post-secondary application cohorts.',
 '2022–2024 and January–September 2025',
 ['This is not university PAL utilization.','The audit excludes primary and secondary schools and follows application-received cohorts.','2025 remains partial and includes pending applications.','The audit did not establish why approval yields fell; a descriptive decomposition is not a causal attribution.'])]}]
(D/'answer_sources.json').write_text(json.dumps({'schemaVersion':1,'items':items},ensure_ascii=False,indent=2),encoding='utf-8')
