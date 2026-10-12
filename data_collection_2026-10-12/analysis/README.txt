ALBERTA IRCC / PAL PRELIMINARY ANALYSIS
Prepared 12 October 2026 UTC. Research meaning confirmed: PAL letters and study permits.

START HERE
alberta_ircc_preliminary_analysis.ipynb -- executed notebook with findings, source
links, tables, two figures, cleaning decisions and interpretation limits.
cleaned/ -- 29 analysis-ready CSVs, including annual outlines and PAL matrices. Originals remain under ../raw/ and prior
extracts remain under ../extracted/ and ../focus_2020_latest/.
tables/ -- selected trend, institution, degree, field, citizenship and PAL tables.
figures/ -- readable PNG exports from the notebook.
cleaned/ANNUAL_OUTLINE_README.txt -- start here for the year-by-year totals and
distributions by institution and credential; latest complete enrolment 2024-25.
pal_interpretation/README.txt -- university PAL usage, pre/post counts, and
29-row dated event matrix; accompanying executed interpretation notebook.
validation_checks.json -- machine-readable checks and retained source discrepancy.
independent_analysis_qa.txt -- independent reviewer findings and limitations.
notebook_execution.json -- executed cells and error-output count.
cleaning_profile.csv -- input hashes, keys, row counts and missing values for the
15 original focused files. New degree/citizenship files have separate provenance
and validation in ../raw/degree_detail/ and citizenship_extraction_notes.txt.

KEY FINDINGS
1. Actual PAL recipients by university x master's/doctoral level remain unknown
   in the retrieved public data. Allocation, issuance, submission, approval and
   enrolment are different measures. No individual recipient names are present.
2. Alberta's 2025 graduate allocation is 5,256 application spaces, master's and
   doctoral combined, out of 47,338 (11.1%). Expected permits are plans, not actuals.
3. Alberta disclosed 26,089 portal-issued PALs in fiscal 2024-25. Lethbridge
   disclosed 1,784 letters issued in 2024; actual submissions are not established.
4. Alberta annual international enrolment was 50,164 in 2024-25, with master's
   headcount 4,747 and doctoral 2,875. This is annual LERS enrolment context.
5. PSIS fall 2024/25 enrolment context provides institution and degree detail:
   UAlberta master's-equivalent 2,058, doctoral-equivalent 1,512;
   UCalgary 2,142 and 909; ULethbridge 87 and 51.
   These are program counts, not individual PAL/permit recipients.
6. IRCC's 2025 permit-effective-year DLI counts include UAlberta 3,615,
   UCalgary 2,580 and ULethbridge 500. They do not isolate initial approvals.
7. Alberta university permit-effective holders in 2025 include India 1,580 and
   China 1,550, out of published University total 8,075. In the separate College
   category India is 4,830 of 8,840. Career College is another separate type.

CLEANING AND DATA DICTIONARY
value/headcount: published counts; nullable integers. Missing/suppressed is not 0.
value_raw: original string, including -- suppression where supplied by IRCC.
source_file/source_sheet/source_cell/source_row: trace back to preserved original.
source_url: publisher URL; snapshot dates are retrieval dates, not data periods.
record_role/row_type: total, subtotal or detail. Never add total rows to detail.
year/academic_year/ref_date: distinct reporting conventions, not join equivalents.
period/partial_year/period_complete: 2026 administrative data are January-July.
coordinate/vector: Statistics Canada identifiers for a series at exact dimensions.
status/symbol and API status codes: source missingness/reliability flags retained.
share_of_type_pct: rounded country count / published type total x 100.
share_of_system_pct: membership count / annual system headcount x 100; groups overlap.
graduate_share_of_allocation_pct: graduate application spaces / all spaces x 100.

No suppressed value imputation, outlier deletion, cross-source person matching,
or inference of PAL receipt was performed. Labels retain publisher meaning.
Master's is not MA-only. Doctoral-equivalent is not an exact PhD-only category.
Graduate certificates and diplomas are not master's degrees.

MATERIAL COMPARABILITY LIMITS
- PAL system starts in 2024. Earlier years are not applicable, not zero.
- Master's/doctoral applicants generally exempt in 2024, included Jan22 2025,
  public-DLI degree programs exempt again Jan1 2026; other exemptions apply.
- LERS is annual headcount in reporting institutions' approved programs. PSIS
  is fall-snapshot program enrolment, randomly rounded to 3. IRCC holders are
  rounded to 5 and do not establish current attendance or physical residence.
- LERS institution totals sum to 50,606 vs deduplicated system 50,164. Do not
  repair this legitimate overlap by altering institution counts.
- Athabasca has a 16-month 2024-25 reporting window; NorQuest repeats spring
  2024 in adjacent years; MaKami first reports in 2024-25. Earlier changes also
  exist in the original reporting-change sheet.
- Federal 2024 allocation rows sum one below the printed national total.
  The 2025 prose expected-permit total 316,267 differs from table 316,276.
- Old year-end IRCC stock and newer monthly stock have different scopes/vintages.
  Fiscal-year PAL issuance cannot be divided by calendar-year allocation.

REPRODUCTION
Run ../scripts/preliminary_analysis.py to regenerate cleaned tables and checks.
Run ../scripts/build_annual_outline.py after cleaning for the annual outlines.
Run ../scripts/extract_citizenship.py for the source-cell citizenship extraction.
Run ../scripts/build_analysis_notebook.py to rebuild and execute the notebook.
The notebook executes from this analysis folder. It uses pandas, openpyxl,
matplotlib, nbformat, nbclient and ipykernel; additional notebook packages are
installed locally under _dependencies. _kernels and _matplotlib are runtime files.
No network is needed for these analysis runs. Acquisition scripts are in ../scripts
and ../raw/degree_detail; public sources can revise, so use saved snapshots for
exact reproduction. Degree provenance and independent API/bulk comparison:
../raw/degree_detail/provenance.json and validation.json (827/827 numeric matches).

NEXT EVIDENCE TO OBTAIN
Completed ATIP summaries already saved under ../research/atip identify detailed
degree/outcome extracts: A-2024-01082, 2A-2023-48155, A-2024-63937, A-2025-66824,
and Alberta-specific A-2025-84005. The released packages have not been obtained;
requested detail is not proof it was supplied. For PAL usage, provincial records
need separate allocated/issued/submitted/cancelled counts by DLI, degree and month.
No requests or external messages have been sent.
