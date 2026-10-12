IRCC AND ALBERTA INTERNATIONAL STUDENT DATA COLLECTION
Retrieved 12 October 2026 (UTC)

Purpose
-------
Official online source files and traceable CSV extracts for Canadian international
student counts, Alberta institutions, provincial attestation letter (PAL)
allocations, and available evidence of actual issuance/use. Collection is the first
stage of the requested research; this is not a completed university PAL-use census.
The requested focus is calendar 2020 through the latest available period. For
academic data, 2019-20 through 2024-25 supplies six complete years; newer 2025-26
institutional reports and estimates are retained separately. Original files keep
their full histories. PALs began in2024: earlier PAL years are not applicable,
not zero usage or missing observations.

DEEPER SEARCH UPDATE
--------------------
Start with focus_2020_latest/ for the selected historical window. New sources:
  - Statistics Canada PSIS full cube and 2019/20-2024/25 extracts for every province.
  - Quarterly study-related usual-resident estimates, July2021-July2026.
  - IRCC's separate national monthly stock/arrivals series through July2026.
  - Modelled2025/26 enrolment estimates, with observed/modelled years distinguished.
  - Lethbridge2024 PAL issuance:1784, verified in February2025 GFC minutes.
  - MacEwan2025 expected PAL allocation:1500, explicitly an expectation.
  - Selected USask, Manitoba and McMaster PAL-use evidence with different definitions.
  - New2025/26 university reports; report dates are not necessarily metric dates.

research/source_coverage_log.csv shows routes checked, results and limitations.
research/institution_search_log.txt and research/provincial_search_notes.txt
document university and comparative searches. research/atip/README.txt explains
the completed federal disclosure search:592 broad student-related matches,
5PAL-specific summaries and14priority leads. These are summaries, NOT the
underlying released tables. No requests or external communications were sent.

Priority previously released-record leads:
  A-2024-02010:2024 PAL allotments to public/private colleges, including Alberta.
  A-2025-84005:Alberta DLI applications/approvals/refusals, Jan2024-Dec2 2025.
  A-2025-83996:University of Calgary initial-permit decisions during2025.
  2A-2021-02627:international-student records by DLI including Alberta2020/21.
Exact summaries, official URLs, completion dates and limitations are saved in
research/atip/priority_record_leads.csv. Requested scope is not proof every field
was supplied. Reported page counts describe the package, never student counts.

Access limits: UAlberta's indexed2024/25 report returned403 on download; an
indexed figure was not admitted to verified extracts. Calgary's public PowerBI
dashboard needs a functioning browser; no browser surface was connected. No
dashboard export was obtained. Search evidence does not prove data is absent.

New-series comparability notes:
  PSIS counts fall-snapshot PROGRAM enrolments, randomly rounded to3. Alberta's
  2024/25 total41007 differs from LERS50164 because scope/time/grain differ. Its
  university19461 and college21543 cells differ from the total by3 due to rounding.
  NPR data estimate usual residents; study-only, dual work/study, and asylum-related
  study categories are separate. July1 2026 is preliminary. These are not enrolments.
  IRCC's newer national stock series includes dual work/study holders but excludes
  asylum claimants/protected persons/related groups. It must not be spliced into
  the older broad year-end stock series as though scope/vintage were identical.
  May2026 modelled2024/25 estimates predate the October2026 observed PSIS release.
  Use the newer observed PSIS data for that PSIS population; retain the modelled
  2025/26 values as estimates only. Prairies totals are not Alberta totals.

extracted/extended_file_inventory.csv indexes the new/focused extracts.
extended_validation.json and research/extended_independent_qa.txt document the
new extraction checks; collection_validation.json covers all collected originals.

START HERE
----------
extracted/ircc_year_end_permit_holders.csv
  Canada and every province/territory, by study level, 2000-2024.
  Valid study permit holders on December 31; a stock measure.

extracted/ircc_permit_effective_year_province_study_level.csv
  Annual published totals, 2015-2025; January-July 2026 is partial.
  Holders by year the permit became effective; not a year-end stock.

extracted/ircc_alberta_institution_permit_effective_year.csv
  Alberta designated learning institutions (DLIs), public/private, 2016-2025,
  plus January-July 2026. Includes subtotal rows, identified by row_type.
  These are permit-holder counts, not PAL issuance or enrolment counts.

extracted/alberta_enrolment_by_sector_and_institution.csv
  International headcount for Alberta's reporting post-secondary system,
  2015-2016 through 2024-2025. Includes institutional, sector and system totals.
  Use the Status=Total rows for annual institutional headcounts. Do not add the
  institutional rows to estimate the unique system headcount.

extracted/pal_provincial_allocations_2024_2026.csv
  All provinces/territories; published application-space allocations and expected
  permit issuances. 2024 uses the final adjusted/top-up table, not the preliminary
  population-based scenario. Allocations are capacity, not actual usage.

extracted/pal_verified_evidence.csv
  Alberta portal PAL issuance; a Lethbridge allocation; Calgary's reported underuse.
  Includes brief quotations, source URLs and physical PDF page numbers.
  See pal_additional_verified_evidence.csv for new Lethbridge actual issuance,
  MacEwan expectation and the explicit missing-submission-count evidence.

source_manifest.csv and source_manifest.json
  Every original download: source URL, retrieval time, filename, size and SHA-256.
extracted/file_inventory.csv
  CSV descriptions and row counts.
validation.json
  Download integrity, file parsing and PAL provincial-total reconciliation results.
data_gaps.csv
  Missing information and the evidence needed to answer remaining questions.

Original sources are under raw/ircc, raw/alberta, raw/web, raw/documents and
raw/metadata. The raw workbooks include all original notes and full historical
coverage. Other extracted CSVs preserve enrolment dimensions, source HTML tables,
the DLI register, the data dictionary and reporting changes.

