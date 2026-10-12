IRCC AND ALBERTA INTERNATIONAL STUDENT DATA
Research snapshot: 12 October 2026 (UTC)

PURPOSE AND SCOPE
-----------------
This collection brings together official source files, cleaned data and preliminary
analysis of international students in Canada, with an Alberta focus. It covers
student numbers, institutions and study levels; provincial attestation letter
(PAL) allocations; and the available evidence of university PAL issuance and use.
IRCC is Immigration, Refugees and Citizenship Canada.
It does not provide a complete university PAL-use census or identify individual
recipients. Allocations, letters, permits, arrivals and enrolments are distinct.

The main window is calendar 2020 onward. The main academic series cover six
years, 2019-20 through 2024-25. Later institutional reports and estimates are kept
separate, and January-July 2026 administrative counts are labelled partial-year.
Original downloads retain longer histories where available. PALs began in 2024;
earlier PAL years are not applicable, not zero usage.

START HERE: CHOOSE YOUR QUESTION
--------------------------------
All paths below are relative to this collection folder.
Open CSV files in a spreadsheet application; open .ipynb notebooks in a Jupyter
notebook viewer to read saved tables, figures and commentary.

1. How many students were there each year?
   analysis/cleaned/annual_enrolment_canada_alberta.csv
     Six-year overview with separately labelled Alberta annual headcounts and
     Canada/Alberta fall program enrolments.
   analysis/cleaned/annual_alberta_enrolment_by_institution.csv
   analysis/cleaned/annual_alberta_enrolment_by_study_level.csv
     Year-by-year distributions across institutions and credential/program types.
   analysis/cleaned/annual_student_count_outline.csv
     Counts and definitions for separate annual and snapshot permit/enrolment
     measures, including their source references.
   analysis/cleaned/ANNUAL_OUTLINE_README.txt explains these four files.

2. What kinds of students, and at which universities?
   analysis/alberta_ircc_preliminary_analysis.ipynb
     Executed notebook: degree, institution, citizenship and PAL findings,
     source links, tables, figures and cleaning commentary.
   analysis/cleaned/statcan_international_degree_institution.csv
     International degree-level enrolment context for Canada and Alberta.
   analysis/cleaned/37100163_international_age_gender_degree.csv
   analysis/cleaned/37100163_international_field_degree.csv
   analysis/cleaned/37100232_international_institution_field_degree.csv
     Additional age/gender, field and institution/degree profiles. These describe
     enrolments; they do not identify who received a PAL or study permit.

3. Were university PAL allocations used, and what changed after introduction?
   analysis/pal_allocation_admissions_and_timeline.ipynb
     Executed analysis of utilization evidence, before/after counts and possible
     drivers, with limits on causal interpretation.
   analysis/cleaned/pal_before_after_event_matrix.csv
   analysis/cleaned/pal_before_after_annual_counts.csv
   analysis/cleaned/pal_university_utilization_evidence.csv
     Dated events, annual comparisons and institution-specific usage evidence.
   analysis/pal_interpretation/README.txt provides the detailed guide.

FOLDER GUIDE
------------
analysis/cleaned/ contains 29 cleaned CSVs, including the files above.
analysis/cleaned_file_inventory.csv lists all 29 files and their row counts.
analysis/README.txt describes the analysis, definitions and supporting files.
analysis/tables/ and analysis/figures/ contain selected outputs.
focus_2020_latest/ contains the earlier extracts restricted to the main window.
extracted/ contains source-derived tables, including longer historical series.
raw/ preserves original downloads. Later additions also have separate source
archives and receipts; see the reproduction and validation section below.
research/ records search coverage, access limits and supporting investigations.
research/atip/README.txt explains the completed access-to-information release
leads. Only summaries were obtained, not the underlying disclosure packages.

For definitions and safe comparisons, read RULES FOR INTERPRETATION below
before combining files. For source coverage and unresolved questions, use the
freshness, remaining-gap and validation sections.

VERIFIED COUNTS AND WHAT THEY MEAN
---------------------------------
Student enrolment
Alberta's Learner and Enrolment Reporting System (LERS) reports these annual
international headcounts in its reporting post-secondary system:

  Academic year   Headcount
  2019-20            28,246
  2020-21            27,028
  2021-22            29,991
  2022-23            37,076
  2023-24            48,311
  2024-25            50,164

