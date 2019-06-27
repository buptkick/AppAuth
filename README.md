----------

# AppAuth #

----------

# Data preparation

More than 2 set of Android Apps belong to different developers. 

# Feature Extraction #

$ python authfeature.py creator_path [op]csv_path

creator_path: contains sub-directories named with 'auth1', 'auth2', ..., 'authN' and their apks in these sub-directories.

[op]csv_path: output the feature vectors into .csv files named with author's name.

# Cross Validation

$ python crossval.py [op]csv_path

[op]csv_path: input the feature vectors in .csv files named with author's name.

# Pair Attribution

$ python pariauth.py csv_path_pre csv_path_all

csv_path_pre: input the need-to-predict 2 feature vectors in 2 .csv files named with author's name. [dir]Features_pre---┬---[file]auth#1pre.csv-----[row]auth#1apk#1pre 

​                                  └---[file]auth#2pre.csv-----[row]auth#2apk#1pre"

csv_path_all: input all the other feature vectors in .csv files named with author's name.  

[dir]Features_all---┬---[file]auth#1all.csv---┬---[row]auth#1apk#1all

​                                 │                                       ├---[row]auth#1apk#2all

​                                 │                                       ├---...

​                                 │                                       └---[row]auth#1apk#Nall

​                                 └---[file]auth#2all.csv---┬---[row]auth#2apk#1all

​                                                                          ├---[row]auth#2apk#2all

​                                                                          ├---...

​                                                                          └---[row]auth#2apk#Nall

# Experimental Result

