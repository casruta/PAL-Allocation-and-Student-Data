"""Execute the PAL interpretation and before/after evidence notebook."""
from pathlib import Path
import sys,os,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis'
DEPS=OUT/'_dependencies'
sys.path.insert(0,str(DEPS))
os.environ['PYTHONPATH']=str(DEPS)+os.pathsep+os.environ.get('PYTHONPATH','')
import nbformat as nbf
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
cells=[]
def md(s):cells.append(nbf.v4.new_markdown_cell(s))
def code(s):cells.append(nbf.v4.new_code_cell(s))
md("""# What PAL allocations tell us about university admissions
Research cutoff: 12 October 2026. Three bounded research tracks covered university usage, pre-PAL student numbers, and policy events; a separate review checked the synthesis.

**Answer:** Some universities underused their PAL allocation, but underuse was not universal and Alberta university percentages are mostly undisclosed. A PAL is permission to submit a study-permit application within an allocation. It does not reveal academic admission standards, prove a visa approval, or count a student arrival.

In 2025 Alberta's graduate allocation was **5,256 of 47,338 spaces (11.1%)**. This describes a planning category combining master's and doctoral applicants, not the share of actual admitted or enrolled students. Other spaces are not exclusively university undergraduate places. Graduate exemptions changed across years, making the PAL population itself unstable.

The useful sequence is **admission offer → PAL issued/endorsed → permit application submitted → approved → student arrives → enrols**. The data do not link these stages person-by-person. Some university-admitted students are PAL-exempt; replacement letters and deferrals can also complicate letter counts. A quota can be fully used without meeting enrolment targets.
""")
code("""from pathlib import Path
import pandas as pd, json, runpy
from IPython.display import display
ROOT=Path.cwd().parent
assert (ROOT/'research/pal_interpretation').exists()
runpy.run_path(str(ROOT/'scripts/build_pal_matrix.py'))
runpy.run_path(str(ROOT/'scripts/pal_diagnostic_calculations.py'))
C=ROOT/'analysis/cleaned'
R=ROOT/'research/pal_interpretation'
D=ROOT/'analysis/pal_interpretation'
pd.options.display.max_colwidth=130
pd.options.display.max_rows=40
pd.options.display.float_format='{:,.2f}'.format
""")
md("""## What percentage of the university quota was used?

| University | Defensible 2024 usage statement | What it actually measures |
|---|---|---|
| Calgary | Underused; exact percentage unknown | Institutional qualitative statement; no matched counts |
| Lethbridge | 1,784 PALs issued; exact utilization unknown | The 2,687 allocation has a differently specified period; do not headline 66.4% |
| Saskatchewan | 1,623 / 2,958 = **54.9%** as of December 3 | Endorsements against allocation; not confirmed IRCC submissions |
| Manitoba | **Less than 50%** of 7,540 | Institution-reported bound, not an exact rate |
| Toronto | **100% reported used** | All-used statement; counts and processing stage unspecified |
| McMaster | **90% issued; 70% reported utilization** | Institutional account with incomplete denominator definitions |

These are selected disclosures, not a representative national league table. Toronto's full PAL use coexisted with international intake 6% below fall 2023 and 978 below target, showing that allocation use and enrolment performance are different.

For Alberta overall, **26,089 portal-issued PALs in fiscal 2024–25** cannot be divided by a calendar-year allocation. Nor is the audit's **25% of forecast approvals achieved by September 2025** an Alberta university PAL utilization rate: it is a different provincial measure covering new permits and extensions.
""")
code("""u=pd.read_csv(C/'pal_university_utilization_evidence.csv')
display(u[['entity','period','stage','numerator','denominator','display_percentage','limitation','source_url']])
assert abs(1623/2958*100-54.8681541582)<0.0001
""")
md("""## Before PAL: how many students came to Canada, and what do we know for Alberta?
An official IRCC Senate response provides annual **study permit holders excluding extensions**. It is an entry-relevant measure: the response explains confirmation and printing of a permit by CBSA on arrival. We retain the precise source label rather than relabel it a harmonized border-crossing count. The series covers all study levels, not universities alone.

No comparable public annual **Alberta new-arrivals** series was located. Alberta's DLI permit-effective holder series includes extensions; it is shown as context, not as the Alberta portion of the national initial-holder series. The columns below must not be divided to calculate Alberta's share of new arrivals.

2020 was affected by COVID travel restrictions, so 2023 is the more useful immediate pre-PAL comparison. Academic 2023–24 overlaps PAL introduction; fall 2023 is pre-PAL, but the entire academic year is not.

Sources: [IRCC Senate S-32 response, page 4](https://sencanada.ca/media/yzjh5dlm/clrk_tabling_2026-04-02_senate-question-n-32-1_downe_b_e.pdf), [IRCC Alberta DLI workbook](https://www.ircc.canada.ca/opendata-donneesouvertes/data/EN_ODP-TR-Study-DLI_name_PT_Admin_type.xlsx), [2020 travel changes](https://www.canada.ca/en/immigration-refugees-citizenship/news/2020/10/update-on-travel-restriction-exemptions-for-international-students.html).
""")
code("""annual=pd.read_csv(C/'pal_before_after_annual_counts.csv')
display(annual[['year','canada_holders_excluding_extensions','alberta_postsecondary_permit_effective_holders','alberta_december_31_permit_stock_old_vintage','alberta_pal_application_allocation']])
before=annual.set_index('year').loc[2023]
after=annual.set_index('year').loc[2025]
display(pd.DataFrame([
 {'measure':'Canada holders excluding extensions','2023':before.canada_holders_excluding_extensions,'2025':after.canada_holders_excluding_extensions,'change_pct':100*(after.canada_holders_excluding_extensions/before.canada_holders_excluding_extensions-1)},
 {'measure':'Alberta DLI permit-effective holders incl extensions','2023':before.alberta_postsecondary_permit_effective_holders,'2025':after.alberta_postsecondary_permit_effective_holders,'change_pct':100*(after.alberta_postsecondary_permit_effective_holders/before.alberta_postsecondary_permit_effective_holders-1)}]))
""")
md("""National initial holders declined from **495,860 in 2023 to 293,260 in 2024 and 115,460 in 2025**, using the same Senate-source vintage. Alberta's narrower DLI permit-effective count declined from **29,630 to 25,570 and 17,250**. These are descriptive before/after changes, not the causal effect of PAL alone.

The newer explicit-arrivals dashboard reports 292,875 nationally in 2024, 114,975 in 2025 and 28,200 in January–July 2026. These differ slightly from the Senate vintage; both are retained separately. There is no full-year 2026 actual yet in this collection. Do not interpret the two vintages as contradictory counts of an identical fixed population without further reconciliation.

Existing enrolment context remains available in the cleaned files: Alberta annual headcount rose from 37,076 in 2022–23 to 48,311 in 2023–24 and 50,164 in 2024–25. Multi-year continuing students, reporting periods and scope mean enrolment need not move with new arrivals immediately; reporting changes also limit interpretation.
""")
md("""## Dated matrix: baseline numbers and important subsequent events
The downloadable matrix combines annual observations with **21 material policy/reporting events** and a pandemic context row. Event rows preserve announcement/effective/reporting dates, affected cohorts, exact numerical context, sources and interpretation limits. Empty numeric cells mean that an event is not a student-count observation. Annual numbers must not be read as measurements on each policy date.

The chronology includes Alberta's first PAL issuance on March 1, 2024; initial graduate exemptions; graduate inclusion from January 22, 2025; public-institution graduate exemption from January 1, 2026; financial requirements; PGWP, family work and processing-route changes; and the published provincial allocations.
""")
code("""m=pd.read_csv(C/'pal_before_after_event_matrix.csv')
display(m[['date_or_period','event_or_observation','canada_count','alberta_count','policy_or_institution_number','affected_cohort','limitations']])
print('Every row has its source URL in the downloadable CSV. Full matrix rows:',len(m))
""")
md("""## Why might allocations remain unused?

**1. Fewer prospective applicants reach the PAL/application stage.** Calgary reported roughly 40% fewer international applications in 2024 and attributed the drop and unused allocation to the visa/PAL process. This is the university's explanation, not an independent causal estimate. [Calgary minutes, page 2](https://www.ucalgary.ca/secretariat/sites/default/files/teams/1/GFC/Standing%20Committee%20Minutes/GAPS/GAPS%20Approved%20Minutes%202025-01-22.pdf)

**2. Timing, expiry and deferral can interrupt conversion.** Alberta's first PALs were issued March 1, after the January 22 federal requirement. Universities also describe uncertainty over whether issued letters were submitted. These facts support a possible timing mechanism but do not quantify lost admissions.

**3. Fewer applications become permits.** The audit's national post-secondary cohorts show applications falling 54.2% from 2023 to 2024 and approvals falling 67.3%. Approved/received yield fell from 57.6% to 41.2%. Lower yield explains part of the permit shortfall arithmetically, but a refusal after a valid submission does not itself prove an unused PAL space. IRCC had not established why yields fell. The audit found higher financial requirements and letter verification did not explain the extent of the decline; unclear financial-document expectations occurred in 23 of 51 sampled financial refusals. [Audit, paragraphs 14–18](https://www.canada.ca/en/immigration-refugees-citizenship/corporate/transparency/committees/cimm-apr-20-2026/oag-report.html)

**4. The overall study proposition changed.** Savings requirements, spouse employment eligibility, PGWP rules and processing routes can affect affordability and willingness to apply. These are plausible mechanisms supported by verified rule changes, not measured causal contributions. Restrictions targeting college/non-degree programs must not be generalized to all university degrees. Housing capacity was a policy rationale; its contribution to underuse is not measured here.

**5. The denominator and eligible population changed.** 2024 excluded master's/doctoral applicants; 2025 included them subject to exceptions; 2026 exempts degree-granting master's/doctoral programs at public DLIs again. Lower PAL counts can coexist with graduate recruitment. Annual spaces cannot be carried forward, so unused allocation is not a bank of guaranteed future enrolments.
""")
code("""outcomes=pd.read_csv(D/'audit_new_permit_outcomes.csv')
display(outcomes[['year','applications_received','applications_approved','approval_yield_pct','forecast_approved','forecast_attainment_pct','period_scope']])
decomposition=json.loads((D/'audit_decomposition.json').read_text())
display(pd.DataFrame([{'method':'Volume first','volume_component_pct':decomposition['volume_component_share_pct'],'yield_component_pct':decomposition['yield_component_share_pct']},
 {'method':'Yield first','volume_component_pct':decomposition['reverse_order_volume_share_pct'],'yield_component_pct':decomposition['reverse_order_yield_share_pct']},
 {'method':'Symmetric average','volume_component_pct':decomposition['symmetric_volume_share_pct'],'yield_component_pct':decomposition['symmetric_yield_share_pct']}]))
print('Accounting sensitivity only. None of these percentages measures the causal contribution of PAL policy.')
""")
md("""## What can be concluded about admitted students?
The PAL figures identify an administrative allocation and, in 2025, a graduate-versus-other planning split. They cannot identify MA versus MSc/MBA/PhD actual recipients, admission standards, applicant quality, academic field, or nationality of the students admitted by each university. Existing degree/field and citizenship tables describe related populations; linking them to PAL awards would be an ecological inference unsupported by these sources.

Underuse at an institution suggests its allocation did not bind at the measured stage and date. It does not prove the university had no demand, that all eligible applicants could obtain visas, or that the institution should relax academic standards. Toronto's full use and lower intake is a concrete counterexample to treating PAL use as enrolment success. [Toronto planning paper, PDF page 11](https://governingcouncil.utoronto.ca/system/files/agenda-items/20250212_PB_03.pdf)

To calculate defensible Alberta university percentages, obtain a same-year, same-cohort table of allocation adjustments, unique letters issued, replacements/cancellations, letters attached to submitted applications, approvals/refusals/pending decisions, arrivals and registrations. Break out university, degree level and intake. Existing completed ATIP leads are saved in the research folder, but the released packages have not been obtained.

## Validation and unresolved source issues
The annual matrix copies published totals without summing months. No absent PAL quota before 2024 is recoded as zero. Fiscal issuance is not divided by calendar allocation. Reported upper bounds remain bounds. The national Senate initial-holder and current arrival series remain separate. The detailed timeline records a historical-date conflict for the 2025 financial threshold and distinguishes legal effective dates from later notices. Primary downloads and hashes are stored under `research/pal_interpretation`.
""")
code("""display(pd.DataFrame(json.loads((D/'matrix_validation.json').read_text())['checks'].items(),columns=['check','passed']))
print('Independent review:',(D/'independent_qa.txt').exists())
""")
nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'IRCC analysis Python','language':'python','name':'ircc-analysis'},'language_info':{'name':'python','version':sys.version.split()[0]}})
target=OUT/'pal_allocation_admissions_and_timeline.ipynb'
nbf.validate(nb);nbf.write(nb,target)
ks=OUT/'_kernels'/'ircc-analysis'
km=KernelManager(kernel_name='ircc-analysis',kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(ks.parent)]))
print('Executing PAL interpretation notebook',flush=True)
NotebookClient(nb,timeout=180,startup_timeout=45,km=km,resources={'metadata':{'path':str(OUT)}}).execute()
nbf.validate(nb);nbf.write(nb,target)
result={'executed_code_cells':sum(c.cell_type=='code' for c in nb.cells),'error_outputs':sum(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs),'file':target.name}
(OUT/'pal_interpretation/notebook_execution.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
