import re
import sys
import argparse
import mmap
import os
import gzip
import io

pattern = re.compile(r"(?:\$|%(?:25)*24|\\(?:0024|0{0,2}44))(?:{|%(?:25)*7[Bb]|\\(?:007[Bb]|0{0,2}173)).{0,30}?((?:[Jj]|%(?:25)*[46][Aa]|\\(?:00[46][Aa]|0{0,2}1[15]2)).{0,30}?(?:[Nn]|%(?:25)*[46][Ee]|\\(?:00[46][Ee]|0{0,2}1[15]6)).{0,30}?(?:[Dd]|%(?:25)*[46]4|\\(?:00[46]4|0{0,2}1[04]4)).{0,30}?(?:[Ii]|%(?:25)*[46]9|\\(?:00[46]9|0{0,2}1[15]1)|ı).{0,30}?(?::|%(?:25)*3[Aa]|\\(?:003[Aa]|0{0,2}72)).{0,30}?((?:[Ll]|%(?:25)*[46][Cc]|\\(?:00[46][Cc]|0{0,2}1[15]4)).{0,30}?(?:[Dd]|%(?:25)*[46]4|\\(?:00[46]4|0{0,2}1[04]4)).{0,30}?(?:[Aa]|%(?:25)*[46]1|\\(?:00[46]1|0{0,2}1[04]1)).{0,30}?(?:[Pp]|%(?:25)*[57]0|\\(?:00[57]0|0{0,2}1[26]0))(?:.{0,30}?(?:[Ss]|%(?:25)*[57]3|\\(?:00[57]3|0{0,2}1[26]3)))?|(?:[Rr]|%(?:25)*[57]2|\\(?:00[57]2|0{0,2}1[26]2)).{0,30}?(?:[Mm]|%(?:25)*[46][Dd]|\\(?:00[46][Dd]|0{0,2}1[15]5)).{0,30}?(?:[Ii]|%(?:25)*[46]9|\\(?:00[46]9|0{0,2}1[15]1)|ı)|(?:[Dd]|%(?:25)*[46]4|\\(?:00[46]4|0{0,2}1[04]4)).{0,30}?(?:[Nn]|%(?:25)*[46][Ee]|\\(?:00[46][Ee]|0{0,2}1[15]6)).{0,30}?(?:[Ss]|%(?:25)*[57]3|\\(?:00[57]3|0{0,2}1[26]3))|(?:[Nn]|%(?:25)*[46][Ee]|\\(?:00[46][Ee]|0{0,2}1[15]6)).{0,30}?(?:[Ii]|%(?:25)*[46]9|\\(?:00[46]9|0{0,2}1[15]1)|ı).{0,30}?(?:[Ss]|%(?:25)*[57]3|\\(?:00[57]3|0{0,2}1[26]3))|(?:.{0,30}?(?:[Ii]|%(?:25)*[46]9|\\(?:00[46]9|0{0,2}1[15]1)|ı)){2}.{0,30}?(?:[Oo]|%(?:25)*[46][Ff]|\\(?:00[46][Ff]|0{0,2}1[15]7)).{0,30}?(?:[Pp]|%(?:25)*[57]0|\\(?:00[57]0|0{0,2}1[26]0))|(?:[Cc]|%(?:25)*[46]3|\\(?:00[46]3|0{0,2}1[04]3)).{0,30}?(?:[Oo]|%(?:25)*[46][Ff]|\\(?:00[46][Ff]|0{0,2}1[15]7)).{0,30}?(?:[Rr]|%(?:25)*[57]2|\\(?:00[57]2|0{0,2}1[26]2)).{0,30}?(?:[Bb]|%(?:25)*[46]2|\\(?:00[46]2|0{0,2}1[04]2)).{0,30}?(?:[Aa]|%(?:25)*[46]1|\\(?:00[46]1|0{0,2}1[04]1))|(?:[Nn]|%(?:25)*[46][Ee]|\\(?:00[46][Ee]|0{0,2}1[15]6)).{0,30}?(?:[Dd]|%(?:25)*[46]4|\\(?:00[46]4|0{0,2}1[04]4)).{0,30}?(?:[Ss]|%(?:25)*[57]3|\\(?:00[57]3|0{0,2}1[26]3))|(?:[Hh]|%(?:25)*[46]8|\\(?:00[46]8|0{0,2}1[15]0))(?:.{0,30}?(?:[Tt]|%(?:25)*[57]4|\\(?:00[57]4|0{0,2}1[26]4))){2}.{0,30}?(?:[Pp]|%(?:25)*[57]0|\\(?:00[57]0|0{0,2}1[26]0))(?:.{0,30}?(?:[Ss]|%(?:25)*[57]3|\\(?:00[57]3|0{0,2}1[26]3)))?).{0,30}?(?::|%(?:25)*3[Aa]|\\(?:003[Aa]|0{0,2}72)).{0,30}?(?:\/|%(?:25)*2[Ff]|\\(?:002[Ff]|0{0,2}57)|\${)|(?:[Bb]|%(?:25)*[46]2|\\(?:00[46]2|0{0,2}1[04]2)).{0,30}?(?:[Aa]|%(?:25)*[46]1|\\(?:00[46]1|0{0,2}1[04]1)).{0,30}?(?:[Ss]|%(?:25)*[57]3|\\(?:00[57]3|0{0,2}1[26]3)).{0,30}?(?:[Ee]|%(?:25)*[46]5|\\(?:00[46]5|0{0,2}1[04]5)).{2,60}?(?::|%(?:25)*3[Aa]|\\(?:003[Aa]|0{0,2}72))(JH[s-v]|[\x2b\x2f-9A-Za-z][CSiy]R7|[\x2b\x2f-9A-Za-z]{2}[048AEIMQUYcgkosw]ke[\x2b\x2f-9w-z]))")
def checkline(lineno:int, line:str, out):
    match = re.search(pattern, line)
    if match:
        print(f"{filename}:{lineno} {line}", file=out)
    #else:
    #    print(f"NOMATCH {filename}:{lineno} {line}", file=out)
def checklines(mapfile, out, fsize):
    lineno = 0
    while mapfile.tell() != fsize:
        line=mapfile.readline()
        lineno+=1
        sline = line.decode('utf-8')
        checkline(lineno, sline, out)


def check(filename, out):
    if os.stat(filename).st_size> 0: 
        print(filename)
        with open(filename, "r") as infile:
            with mmap.mmap(infile.fileno(), 0, prot=mmap.PROT_READ) as mapfile:
                if filename.endswith(".gz"):
                   gzf = gzip.decompress(mapfile.read())
                   data = gzf.decode('utf-8')
                   instream = io.StringIO(data)
                   lineno = 1
                   for line in instream.readlines():
                       checkline(lineno, line, out)
                       lineno+=1
                else:
                    fsize = mapfile.size()
                    checklines(mapfile, out, fsize)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=sys.argv[0])
    parser.add_argument("--out", default=sys.stdout, type=argparse.FileType('w'))
    parser.add_argument("--err", default=sys.stderr, type=argparse.FileType('w'))
    parser.add_argument("--in", dest="infiles", nargs="+")
    args = parser.parse_args()
    err = args.err 
    for filename in args.infiles:
        try:
            check(filename, args.out)
        except BaseException as e:
            print(filename, e, file=err)
