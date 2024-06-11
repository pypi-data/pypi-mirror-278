from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
def _main():
 parser=argparse.ArgumentParser(description='Update journals.json.')
 parser.add_argument('infiles',type=str,nargs='+')
 args=parser.parse_args()
 exclude_list=['journal_abbreviations_entrez.csv','journal_abbreviations_webofscience-dotless.csv','journal_abbreviations_webofscience-dots.csv','journal_abbreviations_medicus.csv','journal_abbreviations_ieee_strings.csv']
 out={}
 for file in args.infiles:
  file=Path(file)
  if file.name in exclude_list or file.suffix!='.csv':continue
  with file.open() as f:out|={row[0]:row[1] for row in csv.reader(f,delimiter=',')}
 print('The following entries are equal after lower()')
 for s in get_equal_after_lower(list(out.keys())):
  print()
  print(s)
 with Path('journals.json').open('w') as f:json.dump(out,f,indent=2,ensure_ascii=False)
def get_equal_after_lower(strings:list[str])->list[list[str]]:
 transformed_strings=[s.lower() for s in strings]
 transformed_dict:dict[str,list[str]]={}
 for original,transformed in zip(strings,transformed_strings):
  if transformed in transformed_dict:transformed_dict[transformed].append(original)
  else:transformed_dict[transformed]=[original]
 return [strings for strings in transformed_dict.values() if len(strings)>1]
if __name__=='__main__':_main()