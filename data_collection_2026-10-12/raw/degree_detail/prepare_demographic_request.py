from pathlib import Path
import json
p=Path(__file__).resolve().parent
coords=set()
# All degree/age/gender combinations, plus all field/degree combinations.
for geo in [1,10]:
    for degree in range(1,9):
        for age in range(1,9):
            for gender in range(1,5):coords.add(f'{geo}.{degree}.1.1.3.{age}.{gender}.1.1.0')
        for field in range(1,15):coords.add(f'{geo}.{degree}.1.{field}.3.1.1.1.1.0')
q=[dict(productId=37100163,coordinate=c,latestN=6) for c in sorted(coords)]
for i in range(0,len(q),250):
    (p/f'37100163_detail_request_{i//250}.json').write_text(json.dumps(q[i:i+250]))
print(len(q))
