#!/usr/bin/env python

import sys
import os

TAGCHAR="@"

class SumTimelog:
    
    CATSEPARATOR="_"
    
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
                t1,t2,cat,e = line.split(":", 3)
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
            #print("Mincount: '%d' '%s' %s'" % (mincount, cat, line))
            
            
            cats = cat.split("_")
            cat_combined = ""
            for cat_part in cats:
                if cat_combined == "":
                    cat_combined = cat_part
                else:
                    cat_combined = cat_combined + "_" + cat_part
                
                #if cat_combined.startswith(cat):
                if True:
                    # we don't want to show parent cats, only child
                    if cat_combined not in self.cats:
                        self.cats[cat_combined] = []
                #else:
                #    continue

                #a = (mincount, e)
                #print( "A cat_combined'%s': '%s'" %(cat_combined, str(a)) )
                self.cats[cat_combined].append( (int(mincount), t, cat, e) )
                #print("cats: " + str(self.cats))
        
            # find tags
            probableTags = e.split(self.TAGCHAR)
            allProbTags = len(probableTags) - 1
            if len(probableTags) > 1:
                # chci iterovat pres skoro vsechny polozky
                # e is rstripped - see above
                for i in range(allProbTags):
                    if len(probableTags[ allProbTags - i ]) == 0:
                        # mam invalidni tag
                        raise ValueError("Invalid (empty) tag on line '%s'" % line)

                    # tag je to, co nema mezeru uprostred slova
                    if ' ' in probableTags[ allProbTags - i ]:
                        # not a hash
                        sys.stderr.write("Warning (Debug): space in \"tag\" '%s'. Ignoring tag.\n" % probableTags[ allProbTags - i ])
                        break
                    
                    if probableTags[ allProbTags - i ] not in self.tags:
                        self.tags[ probableTags[ allProbTags - i ] ] = []
                    self.tags[ probableTags[ allProbTags - i ] ].append( (int(mincount), t,  cat, e) )
            
            
    def printCats(self):
        
        # zjistit nejdelsi category
        maxcatlen = -1 
        for cat_combined in sorted(self.cats.keys()):
            if len(cat_combined) > maxcatlen:
                maxcatlen = len(cat_combined)

        formatstring = "{:s}: {:" +str(maxcatlen)+ "s}: {:s}"
        formattotalstring = "------------------\nTOTAL for CATEGORY  {:"+str(maxcatlen)+"s}: {:d}:{:02d}"

        for cat_combined in sorted(self.cats.keys()):
            totalminutes = 0
            
            outputstr = "START of output for CATEGORY  %s" % cat_combined
            print("\n"+outputstr+"\n"+"-"*len(outputstr))
            
            for entry in self.cats[cat_combined]:
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
    p = SumTimelog()
    p.go()
    p.printCats()
    p.printTags()
