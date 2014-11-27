import sumaFotosParalelo
import numpy as np
import time
from PIL import Image
from os import system

transp=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
def toGif(fp,delay,output):
    #el delay representa la pausa entre una imagen y otra y loop 0 especifica que el gif se repite en un bucle. *jpg tomara todos los archivos *jpg (para este caso, puede ser cualquier formato de imagen)
    system('convert -delay %d -loop 0 %s %s ' % (delay,fp,output))
def main():
    starting_point=time.time()
    for valor in transp:
        system('mpiexec -np 2 python sumaFotosParalelo.py galaxia.jpg barco.jpg '+ str(valor))
        nombreSalida='Imagenes/sumaAnimacion.gif'
        delay=15
    filepath='Imagenes/*jpg'
    toGif(filepath,delay,nombreSalida)

    elapsed_time=time.time()-starting_point
    print ""
    print "Parallel Time [seconds]: " + str(elapsed_time)

main()




