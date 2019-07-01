----------

# AppAuth #

----------

# Data preparation

At least 2 set of Android Apps belong to different developers. 

# Feature Extraction #

```shell
$ python authfeature.py creator_path [op]csv_path
```

**creator_path**: contains sub-directories named with 'auth1', 'auth2', ..., 'authN' and their ".apk" files in these sub-directories.

    [*dir*]creator_path---┬---[*dir*]auth#1---┬---[*file*]auth#1apk#1.apk
                          │                   ├---[*file*]auth#1apk#2.apk
                          │                   ├---...
                          │                   └---[*file*]auth#1apk#N.apk
                          ├---[*dir*]auth#2---┬---[*file*]auth#2apk#1.apk
                          │                   ├---[*file*]auth#2apk#2.apk
                          │                   ├---...
                          │                   └---[*file*]auth#2apk#N.apk
                          ├---...
                          └---[*dir*]auth#N---┬---[*file*]auth#Napk#1.apk
                                              ├---[*file*]auth#Napk#2.apk
                                              ├---...
                                              └---[*file*]auth#Napk#N.apk
[*op*]**csv_path**: output the feature vectors into ".csv" files named with author's name.

# Cross Validation

```shell
$ python crossval.py [op]csv_path
```

[*op*]**csv_path**: input the feature vectors in ".csv" files named with author's name.

# Pair Attribution

```shell
$ python pariauth.py csv_path_pre csv_path_all
```

**csv_path_pre**: input the need-to-predict 2 feature vectors in 2 ".csv" files named with author's name.

    [*dir*]Features_pre---┬---[*file*]auth#1pre.csv-------[*row*]auth#1apk#1pre
                          └---[*file*]auth#2pre.csv-------[*row*]auth#2apk#1pre

**csv_path_all**: input all the other feature vectors in ".csv" files named with author's name.

    [*dir*]Features_all---┬---[*file*]auth#1all.csv---┬---[*row*]auth#1apk#1all
                          │                           ├---[*row*]auth#1apk#2all
                          │                           ├---...
                          │                           └---[*row*]auth#1apk#Nall
                          └---[*file*]auth#2all.csv---┬---[*row*]auth#2apk#1all
                                                      ├---[*row*]auth#2apk#2all
                                                      ├---...
                                                      └---[*row*]auth#2apk#Nall

# Experimental Result

