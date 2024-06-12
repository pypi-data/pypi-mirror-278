#imports
import csv
import advocate
import json



#internal function for removing keys
def keystripper(rows):
    rows=[ [ str(value) for value in row.values() ] for row in rows ]
    return rows

class FileMaker:

    #initialise FileMaker object
    def __init__(self,iplist,outfile):
        self.iplist=iplist
        self.outfile=outfile
        #parse extension
        self.filetype=outfile.split(".")[-1].lower()

    #generator function
    def generate(self):

        #open iplist file
        with open(self.iplist, "r") as iplist:
            rows=[]
            for ip in iplist:
                ip=ip.replace("\n","")

                #query api
                r=advocate.post(f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
                rows.append(json.loads(r.text))

            #write to json
            if self.filetype == "json":
                with open(self.outfile, "w", newline='\n') as outf:
                    outf.write(json.dumps(rows))
                    return "written to json"

            #write to csv   
            elif self.filetype == "csv":
                with open(self.outfile, "w", newline='\n') as outf:
                    selected=rows[0]
                    fields = [ key for key in selected.keys()]
                    rows=keystripper(rows)
                    writer = csv.writer(outf, delimiter=",")
                    writer.writerow(fields)
                    writer.writerows(rows)
                    return "written to csv"

            #invalid extension
            else:
                return "extension must be json or csv"

