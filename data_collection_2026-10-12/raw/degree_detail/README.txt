OFFICIAL STATISTICS CANADA DEGREE-LEVEL CONTEXT
Retrieved 2026-10-12 UTC. Source release date: 2026-10-01. Latest academic year: 2024/2025.

These data describe INTERNATIONAL ENROLMENTS, not PAL recipients, PAL letters issued,
permit applications, permit approvals, study permit holders, or graduates.

Sources:
https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710023201
https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710016301
https://www.statcan.gc.ca/en/developers/wds/user-guide

37100232-eng.zip: full official table 37-10-0232-01 (institution, ISCED degree-equivalent
level, institution type, registration status, field of study, student status, gender).
37100163-eng.zip: full official table 37-10-0163-01 (province, ISCED degree-equivalent
level, institution type, field of study, student status, age, gender, academic period,
selected statistic).

Filtered CSV names containing international_canada_alberta_2019_latest retain all
published rows for Canada/Alberta/Alberta institutions, international status and
2019/2020 onward, preserving source dimension names, numeric values and flags.
All other dimensions remain present: these CSVs contain many overlapping totals,
subtotals and detailed categories. DO NOT sum the whole file.

The smaller 37100232_international_degrees_canada_alberta_2019_2024.csv is an API
extract of degree totals, international students, all institution types, all
registration statuses, all fields, all genders, latest six academic years. It
contains 827 numeric rows. Its 232 requested series yielded 165 published series
and 67 unavailable coordinates. Of 990 API observations, 163 had no value and no
end reference date; those are retained separately in
37100232_api_unavailable_observations.csv, and are not counted as numeric records.
Unavailable series and observations are logged, never recoded to zero.
Raw request and response JSON files preserve the API evidence. Metadata maps the
coordinate component IDs to the official dimension labels.

Interpretation notes from official table metadata:
- Counts are FALL SNAPSHOT program enrolments, not unique persons and not a
  full-academic-year student count. Institutions choose a date Sept 30-Dec 1.
- If a student is enrolled in more than one program at the snapshot, all programs
  are counted. Enrolments at different institutions can also overlap persons.
- All counts are randomly rounded to multiples of three; separately rounded
  totals may not equal the sum of subcategories.
- Data are subject to revision. Differences of a few between related tables can
  reflect rounding; never silently force totals to match.
- Degree labels are ISCED 2011 equivalents. "Master's or equivalent" is not an
  MA-only count; "Doctoral or equivalent" is not an exact PhD credential label.
- Institution data are at parent level, with historical campus exceptions.
- Gender collection changed from sex after the 2021 standard; non-binary is
  rolled into Gender unknown in public outputs. Do not interpret unknown as
  exclusively missing sex/gender information.
- The 2023 correction affected 11 Alberta college institution counts but did not
  affect Alberta/Canada aggregate college totals. These are updated source data.

To use 37-10-0163 values as counts, select Selected statistics=Number,
Selected academic period=Fall snapshot. Other rows are percentages and must not
be mixed with counts. For a single breakdown choose total values in every other
dimension. Both detailed fields and STEM/BHASE subtotals coexist.

Validation approach: preserve downloaded archives, extract metadata and raw
records without recoding, retain flags and unavailable series, and cross-check
independently retrieved API degree totals against the official CSV cube rows.
provenance.json records sources, filters, row counts, bytes and SHA-256 hashes.