Source: analysis/cleaned/annual_enrolment_canada_alberta.csv. These are annual
enrolments, not arrivals, PAL recipients or permit approvals. In 2024-25, LERS
reports 4,747 master's and 2,875 doctoral students; see
analysis/cleaned/alberta_enrolment_by_credential_and_program_type.csv.
Master's is not MA-only, and doctoral categories are not necessarily PhD-only.

Permit holders before and after PAL
The national study-permit series excluding extensions reports 495,860 holders
in 2023, 293,260 in 2024 and 115,460 in 2025. Alberta's post-secondary designated
learning institution (DLI) series reports 29,630, 25,570 and 17,250 respectively.
That series counts holders by the year their permit became effective and includes
extensions.
These are different populations: do not compare them as national/provincial
arrivals or infer PAL's causal effect. No comparable annual Alberta new-arrivals
series was obtained. Six-year counts and exact definitions are in
analysis/cleaned/pal_before_after_annual_counts.csv; dated policy changes are in
analysis/cleaned/pal_before_after_event_matrix.csv.

PAL allocations and actual use
Alberta's published application-space allocations are 40,894 (2024), 47,338
(2025) and 32,271 (2026). The 2025 graduate allocation is 5,256, or 11.1%, for
master's and doctoral applicants combined. These are planned application spaces,
not admitted students or approved permits. Source:
analysis/cleaned/pal_provincial_allocations_2024_2026.csv.

Actual-use evidence remains incomplete:
  - Alberta: 26,089 portal-issued PALs in fiscal 2024-25, across DLIs. The annual
    report states, "the portal issued 26,089 provincial attestation letters"
    (physical PDF page 58). Fiscal issuance cannot be divided by calendar quotas.
  - Lethbridge: 1,784 PALs issued in 2024. Its 2,687 allocation covers January 22,
    2024-January 21, 2025; unmatched periods prevent a verified utilization rate.
  - Calgary: reported 2024 underuse without the counts needed for a percentage.
  - Comparators: the University of Saskatchewan endorsed 54.9% of its allocation
    by December 3, 2024; the University of Manitoba reported less than 50% used;
    the University of Toronto reported all used. Stages and dates
    differ, so these are disclosures, not a standardized university ranking.
Quotations, dates, sources and limitations:
analysis/cleaned/pal_university_utilization_evidence.csv.

RULES FOR INTERPRETATION
-----------------------
1. Separate admission, PAL allocation, issuance, submission, permit approval,
   permit effectiveness, arrival and enrolment. A person can appear at several
   stages. Allocation does not reveal actual university or degree recipients.
2. PAL began January 22, 2024; earlier years are not applicable, not zero.
   Master's/doctoral applicants were generally exempt in 2024, included from
   January 22, 2025. From January 1, 2026, students in degree-granting master's
   and doctoral programs at public DLIs are exempt again. This does not cover
   every graduate certificate or private institution. Other exemptions apply.
   Changing coverage prevents a like-for-like quota trend.
3. LERS covers approved programs at publicly funded reporting institutions, not
   all private colleges or K-12; Banff is excluded. Its international definition
   includes Student Visa or Other Visa and some refugee/work-permit apprentices.
   Published headcounts are unique at each aggregation level: 2024-25 institution
   totals sum to 50,606, versus 50,164 unique system students. Do not sum them.
4. Athabasca's 2024-25 window spans 16 months; NorQuest repeats spring 2024 across
   adjacent years; MaKami first reports in 2024-25. Check the reporting-change
   extract before interpreting growth. Statistics Canada's Postsecondary Student
   Information System (PSIS) instead counts fall-snapshot program enrolments,
   rounded to three; it is not annual LERS.
5. IRCC counts are rounded to five; suppressed cells remain blank, not zero.
   Province indicates intended destination, not verified residence or attendance.
   Use published annual totals, never sums of months. January-July 2026 is partial.
   Do not splice older year-end and newer monthly stocks with different scopes.
6. Source inconsistencies remain documented: 2024 allocation rows sum to 552,094
   versus published 552,095; the 2025 expected-permit table says 316,276 versus
   316,267 in prose. Neither approvals versus forecast nor expected permits
   measure PAL utilization. Observed declines do not establish policy causation.

