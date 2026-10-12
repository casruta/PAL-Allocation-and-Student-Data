PAL ALLOCATIONS, UNIVERSITY ADMISSIONS AND BEFORE/AFTER MATRIX
Research cutoff: 12 October 2026 UTC.

DELIVERABLES
../pal_allocation_admissions_and_timeline.ipynb
  Executed narrative analysis, usage table, annual comparisons, dated event
  matrix, driver discussion and reproducible accounting sensitivity.
../cleaned/pal_before_after_event_matrix.csv
  29 rows: 21 material policy/institutional-report events, six annual count
  comparisons (2020-2025), a partial January-July2026 row and pandemic context.
../cleaned/pal_before_after_annual_counts.csv
  Six-year national initial-holder and Alberta DLI context, with separate
  metrics, old-vintage stock and application allocations.
../cleaned/pal_university_utilization_evidence.csv
  13 evidence rows, with stage, numerator/denominator where available, reported
  percentages/bounds, dates, quotation, source and limitations.
../cleaned/pal_policy_events_and_drivers.csv
  21 dated events with affected cohorts, numbers, mechanisms and evidence type.
../cleaned/pal_baseline_source_observations.csv
  77 individually labelled baseline/current observations across separate series.

MAIN CONCLUSIONS
- Underuse is institution-specific. Calgary reports underuse without a rate;
  Saskatchewan reports54.9% endorsed byDec3,2024; Manitoba reports<50%; Toronto
  reportsallused(100%). These stages/periods are not interchangeable.
- Toronto used all2024PALallocation but intake was6%belowfall2023, showing that
  quota use does not guarantee arrivals or enrolment targets.
- PAL quotas are application capacity. They do not identify academic quality,
  university admission thresholds, or actual MA/PhD admissions.
- Alberta2025graduateplanningallocation was5256/47338=11.1%; graduate exemptions
  in2024, inclusionJan22,2025, and public-DLI exemptionJan1,2026 change coverage.
- National holders excluding extensions were495860(2023),293260(2024),115460(2025)
  in the same Senate-source vintage. Alberta DLI permit-effective holders were
  29630,25570,17250; these include extensions and are NOT Alberta arrivals.
- No harmonized public annual Alberta new-arrivals series was located.
- Fewer applications and lower conversion into approvals are observed. The
  effects of finances, family work, PGWP, processing routes and timing cannot
  be assigned causal percentages from these aggregate data.

METHOD AND VALIDATION
Three bounded agent research tracks: university usage, pre-PAL baseline,
policy timeline/drivers. A subsequent independent review checked synthesis.
All six national initial-holder counts2020-25 checked against SenatePDFpage4;
Alberta counts checked against original IRCC annual total columns. OAG four-row
table checked againstExhibit3. Notebook executed6code cells,0erroroutputs.
matrix_validation.json records6passed structural/content checks.
independent_qa.txt records review results and limitations.

Audit accounting decomposition is order-dependent and noncausal. Both orders
and symmetric sensitivity are saved; no percentage is attributed to PAL policy.
2025 audit figures are only toSeptember and include pending decisions. No
decision-year/receipt-year Senate ratio is labelled a cohort approval rate.
Pre2024PALquota is not applicable, never0. FiscalPALissuance is not divided by
calendarallocation. Missing institutional usage remains unknown, not0.

SOURCE ARCHIVE AND REPRODUCTION
../../research/pal_interpretation contains the three research notes and tables.
baseline_raw has Senate originalPDF, text, SHA256/provenance and number checks.
raw_timeline has20official/university downloads with receipts and hashes.
Existing underlying IRCC workbooks and Alberta sources remain in ../../raw.
Separate retrieval receipts cover new sources; original collection manifest
continues to describe its earlier collection snapshot.

Run ../../scripts/build_pal_interpretation_notebook.py to rebuild matrices,
audit calculations and execute the notebook using saved sources. No network is
needed. The runtime uses the existing analysis/_dependencies and _kernels.
Standalone steps: build_pal_matrix.py and pal_diagnostic_calculations.py.

NEXT EVIDENCE NEEDED
Matched institution/intake/degree counts for allocation (including adjustments),
unique letters, replacements/cancellations, submitted applications, decisions,
arrivals and registration. Existing completed ATI packages are catalogued but
have not been obtained. No external requests or messages were sent.
