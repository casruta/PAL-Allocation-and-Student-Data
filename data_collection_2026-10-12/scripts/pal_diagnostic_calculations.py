"""Bounded accounting decomposition; these are NOT causal effects or PAL usage."""
from pathlib import Path
import pandas as pd
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/pal_interpretation'
OUT.mkdir(parents=True,exist_ok=True)
url='https://www.canada.ca/en/immigration-refugees-citizenship/corporate/transparency/committees/cimm-apr-20-2026/oag-report.html'
d=pd.DataFrame([
    [2022,624627,336981,None,'Full application-received year'],
    [2023,792200,456690,None,'Full application-received year'],
    [2024,363007,149559,348900,'Full application-received year'],
    [2025,134195,50370,255360,'Partial: as of September 2025; about 26,000 pending new applications'],
],columns=['year','applications_received','applications_approved','forecast_approved','period_scope'])
d['approval_yield_pct']=100*d.applications_approved/d.applications_received
d['forecast_attainment_pct']=100*d.applications_approved/d.forecast_approved
d['population']='New post-secondary study permit applications; excludes primary/secondary; application-received cohort'
d['interpretation']='Approval yield is approved/received at audit cutoff, not final decision-only approval probability. Not PAL allocation utilization.'
d['source_url']=url
d['source_location']='Exhibit 3 and paragraphs 7, 14-18'
d.to_csv(OUT/'audit_new_permit_outcomes.csv',index=False)
a0,a1,p0,p1=792200,363007,456690,149559
r0,r1=p0/a0,p1/a1
volume=(a1-a0)*r0
yield_component=a1*(r1-r0)
result={
    'comparison':'2023 to 2024, audit application-received cohorts',
    'applications_change_pct':100*(a1/a0-1),
    'approvals_change_pct':100*(p1/p0-1),
    'approvals_change':p1-p0,
    'volume_component_at_2023_yield':volume,
    'yield_component_at_2024_volume':yield_component,
    'volume_component_share_pct':100*volume/(p1-p0),
    'yield_component_share_pct':100*yield_component/(p1-p0),
    'reverse_order_volume_share_pct':100*((a1-a0)*r1)/(p1-p0),
    'reverse_order_yield_share_pct':100*(a0*(r1-r0))/(p1-p0),
    'symmetric_volume_share_pct':100*((a1-a0)*(r0+r1)/2)/(p1-p0),
    'symmetric_yield_share_pct':100*((a0+a1)/2*(r1-r0))/(p1-p0),
    'identity':'Delta approvals = (A2024-A2023)*r2023 + A2024*(r2024-r2023)',
    'interpretation':'Sequential accounting decomposition, volume first. Order-dependent; not a causal attribution to PALs or policy changes. Pending decisions can affect yield.',
    'source_url':url}
assert abs(volume+yield_component-(p1-p0))<1e-6
(OUT/'audit_decomposition.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
