# EDIT THIS

# LARCV AND LARLITE DIRS
MY_LARLITE=/Users/twongjirad/working/uboone/larlite
MY_LARCV=/Users/twongjirad/working/larbys/LArCV
MY_LARLITECV=/Users/twongjirad/working/larbys/larlitecv

# optional
#MY_PYLARD_ENV=/Users/twongjirad/working/uboone/pylard2/env

#SETUP LARLITE
cd $MY_LARLITE/config
source setup.sh
cd -

# SETUP LARCV
source $MY_LARCV/configure.sh

# SETUP LARLITECV
source $MY_LARLITECV/configure.sh

# (opt) pylard for viewing
#source ${MY_PYLARD_ENV}/bin/activate