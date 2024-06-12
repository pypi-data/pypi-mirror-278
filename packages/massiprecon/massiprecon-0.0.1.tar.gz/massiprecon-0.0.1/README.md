# massiprecon    
Given a list of ips massiprecon will find location and provider info etc and write them to a csv or json
![image](https://github.com/malectricasoftware/balsamic/assets/107813117/c9e8138c-9f8f-4d68-b71c-331cf7a42343)

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
