"""Project only the reviewed observations cited in the chat answer."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
T=ROOT/'analysis/tables'
def query(qid,label,filename,df,columns,definition,caveats,period,filters):
    return {'id':qid,'source':{'label':label,'files':[{'label':filename}],
        'metricDefinitions':[{'label':label,'definition':definition}],
        'filters':filters,'caveats':caveats},'reportingPeriod':period,
        'columns':columns,'rows':json.loads(df[columns].to_json(orient='records'))}

pal=pd.read_csv(T/'alberta_pal_allocations_2024_2026.csv')
ev=pd.read_csv(T/'alberta_pal_actuals_and_evidence.csv')
ev=ev[ev.metric.isin(['PALs issued by provincial portal','PALs issued'])]
degree=pd.read_csv(T/'statcan_degree_by_institution_2024_25.csv')
degree=degree[degree.geography_and_institutions.isin(['University of Alberta, Alberta','University of Calgary, Alberta','University of Lethbridge, Alberta'])&degree.international_standard_classification_of_education_isced.ne("Bachelor's or equivalent")]
lers=pd.read_csv(T/'alberta_degree_enrolment_trend.csv');lers=lers[lers.academic_year.eq('2024-2025')]
permit=pd.read_csv(T/'alberta_postsecondary_permit_effective_totals.csv');permit=permit[permit.row_type.eq('province_total')&permit.year.isin([2024,2025])]
cit=pd.read_csv(T/'alberta_citizenship_profile_2025.csv');cit=cit[cit.country_of_citizenship.eq('India')&cit.institution_type.isin(['University','College'])]
items=[{'id':'alberta-pal-evidence','title':'Alberta PAL allocations and reported issuance','queries':[
 query('pal-allocation','IRCC PAL allocations','pal_provincial_allocations_2024_2026.csv',pal,
 ['year','application_spaces','graduate_application_spaces'],'Allocation counts planned PAL-required application spaces, not actual recipients.',
 ['Graduate exemptions changed between 2024, 2025 and 2026.','The 2025 graduate category combines master’s and doctoral students.'], '2024–2026',['Province: Alberta']),
 query('pal-issued','Official PAL issuance disclosures','alberta_pal_actuals_and_evidence.csv',ev,
 ['entity','period','metric','value'],'Issuance counts letters reported by the provincial portal or institution.',
 ['Fiscal provincial issuance and calendar institutional issuance have different periods.','Letters issued do not establish submissions or approvals.'], 'Fiscal 2024–25 and calendar 2024',['Entities: Alberta and University of Lethbridge'])]},
 {'id':'graduate-student-context','title':'Graduate enrolment by level and Alberta institution','queries':[
 query('lers-degree','Alberta annual headcount','alberta_degree_enrolment_trend.csv',lers,
 ['program_type','headcount','system_headcount'],'Annual headcount covers international students in Alberta reporting institutions’ approved programs.',
 ['Enrolment is not PAL or permit receipt.','Program and institution memberships overlap.','Reporting changes affect comparisons across years.'], 'Academic 2024–25',['Learner category: International']),
 query('psis-degree','Statistics Canada PSIS','statcan_degree_by_institution_2024_25.csv',degree,
 ['geography_and_institutions','international_standard_classification_of_education_isced','value'],'PSIS counts fall-snapshot program enrolments by ISCED equivalent level.',
 ['Program enrolments are not unique people or PAL recipients.','Counts are randomly rounded to three.','Master’s-equivalent is not MA-only; doctoral-equivalent is not PhD-only.'], 'Fall snapshot 2024–25',['Status: International students','Institution type: Total','Registration status: Total','Instructional program: Total','Gender: Total','Institutions: Alberta, Calgary and Lethbridge universities'])]},
 {'id':'permit-profile','title':'Permit-effective holders and citizenship profile','queries':[
 query('permit-totals','IRCC Alberta DLI totals','alberta_postsecondary_permit_effective_totals.csv',permit,
 ['year','value'],'Permit-effective holders are people whose study permits became effective during the stated year.',
 ['This series does not isolate new approvals or current students.','Values are rounded to five.'], 'Calendar 2024 and 2025',['Province: Alberta','Row type: Published province total']),
 query('citizenship','IRCC institution-type citizenship','alberta_citizenship_profile_2025.csv',cit,
 ['institution_type','country_of_citizenship','value','published_type_total','share_of_type_pct'],'Citizenship share divides a rounded country count by the published institution-type total.',
 ['Citizenship is not ethnicity, residence or birthplace.','College and Career College are distinct categories.','These are not degree-specific PAL recipients.'], 'Calendar 2025',['Province: Alberta','Citizenship: India','Institution types: University and College'])]}]
(ROOT/'analysis/answer_sources.json').write_text(json.dumps({'schemaVersion':1,'items':items},ensure_ascii=False,indent=2),encoding='utf-8')
inventory=[]
for f in sorted((ROOT/'analysis/cleaned').glob('*.csv')):
    d=pd.read_csv(f)
    inventory.append({'file':f.name,'rows':len(d),'columns':len(d.columns)})
pd.DataFrame(inventory).to_csv(ROOT/'analysis/cleaned_file_inventory.csv',index=False)
print({'cleaned_files':len(inventory),'rows':sum(x['rows'] for x in inventory)})
