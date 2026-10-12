YEAR-BY-YEAR STUDENT COUNTS -- START HERE

annual_enrolment_canada_alberta.csv
  One row for each academic year, 2019-2020 through 2024-2025.
  Columns distinguish Alberta annual unique headcount (LERS), Alberta fall
  program enrolments (PSIS), and Canada fall program enrolments (PSIS).
  Alberta's share of Canada uses ONLY the matching PSIS measures.

annual_student_count_outline.csv
  53 labelled observations across the available annual/snapshot series.
  Calendar 2020-2025 and January-July 2026 permit-effective holders, older
  year-end permit stock, revised national stock, and academic-year enrolment.
  Each row records geography, period, metric, count, coverage, population,
  interpretation and source. This is an index of separate measures, not a
  table whose rows should be summed. No 2026 full-year total is inferred.

annual_alberta_enrolment_by_institution.csv
  26 institutions, with one count column per academic year.
  Institution headcounts overlap; use the published system total in the
  overview for the number of unique students in the reporting system.

annual_alberta_enrolment_by_study_level.csv
  21 credential/program combinations, with one column per academic year.
  Includes bachelor's, master's, doctoral, diploma and certificate categories.
  Credential/program memberships overlap. Blank is unavailable, not zero.

LATEST COMPLETE ENROLMENT YEAR
  2024-2025 is the latest complete academic year in the collected comparable
  series. Later isolated institutional reports are not a complete provincial
  annual dataset. Do not fill 2025-2026 enrolment with permit-holder figures.

IMPORTANT DEFINITIONS
  LERS: annual international headcount in Alberta reporting institutions and
  their approved programs. Reporting changes apply: Athabasca's 2024-2025
  window spans 16 months; NorQuest repeats spring 2024; MaKami joins reporting.
  PSIS: international program enrolments at a fall snapshot, not unique people.
  IRCC: study permit holders, not proof of current attendance or PAL receipt.
  Stocks and flows, fiscal/calendar/academic years, and differing vintages
  remain separate. PAL allocations are not student counts.

REPRODUCE AND VALIDATE
  Run ../../scripts/build_annual_outline.py after the main cleaning pipeline.
  Validation: ../annual_outline_validation.json and ../annual_outline_qa.txt.
  The existing source files are unchanged; all annual observations are copied
  from published totals or corresponding detail rows, never summed from months.
