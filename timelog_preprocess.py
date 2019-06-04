#!/usr/bin/env python

"""
prida sloupec s casem, kolik aktivita zabrala - v minutach

20150728: uprava tak, aby ve vypisu byl zacatek prace na tasku a ne jeho konec - tstart
"""

import sys
import re
import datetime
from sys import exc_info


class PreprocessTimelog:
    
    def __init__(self, filename):
        self.filename =  filename
        
    def parse_datetime(self, dt):
        """Parse a datetime instance from 'YYYY-MM-DD HH:MM' formatted string."""
        m = re.match(r'^(\d+)-(\d+)-(\d+) (\d+):(\d+)$', dt)
        if not m:
            raise ValueError('bad date time: ', dt)
        year, month, day, hour, min = map(int, m.groups())
        return datetime.datetime(year, month, day, hour, min)


    def go(self):
        
        pline = None
        line = ""
        dt = None
        pdt = None
        if self.filename == '-':
            f = sys.stdin
        else:
            f = open(self.filename, 'r')
            
        count = 0
        while True:
            pline = line
            pdt = dt

            count = count + 1
            line = f.readline()
            if(line == ""):
                #print("D: end of flie")
                break
            line = line.rstrip().lstrip()
            if(line == ""):
                continue
            
            try:
                t1, t2, e = line.split(":", 2)
                t = t1 + ":" + t2
                
                if(pline.find(":") > 0):
                    pt1, pt2, pe = pline.split(":", 2)
                    tstart = pt1 + ":" + pt2
                else:
                    tstart = ""
            except ValueError:
                print("Line (%d): '%s'; pline: '%s'" % (count, line, pline))
                raise
                
            
            try:
                dt = self.parse_datetime(t);
            except ValueError:
                print("Line: '%s', t='%s'" % (line, t))
                raise
                
            if pline == "":
                continue
            
            diffdt = dt - pdt
            if diffdt.total_seconds() < 0:
                raise ValueError("invalid interval - subZero (%s) for line '%s'" % (str(diffdt), line))
            
            try:
                ecat, ee = e.split(":", 1)
            except ValueError:
                e = " PRIVAT: " + e.lstrip()
            
            try:
                print("%s %d:%s" % (tstart, (diffdt.total_seconds() / 60), e.rstrip()) )
            except IOError:
                print("nejak to tu nefunguje...")
                print("t: '%s'"%t)
                print("tstart: '%s'"%tstart)
                print("total_sec: '%d'"%diffdt.total_seconds())
                print("e: '%s'"%e)
                raise
    
            
            
if __name__ == "__main__":
    if len(sys.argv) == 1:
        p = PreprocessTimelog("-")
    else:
        p = PreprocessTimelog(sys.argv[1])
    p.go()
       