FRESHNESS, PROVENANCE AND REMAINING GAPS
-------------------------------------
This is a saved research snapshot retrieved on 12 October 2026 (UTC), not a live
feed. Retrieval dates are not observation dates. Latest coverage varies:
  - IRCC monthly files: through July 2026 (latest year is partial); year-end
    workbook: through 2024. Longer historical series remain in the source files.
  - Alberta annual enrolment: through academic 2024-25.
  - Statistics Canada observed PSIS enrolments: through 2024/25. Separate
    modelled 2025/26 estimates and selected institutional reports are retained.
  - PAL allocation notices: 2024-2026; eligibility and allocations can change.

Source records are distributed across the collection. Start with
source_manifest.csv (or .json) for the original collection. Later additions have
separate records:
  raw/degree_detail/provenance.json
  research/pal_interpretation/baseline_raw/provenance.json
  research/pal_interpretation/raw_timeline/download_receipts.json
These record source locations and hashes for their respective downloads. CSV
source columns identify supporting files, cells, tables or pages where supplied.
No single manifest covers every later addition.

No complete Alberta university-by-year table links allocated spaces, unique
PALs issued, cancellations/replacements, submitted applications, permit decisions,
arrivals and registrations. Degree-specific actual PAL recipients and a harmonized
annual Alberta new-arrivals series remain unavailable in the retrieved evidence.
Missing means unknown, not zero. The policy matrix documents plausible mechanisms;
it does not estimate what share of a decline PAL policy caused.

research/atip/priority_record_leads.csv identifies completed disclosure packages,
including A-2025-84005 for Alberta DLI decisions. Only public summaries were
obtained, not the released tables; requested fields may not have been supplied.
The next useful evidence is those packages and matched institution/intake/degree
records from Alberta's PAL portal. No requests or external messages were sent.
data_gaps.csv records the initial gaps; analysis/README.txt and
analysis/pal_interpretation/README.txt describe the later analysis gaps.

REPRODUCTION AND VALIDATION
---------------------------
Use the saved sources for exact reproduction. Back up derived outputs before
rerunning: the scripts overwrite their generated files. All paths below are
relative to this collection folder; run commands from this folder. Python must
have pandas, openpyxl, lxml and pypdf. Notebook execution additionally needs
matplotlib, nbformat, nbclient, jupyter_client and ipykernel. The notebook builders
load analysis/_dependencies; the preliminary builder creates the local kernel.

For the existing snapshot, run these offline steps in order. This order was
checked against script dependencies; the README review did not rerun the pipeline.
Saved execution records report nine and six notebook code cells, respectively,
with zero error outputs; they are evidence of prior runs, not a fresh-run test.
  python scripts/extract_citizenship.py
  python scripts/build_analysis_notebook.py
  python scripts/build_annual_outline.py
  python scripts/build_pal_interpretation_notebook.py
The first notebook builder runs preliminary_analysis.py to regenerate cleaned
tables and checks, then executes the notebook. The PAL builder runs
build_pal_matrix.py and pal_diagnostic_calculations.py, then executes its notebook.
They use the saved focus extracts, degree files and research evidence tables.
For rebuilding earlier extracts, run scripts/extract_tables.py followed by
scripts/extract_extended.py; degree extraction details are in raw/degree_detail/.

Acquisition is separate: scripts/collect_sources.py and scripts/extend_collection.py
use the network (including curl.exe on Windows). Successful existing downloads
are skipped. Use a new dated collection for refreshed sources; these scripts are
not a one-command reconstruction of all later manually researched evidence.

Check validation results for the relevant stage, not a blanket certification:
  collection_validation.json: earlier manifest's 59 obtained sources and one
    unavailable source; checksum/container checks do not verify every claim.
  raw/degree_detail/validation.json: 827 numeric API/bulk degree matches.
  analysis/validation_checks.json: cleaning checks and retained discrepancies.
  analysis/annual_outline_validation.json: annual overview reconciliation.
  analysis/pal_interpretation/matrix_validation.json: matrix structure/content.
The analysis folders also contain notebook_execution.json and independent review
notes. These document completed checks and their limits, not proof that every
public source was found or every causal interpretation is established.