VERIFIED ANCHOR FIGURES (different measures; not interchangeable)
--------------------------------------------------------------
IRCC, December 31, 2024 valid permit holders:
  Canada: 996,375; Alberta intended destination: 71,545.
  The downloaded year-end workbook stops at 2024. These are not October 2026 counts.

Alberta reported international post-secondary enrolment, academic 2024-2025:
  System unique headcount: 50,164.
  University of Alberta 8,664; University of Calgary 7,223;
  University of Lethbridge 1,844; Grant MacEwan University 1,094;
  Mount Royal University 555; Alberta University of the Arts 105;
  Athabasca University 2,664 (transition-period caveat below).
  Other institutions are included in the CSV; this list is not all universities.

Alberta PAL-required application spaces, as published in the saved IRCC notices:
  2024: 40,894; 2025: 47,338; 2026: 32,271.
  Cohort eligibility changed across years; these figures are not a like-for-like
  student population series and are not the number of letters used.

Alberta's Advanced Education annual report 2024-25, PDF page 58, states:
  "In 2024-25, the portal issued 26,089 provincial attestation letters to
  designated learning institutions."
  This is fiscal-year portal issuance, not calendar-year IRCC submissions.

University of Lethbridge's March 2024 budget message reports 2,687 allocated
study-permit applications for January 22, 2024-January 21, 2025, not actual usage.
February2025 GFC minutes separately report1784 PALs issued last year. Do not
divide1784 by2687 without checking matched dates and allocation revisions.
University of Calgary's January 22, 2025 GAPS minutes state:
  "the University was not able to use up its 2024 allocation of PALs."
  The source provides no count or utilization percentage.

HOW TO INTERPRET THE DATA
-------------------------
1. Keep these separate: application spaces allocated -> PALs issued -> PALs
   submitted with IRCC applications -> permits approved/effective -> enrolment.
   The same student can appear in more than one measure. These cannot be added.
2. IRCC province is intended destination, not verified physical residence. A valid
   permit does not itself prove active attendance or physical presence in Canada.
3. IRCC publishes rounded numbers (nearest five) and suppresses small cells as --.
   The extracts retain value_raw and suppressed. Suppressed numeric values are
   blank, not zero. Data are preliminary and can be revised. Do not expect sums
   of rounded cells to equal published totals; use the published totals directly.
4. Annual/YTD permit totals are copied from source total columns, never calculated
   by summing monthly counts. 2026 covers January-July only and must not be compared
   as a completed year against 2025.
5. Alberta LERS enrolment covers provincially approved programs at publicly funded
   reporting institutions, not all private colleges or K-12. Banff Centre is
   excluded. Legal status includes Student Visa or Other Visa; certain refugee/
   work-permit apprentices can be classified as international in LERS.
6. LERS headcounts are unique at each published level. Institutional totals sum
   to 50,606 for 2024-25, while the deduplicated system total is 50,164. This is not
   an extraction error. Full-time/part-time definitions are given in Dictionary.
7. Athabasca's 2024-25 transition covers January 2024-April 2025, creating an
   artificial increase. The reporting note's 7,500 extra learners is an all-student
   figure, not the international subset. NorQuest reports spring 2024 in both
   2023-24 and 2024-25. MaKami begins reporting in 2024-25 (international count 4).
   Review Reporting Changes before calculating growth rates.
8. Fiscal PAL issuance and calendar/cap-year allocations do not share the same
   reporting period. Do not calculate a utilization percentage from 26,089 divided
   by the 2024 or 2025 allocation.
9. OAG Exhibit 7 reports Alberta approvals at 25% of forecast through September
   2025. This is NOT PAL utilization. Its CSV filename explicitly says so.
10. Published inconsistencies are retained: IRCC's 2024 allocation national total
    is 552,095, whereas the listed provincial rows sum to 552,094. The 2025 notice's
    prose says 316,267 expected PAL-required permits, but its table and components
    show 316,276; the normalized extract follows the table. No original is changed.

FRESHNESS AND COVERAGE
----------------------
IRCC catalogue modification: September 15, 2026; monthly files through July 2026.
IRCC year-end workbook: 2000-2024, source vintage December 31, 2024.
Alberta enrolment: 2015-16 to 2024-25; workbook notes refer to December 2025 review.
PAL allocation notices: 2024, 2025 and 2026 as retrieved; retain source snapshots
because allocations may be revised later.
Latest Alberta Advanced Education annual report located: 2024-25. This does not
establish that no newer report exists.

REMAINING GAP
-------------
No complete public table of Alberta university-by-year PAL allocations, letters issued,
letters used in submitted applications, cancellations/reissues and utilization
was obtained in this search. Selected institution figures and completed disclosure
summaries were found in the deeper search above. Missing values mean unknown,
not zero. Existing release packages in the saved ATIP shortlist are a concrete
next source; precise utilization may also require an institution-by-period extract from
Alberta Advanced Education's PAL portal, with matched allocation and usage dates,
and IRCC submission/decision counts where available. No request has been sent.

REPRODUCTION AND VALIDATION
---------------------------
scripts/collect_sources.py downloads official sources and preserves a manifest.
It skips existing successful downloads, so rerunning does not silently refresh
this dated snapshot. Use a new dated folder for a future collection.
scripts/extract_tables.py creates CSVs and validates source hashes/file formats.
Dependencies: Python, openpyxl, pandas, lxml, pypdf, and curl on Windows.
Source worksheets/cells or source tables accompany normalized records.
All originals passed checksum and readability checks. A separate research agent
independently checked key counts, definitions and source limitations.
