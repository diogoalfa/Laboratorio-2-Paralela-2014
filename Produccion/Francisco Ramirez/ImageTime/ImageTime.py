__author__ = 'francisco'
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 14:31:26 2014

@author: paralela
"""
import numpy as np
from StringIO import StringIO
import time
from mpi4py import MPI
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import time

starting_point=time.time()



comm = MPI.COMM_WORLD  # comunicador entre dos procesadores
rank = comm.rank     # id procesador actual
size = comm.size     # cantidad de procesadores a usar


def main():
    starting_point=time.time()
    if rank==1:
        im=comm.recv(source=0)
        ok=0
        comm.send(ok,dest=0)

    if rank==0:
        ruta="6MP"
        ext=".jpeg"

        print ""
        print "Abriendo imagen..."
        openIniTime=time.time()
        img=Image.open(ruta+ext)
        openEndTime=time.time()-openIniTime
        print "Image time: ",openEndTime

        print ""
        print "To RGB..."
        openIniTime=time.time()
        img=np.array(img.convert("RGB"))
        openEndTime=time.time()-openIniTime
        print "RGB time: ",openEndTime

        print ""
        print "Comunication time..."
        openIniTime=time.time()
        comm.send(img,dest=1)
        ok=comm.recv(source=1)
        openEndTime=time.time()-openIniTime
        print "Comunication time: ",openEndTime

        print ""
        print "Build imagen..."
        openIniTime=time.time()
        imgContrucFinal=Image.fromarray(img)
        openEndTime=time.time()-openIniTime
        print "Construction time: ",openEndTime

        print ""
        print "Save imagen..."
        openIniTime=time.time()
        imgContrucFinal.save(ruta+ext)
        openEndTime=time.time()-openIniTime
        print "Save time: ",openEndTime


        elapsed_time=time.time()-starting_point
        print ""
        print "Total Time [seconds]: " + str(elapsed_time)



main()
