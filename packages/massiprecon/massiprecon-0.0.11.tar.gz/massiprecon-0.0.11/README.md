# massiprecon    
Given a list of ips massiprecon will find location and provider info etc and write them to a csv or json


## useage (standalone)  
```
usage: py -m massiprecon -i INFILE -o OUTFILE

massiprecon args

options:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        list of ips
  -o OUTFILE, --outfile OUTFILE
                        json or csv file to write to
```


## useage (library)
```
from massiprecon import massiprecon
f=massiprecon.FileMaker(args.infile,args.outfile)
print(f.generate())
```
