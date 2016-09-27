import os,sys
from time import time

s = time()
import ROOT
from larlite import larlite
from larcv import larcv
from larlitecv import larlitecv
print "load libraries: ",time()-s

# make the data coordindator
dataco = larlitecv.DataCoordinator()

using_filelists = False

if using_filelists:
    # one can use filelists to specify file locations
    fin_larlite = "ex_databnb_larlite.txt"
    fin_larcv   = "ex_databnb_larcv.txt"

    dataco.set_filelist( fin_larlite, "larlite" )
    dataco.set_filelist( fin_larcv, "larcv" )
else:
    # one can add files one at a time
    fin_larlite = ["data/data_samples/v05/data_extbnb_to_larcv_v00_p00/larlite_opdigit_0000.root",
                   "data/data_samples/v05/data_extbnb_to_larcv_v00_p00/larlite_wire_0000.root",
                   "data/data_samples/v05/data_extbnb_to_larcv_v00_p00/larlite_opreco_0000.root"]
    fin_larcv   = ["data/data_samples/v05/data_extbnb_to_larcv_v00_p00/supera_data_0000.root"]
    
    for f in fin_larlite:
        dataco.add_inputfile( f, "larlite" )
    for f in fin_larcv:
        dataco.add_inputfile( f, "larcv" )

# note that if one both specifies a filelist and then adds files, the filelist takes priority.
# mixed usage not supported yet

# configure the iomanagers for both larlite and larcv
dataco.configure( "dataco.cfg", "StorageManager", "IOManager" )

# load the iomanagers
dataco.initialize()

entries = {}
entries["larlite"] = dataco.get_nentries("larlite")
entries["larcv"]   = dataco.get_nentries("larcv")
print "entries (larlite): ",entries["larlite"]
print "entries (larcv):   ",entries["larcv"]

# we pick which file type drives the event loop
driver = "larlite"

# get the iomanagers
larlite_io = dataco.get_larlite_io()
larcv_io   = dataco.get_larcv_io()

#for i in range(0,entries[driver]):
for i in range(0,10):
    a = time()
    dataco.goto_entry( i, driver )
    print "io time: ",time()-a
    # to reduce time, pick and choose the data products to read from disk
    # use the ReadOnlyX parameters in the configuration file

    # get stuff example
    event_imgs = larcv_io.get_data( larcv.kProductImage2D, "tpc" )   # tpc images from input larcv file
    opdata     = larlite_io.get_data(larlite.data.kOpDetWaveform, "pmtreadout" ) # pmt waveforms from input larlite file

    # do stuff example
    print "Entry: ",i
    print " LARLITE:",larlite_io.run_id(),larlite_io.subrun_id(),larlite_io.event_id()
    print " LARCV: ",event_imgs.run(),event_imgs.subrun(),event_imgs.event() 
    print " LARCV: ",event_imgs.run(),event_imgs.subrun(),event_imgs.event() 

    # define out image meta: defines image
    x_coord_width = 1500.0
    y_coord_width = 32.0
    num_rows = 32
    num_cols = 1500
    origin_x = 0
    origin_y = 0
    meta = larcv.ImageMeta( x_coord_width, y_coord_width, num_rows, num_cols, origin_x, origin_y )
    
    # create new image
    img = larcv.Image2D( meta )
    # blank it out to zero
    img.paint(0.0)

    # loop through pmt waveforms
    for n in xrange(opdata.size()):
        wf = opdata.at(n)
        pmt = wf.ChannelNumber()%100
        if wf.size()<500:
            continue
        if pmt>=32:
            continue

        for i in xrange(0,1500):
            adc = wf.at(i)-2048.0
            img.set_pixel( pmt, i, adc )

    # image defined. save it to larcv file
    larcv_outputcontainer = larcv_io.get_data( larcv.kProductImage2D, "pmtimage" )
    larcv_outputcontainer.Image2DArray().push_back( img )

    # make a larcv ROI
    myroi = larcv.ROI() # rois specify where in the image a particle (or something of interest) is occuring

    # make output container for ROI
    larcv_outputroi = larcv_io.get_data( larcv.kProductROI, "id" )

    # give the ROI a type. for more info on labels see: (https://github.com/LArbys/LArCV/blob/develop/core/DataFormat/DataFormatTypes.h)
    #myroi.Type( larcv.kROICosmic ) # typically label for background
    #myroi.Type( larcv.kROIBNB )    # typically label for neutrinos

    # put our ROI into the container
    larcv_outputroi.ROIArray().push_back( larcv.ROI() )

    # set the event id: this needs to be set to make sure the output is correct
    larcv_io.set_id( event_imgs.run(), event_imgs.subrun(), event_imgs.event() ) 
    larlite_io.set_id( event_imgs.run(), event_imgs.subrun(), event_imgs.event() ) 

    # put the data in the output containers into the tree
    larcv_io.save_entry()
    #larlite_io.write_event()

# write to disk
larcv_io.finalize()
larlite_io.close()


    
    
