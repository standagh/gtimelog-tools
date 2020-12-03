#!/usr/bin/env python

"""
Versions:
20150601    Oprava chybky v 'calculate_days_lm' -> 'startDay' nebyl uvozen 'self.'

"""


import sys
import datetime
import time
import re

import logging
logging.basicConfig( level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(thread)d - %(name)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"  )
log = logging.getLogger("main")

class FilterTimelogDates:

    def __init__(self, startParam, endParam):
        self.startParam = startParam
        self.endParam = endParam        
        self.startDay = None
        self.lastDay = None
        self.cd = datetime.date.today()
        
        self.calculate_days_interval()
    
    def calculate_days_m(self):
        self.startDay = datetime.date( self.cd.year, self.cd.month, 1)
        self.lastDay = self.cd

    def calculate_days_lm(self):
        self.calculate_days_m()
        self.lastDay = datetime.date.fromordinal( self.startDay.toordinal()-1 )
        self.startDay = datetime.date(self.lastDay.year, self.lastDay.month, 1)

    def calculate_days_w(self):
        self.startDay = datetime.date.fromordinal(self.cd.toordinal() - self.cd.weekday())
        self.lastDay = self.cd

    def calculate_days_lw(self):
        dayInWeek = self.cd.weekday()
        self.startDay = datetime.date.fromordinal(self.cd.toordinal() - self.cd.weekday() - 7)
        self.lastDay = datetime.date.fromordinal(self.cd.toordinal() - self.cd.weekday() - 1)


    def calculate_date_from_input_param(self, param, startDate = None):
    
        if param is None:
            return self.cd
    
        # kolik dnu zpatky
        if re.match('^[0-9]+$', param) is not None:
            #self.cd.toordinal() - int(param)
            return datetime.date.fromordinal( self.cd.toordinal() - int(param) )
    
        # den v mesici
        if re.match('^[0-9]+\.$', param) is not None:
            adts = param.split('.')
            return datetime.date( self.cd.year, self.cd.month, int(adts[0]) )
        
        # den a mesic v roce
        if re.match('^[0-9]+\.\ *[0-9]+\.$', param) is not None:
            adts = param.split('.')
            return datetime.date( self.cd.year, int(adts[1]), int(adts[0]) )

        # den, masic a rok - mozno 2/4 ciferne
        if re.match('^[0-9]+\.\ *[0-9]+\.\ *([0-9]{2}|[0-9]{4})$', param) is not None:
            adts = param.split('.')
            if(int(adts[2]) < 100):
                adts[2] = int(adts[2]) + 2000
            return datetime.date( int(adts[2]), int(adts[1]), int(adts[0]) )

        # +offset kolik dnu od zacatku - pouziti jen u druheho terminu v intervalu
        if re.match('^\+[0-9]+$', param):
            if startDate is None: 
                raise ValueError("StartDate is not set for offset interval")
            return datetime.date.fromordinal( startDate.toordinal() + int(param[1:]) - 1 )

    def calculate_days_interval(self):
        """from startParam and endParam count startDay a lastDay"""
        if str(self.startParam) == "lw":
            self.calculate_days_lw()
        elif str(self.startParam) == "w":
            self.calculate_days_w()
        elif str(self.startParam) == "lm":
            self.calculate_days_lm()
        elif str(self.startParam) == "m":
            self.calculate_days_m()
        else:
            self.startDay = self.calculate_date_from_input_param(self.startParam)
            self.lastDay = self.calculate_date_from_input_param(self.endParam, self.startDay)
            
            #self.startDay = datetime.date.fromordinal((self.cd.toordinal() - int(self.startParam)))
            #if self.endParam is None:
            #    # means current day
            #    self.lastDay = self.cd
            #else:
            #    self.lastDay = datetime.date.fromordinal((self.cd.toordinal() - int(self.endParam)))
        
        # pro jaky interval pracujeme:
        sd = self.startDay.strftime('%Y-%m-%d')
        ed = self.lastDay.strftime('%Y-%m-%d')
        print("0:0:_INTERVAL: DATE INTERVAL: '%s' - '%s'" % (sd, ed))
        

    def parse_date(self, dt):
        """Parse a datetime instance from 'YYYY-MM-DD HH:MM' formatted string."""
        m = re.match(r'^(\d+)-(\d+)-(\d+) (\d+):(\d+) .*$', dt)
        if not m:
            raise ValueError('bad date: ', dt)
        year, month, day, hour, min = map(int, m.groups())
        return datetime.date(year, month, day)

    def go(self):
        f = sys.stdin
        
        while True:
            line = f.readline()
            if line == "":
                break
            
            line = line.rstrip().lstrip()
            if(line == ""):
                continue
            
            try:
                t1, t2, e = line.split(":", 2)  
                t = t1 + ":" + t2
            except ValueError:
                print("Line: '%s'" % (line))
                raise
                
            try:
                dt = self.parse_date(t);
            except ValueError:
                print("Line: '%s', t='%s'" % (line, t))
                raise
            
            if dt >= self.startDay and dt <= self.lastDay:
                print(line)
                

def print_usage():
    print("Invalid input parameters: '%s'. Required either startDay/numOfDays or interval startDay/numOfDays - numDays/endDate." % sys.argv )


if __name__ == "__main__":
    if len(sys.argv) == 2:
        startParam = sys.argv[1]
        endParam = None
    elif len(sys.argv) == 3:
        startParam = sys.argv[1]
        endParam = sys.argv[2]
    else:
        print_usage()
        sys.exit(10)

    p = FilterTimelogDates(startParam, endParam)
    p.go()



