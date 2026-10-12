import pathlib,json,subprocess,hashlib,datetime
root=pathlib.Path(__file__).parent
receipts=json.loads((root/'download_receipts.json').read_text())
sources={"alberta_launch":"https://open.alberta.ca/dataset/9c785a4b-e79a-465b-8fa9-322a322f1f15/resource/802e26db-c6c9-4557-a9ac-60820d707f6b/download/ae-annual-report-2023-2024.pdf","spouse24":"https://search.open.canada.ca/qpnotes/record/cic%2CIRCC-2024-QP-00066","gazette25":"https://gazette.gc.ca/rp-pr/p1/2025/2025-01-18/html/notice-avis-eng.html"}
for key,url in sources.items():
 p=root/(key+('.pdf' if '.pdf' in url else '.html'))
 result=subprocess.run(['curl.exe','-L','--fail','--max-time','35','--silent','--show-error',url,'-o',str(p)],capture_output=True,text=True)
 ok=result.returncode==0 and p.exists()
 receipts.append(dict(source_id=key,url=url,local_path=str(p),status='downloaded' if ok else 'failed',bytes=p.stat().st_size if ok else 0,sha256=hashlib.sha256(p.read_bytes()).hexdigest() if ok else None,retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),error=result.stderr if not ok else None))
 print(key,ok,flush=True)
(root/'download_receipts.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
