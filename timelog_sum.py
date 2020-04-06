#!/usr/bin/env python

import sys
import os

import logging
logging.basicConfig( level=logging.INFO, format="%(asctime)s - %(levelname)s - %(thread)d - %(name)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"  )
log = logging.getLogger(__name__)

TAGCHAR = "@"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SumTimeLog:
    
    CATSEPARATOR = "_"
    
    def __init__(self):
        self.TAGCHAR = TAGCHAR
        if 'GTIMELOG_TAGCHAR' in os.environ:
            self.TAGCHAR = os.environ['GTIMELOG_TAGCHAR']
        
        self.cats = {}    
        self.tags = {}  
    
    def go(self):
        f = sys.stdin
        
        while True:
            line = f.readline()
            if line == "":
                break;
            
            line = line.rstrip()
            try:
                t1, t2, cat, e = line.split(":", 3)
            except ValueError:
                print("Error in data in line '%s'" % line)
                raise
            t = t1 + ":" + t2
            cat = cat.lstrip().rstrip()
            e = e.lstrip().rstrip()

            # _INTERVAL je radek vlozeny timelog_filterdates a obsahuje interval pro jake dny je proveden filterdates
            if cat == '_INTERVAL':
                print e
                continue

            mincount = int(t2.split(" ", 1)[1])
            log.debug("Mincount: '%d' '%s' %s'" % (mincount, cat, line))

            cats = cat.split("_")
            cat_combined = ""
            for cat_part in cats:
                if cat_combined == "":
                    cat_combined = cat_part
                else:
                    cat_combined = cat_combined + "_" + cat_part
                
                if cat_combined not in self.cats:
                    self.cats[cat_combined] = []

                self.cats[cat_combined].append( (int(mincount), t, cat, e) )

            # find tags
            probable_tags = e.split(self.TAGCHAR)
            all_prob_tags = len(probable_tags) - 1
            if len(probable_tags) > 1:
                # chci iterovat pres skoro vsechny polozky
                # e is rstripped - see above
                for i in range(all_prob_tags):
                    probable_tag = probable_tags[ all_prob_tags - i ].rstrip()
                    if len(probable_tag) == 0:
                        # mam invalidni tag
                        raise ValueError("Invalid (empty) tag on line '%s'" % line)

                    # tag je to, co nema mezeru uprostred slova
                    if ' ' in probable_tag:
                        # not a hash
                        sys.stderr.write("Warning (Debug): space in \"tag\" '%s'. Ignoring tag.\n" % probable_tag)
                        break

                    if probable_tag not in self.tags:
                        self.tags[ probable_tag ] = []
                    self.tags[ probable_tag ].append( (int(mincount), t,  cat, e) )
            
            
    def printCats(self):
        
        # zjistit nejdelsi category
        maxcatlen = -1 
        for cat_combined in sorted(self.cats.keys()):
            if len(cat_combined) > maxcatlen:
                maxcatlen = len(cat_combined)

        formatstring = "{:s}: {:" +str(maxcatlen)+ "s}: {:s}"
        formattotalstring = "------------------\nTOTAL for CATEGORY  {:"+str(maxcatlen)+"s}: "+bcolors.OKBLUE+"{:d}:{:02d}"+bcolors.OKBLUE

        for cat_combined in sorted(self.cats.keys()):
            totalminutes = 0
            
            outputstr = "START of output for CATEGORY  %s%s%s" % (bcolors.OKGREEN, cat_combined, bcolors.ENDC)
            print("\n"+outputstr+"\n"+"-"*len(outputstr))
            
            totalminperday = 0
            prevDateCat = None
            prevDate = None

            perDayOutput = ""

            for entry in self.cats[cat_combined]:
                #print(entry)
                try:
                    #totalminutes = totalminutes + entry[0]
                    # remove minutes length entry
                    t1,t2,t3 = entry[1].split(" ", 2)
                    totalminutes = totalminutes + int(t3)
                    t = t1 + " " + t2
                    
                    # work time
                    whr = int(t3) / 60
                    wminutes = int(t3) % 60
                    t = t + " (%d:%02d)"%(whr,wminutes)

                    # time, category, entry
                    print(formatstring.format(t, entry[2], entry[3]) )


                    if prevDateCat != (t1 + "_" + str(cat_combined)):
                        if(prevDateCat != None):
                            whr = totalminperday / 60
                            wminutes = totalminperday % 60
                            perDayOutput = perDayOutput + "\n" + formatstring.format(prevDate + "       (%s%d:%02d%s)"%(bcolors.OKBLUE,whr,wminutes,bcolors.ENDC), cat_combined, '-')

                        prevDateCat = (t1 + "_" + str(cat_combined))
                        prevDate = t1
                        totalminperday = 0

                    totalminperday = totalminperday + int(t3)

                except IndexError:
                    print("here" + str(entry))
                    raise
                
            if(prevDateCat != None):
                whr = totalminperday / 60
                wminutes = totalminperday % 60
                perDayOutput = perDayOutput + "\n" + formatstring.format(prevDate + "       (%s%d:%02d%s)"%(bcolors.OKBLUE,whr,wminutes,bcolors.ENDC), cat_combined, '-')

            print(perDayOutput)

            hr = totalminutes / 60
            minutes = totalminutes % 60
            mandays = hr / 8

            outputstr = formattotalstring.format(cat_combined, hr, minutes)
            print(outputstr+"\n"+"-"*len(outputstr))
 
    def printTags(self):
        
        # zjistit nejdelsi category
        maxcatlen = -1 
        for cat_combined in sorted(self.cats.keys()):
            if len(cat_combined) > maxcatlen:
                maxcatlen = len(cat_combined)
        maxtaglen = -1 
        for tag in sorted(self.tags.keys()):
            if len(tag) > maxtaglen:
                maxtaglen = len(tag)

        formatstring = "{:s}: {:" +str(maxcatlen)+ "s}: {:s}"
        formattotalstring = "TOTAL for TAG       {:"+str(maxtaglen)+"s}: {:d}:{:02d}"
        
        for tag in sorted(self.tags.keys()):
            totalminutes = 0
            
            outputstr = "START of output for TAG       %s" % tag
            print("\n"+outputstr+"\n"+"-"*len(outputstr))
            
            for entry in self.tags[tag]:
                #print(entry)
                try:
                    totalminutes = totalminutes + entry[0]
                    # remove minutes length entry
                    t1,t2,t3 = entry[1].split(" ", 2)
                    t = t1 + " " + t2
                    
                    # work time
                    whr = int(t3) / 60
                    wminutes = int(t3) % 60
                    t = t + " (%d:%02d)"%(whr,wminutes)

                    # time, category, entry
                    print(formatstring.format(t, entry[2], entry[3]) )
                except IndexError:
                    print("here" + str(entry))
                    raise
                
            hr = totalminutes / 60
            minutes = totalminutes % 60
            mandays = hr / 8


            outputstr = formattotalstring.format(tag, hr, minutes)
            print(outputstr+"\n"+"-"*len(outputstr))
 
                 
if __name__ == "__main__":
    p = SumTimeLog()
    p.go()
    p.printCats()
    p.printTags()
