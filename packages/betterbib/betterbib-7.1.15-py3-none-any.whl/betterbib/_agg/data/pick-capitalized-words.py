import argparse
import json
from pathlib import Path
import enchant
def _contains_upper(string):return any((char.isupper() for char in string))
def _main():
 args=_parse_cmd_arguments()
 with Path(args.infile).open() as f:words=f.read().split()
 words=set(words)
 dictionary=enchant.DictWithPWL('en_US')
 cwords=[w for w in words if w[0].isupper() and (not _contains_upper(w[1:])) and (not dictionary.check(w.lower()))]
 with Path(args.outfile).open('w') as f:json.dump(sorted(cwords),f,indent=2,ensure_ascii=False)
def _parse_cmd_arguments():
 parser=argparse.ArgumentParser(description='Update capit.json.')
 parser.add_argument('infile',type=str)
 parser.add_argument('outfile',type=str)
 return parser.parse_args()
if __name__=='__main__':_main()