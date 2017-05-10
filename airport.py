# -*- coding: cp1252 -*-
"""
Application des  fils d'éxecution et files d'attente :
  La simulation d’un Aéroport
  L'équipe :
            Dobrescu Alexandra
            Dragomir Gabriel
            Felciuc Vlad
  Groupe: 1220F
le 10 April 2017
"""

import time
import random
import logging
import sys, os
import multiprocessing
from multiprocessing import Process, Queue, current_process, freeze_support
import sys, threading, logging, os
import datetime
from time import gmtime, strftime

#
# Function run by worker processes
#

def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = execute_function(func, args)
        output.put(result)

#
# Function used to calculate result
#

def execute_function(func, args):
    result = func(args)
    return '%s says that %s %s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# Functions referenced by tasks
#

def message_air (flight) :
    return "Flight no. " + flight + "has joined the AIR queue.\r\n"

def message_ground (flight) :
    return "Flight no. " + flight + "has joined the GROUND queue.\r\n"

def utilisation():
    print 
    """
          Le programme doit etre appelle avec minimum 1 argument:
          python flight_process.py Nom_de_fichier.txt (dans ce cas le nom de
          fichier est avioane.txt)
    """

def main(argv=None):
    working_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
    #Configurez le logging pour ecrire dans un fichier texte
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        filename=working_dir + 'process.log',
                        level=logging.INFO)
    logging.info("Main start")
    
    #Bucla principala
    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        utilisation()
        return 0
    else:
        NUMBER_OF_PROCESSES = 4
        #aici punem listele in care stocam avioanele care se afla la sol sau nu 
        airThread = []
        groundThread = []

    # Cream cozi
        airQueue = Queue()
        groundQueue = Queue()


    print ( "Airport Runway Simulator" )
    print ( "\r\n" )

    with open(working_dir+argv[1], 'r') as f:
        # indexAir = 0
        # indexGround = 0
        for line in f:
            time.sleep(2)
            if line [0:3] == "air":
                line.strip('\r\n')
                airQueue.put(line)
                airThread.append(line[len(line)-4: len(line)-1])
                # indexAir = indexAir + 1
                localtime = strftime("%H:%M:%S", gmtime())
                print (localtime + " - Flight no." + airThread[airQueue.qsize()-1] + " has joined the AIR queue.\r\n")

            elif line [0:6] == "ground":
                line.strip('\r\n')
                groundQueue.put(line)
                groundThread.append(line[len(line)-4: len(line)-1])
                # indexGround = indexGround + 1
                localtime = strftime("%H:%M:%S", gmtime())
                print (localtime + " - Flight no." + groundThread[groundQueue.qsize()-1] + " has joined the GROUND queue.\r\n" )

            elif line [0] == " ":
                while not( airQueue.empty() ) or not( groundQueue.empty() ):
                    # print indexAir
                    # print indexGround
                    localtime = strftime("%H:%M:%S", gmtime())
                    print (localtime)
                    time.sleep(0.5)
                    print ("There are " + str(airQueue.qsize()) + " in the AIR queue.")
                    time.sleep(0.5)
                    print ("There are " + str(groundQueue.qsize()) + " on the GROUND queue.\r\n")
                    time.sleep(1)
                    if not(airQueue.empty()):
                        print ("Flight no. " + airThread[0] + " is now landing.\r\n")
                        airQueue.get()
                    elif not(groundQueue.empty()):
                        print ("Flight no. " + groundThread[0] + " is taking off.\r\n")
                        groundQueue.get()

                    time.sleep(3)
                    localtime = strftime("%H:%M:%S", gmtime())
                    print ("Runway is clear.")
                    time.sleep(0.5)
                    print ("Time is " + localtime + "\r\n")
   
    # Submit tasks (on met en queue les threads)
    for air in airThread:
       # logging.info(air)
        airQueue.put(air)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(airQueue, groundQueue)).start()

    # Get and print results
    for i in range(len(airThread)):
       # logging.info(done_queue.get())
       print (groundQueue.get())

    # Add more tasks using `put()`
    for ground in groundThread:
        logging.info(ground)
        airQueue.put(ground)

    # Get and print some more results
    for i in range(len(groundThread)): 
        print (groundQueue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        airQueue.put('STOP')
      
    logging.info("Main stop")
    return 0

if __name__ == '__main__':
    #freeze_support()
    sys.exit(main())
