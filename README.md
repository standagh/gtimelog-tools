# gtimelog-tools
Reporting tools for gtimelog project

Main entry points:

gtlsreports
  - to report summary on tasks and subtasks
  
gtlsreportst
  - to report summary on top level tasks - without any '_'
  
gtlsreportd
  - to report deaily details for selected selected tasks
  
By default it works on file: "$HOME/.gtimelog/timelog.txt"
Possible override via env variable 'GTLLIST_DATA' (see file gtllist)

To see possible command line params see:
./gtlsreport_help

