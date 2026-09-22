from pathlib import Path
import argparse,json
A=Path(__file__).resolve().parents[1]/'assets'
p=argparse.ArgumentParser(description='Read exact extracted pages; does not mark a paper reviewed')
p.add_argument('--paper-id',required=True);p.add_argument('--pages',required=True,help='Comma separated physical PDF page numbers');p.add_argument('--max-chars',type=int,default=20000);a=p.parse_args()
papers={x['paper_id']:x for x in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
if a.paper_id not in papers:p.error('Unknown paper ID')
pages=json.loads((A/papers[a.paper_id]['text_pages_file']).read_text(encoding='utf-8'));wanted={int(n) for n in a.pages.split(',')}
if not wanted.issubset({x['page'] for x in pages}):p.error('Page outside paper')
text='\n'.join(f"\n### {a.paper_id} PDF PAGE {x['page']}\n{x['text']}" for x in pages if x['page'] in wanted)
print(text[:a.max_chars])
if len(text)>a.max_chars:print('\nTRUNCATED: request fewer pages or increase --max-chars. Do not mark unseen text reviewed.')
