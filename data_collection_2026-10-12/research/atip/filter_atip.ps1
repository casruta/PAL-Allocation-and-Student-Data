$ErrorActionPreference = 'Stop'
$collectionRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$rawFile = Join-Path $collectionRoot 'raw/atip/ati-all.csv'
$allRows = @(Import-Csv -LiteralPath $rawFile)
$irccRows = @($allRows | Where-Object { $_.owner_org -eq 'cic' -and [int]$_.year -ge 2020 })
$studentRows = @($irccRows | Where-Object { ($_.summary_en + ' ' + $_.summary_fr) -match 'study permit|international student|provincial attestation|\bPAL\b|designated learning|permis d.[ée]tudes|[ée]tudiants [ée]trangers|attestation provinciale' })
$palRows = @($irccRows | Where-Object { ($_.summary_en + ' ' + $_.summary_fr) -match 'attestation provinc|provincial attestation|\bPAL\b' })
$ids = @('A-2024-02010','A-2025-84005','A-2025-83996','2A-2021-02627','2A-2021-01634','A-2026-30356','A-2026-03891','1A-2025-15195','A-2024-01082','2A-2024-39077','2A-2023-72482','A-2025-55557','A-2024-48121','A-2024-68363')
$leads = @($irccRows | Where-Object { $_.request_number -in $ids } | Select-Object *, @{Name='summary_record_url';Expression={ 'https://search.open.canada.ca/ati/record/' + [uri]::EscapeDataString(($_.owner_org,$_.year,$_.month,$_.request_number -join ',')) }})
$studentRows | Export-Csv -NoTypeInformation -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot 'ircc_student_related_summaries_2020_onward.csv')
$palRows | Export-Csv -NoTypeInformation -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot 'ircc_pal_related_summaries_2020_onward.csv')
$leads | Export-Csv -NoTypeInformation -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot 'priority_record_leads.csv')
$provenance = [ordered]@{
    collected_date_utc = '2026-10-12'
    source_name = 'Completed Access to Information Request Summaries dataset'
    publisher = 'Treasury Board of Canada Secretariat; summaries submitted by federal institutions'
    source_url = 'https://open.canada.ca/data/dataset/0797e893-751e-4695-8229-a5066e4fe43c/resource/19383ca2-b01a-487d-88f7-e1ffbc7d39c2/download/ati-all.csv'
    landing_url = 'https://open.canada.ca/data/en/dataset/0797e893-751e-4695-8229-a5066e4fe43c'
    raw_relative_path = 'raw/atip/ati-all.csv'
    raw_bytes = (Get-Item -LiteralPath $rawFile).Length
    raw_sha256 = (Get-FileHash -LiteralPath $rawFile -Algorithm SHA256).Hash.ToLowerInvariant()
    raw_rows = $allRows.Count
    ircc_completed_2020_onward_rows = $irccRows.Count
    student_keyword_rows = $studentRows.Count
    pal_keyword_rows = $palRows.Count
    priority_lead_rows = $leads.Count
    filters = 'owner_org=cic; completion year >=2020. Broad student and narrow PAL expressions in filter_atip.ps1. Priority IDs manually selected from summaries.'
    limitations = 'These are request summaries, not the underlying disclosed records. Page counts are disclosure package lengths, never student or PAL counts. Completed year/month is not the data period. All disclosed/part disclosed does not establish that the requested data existed at the requested granularity. No copies requested and no contact initiated.'
}
$provenance | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot 'provenance.json')
$provenance | ConvertTo-Json -Depth 5
