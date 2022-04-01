import signal
import rpyc
import sys
import time
import threading

def signal_handler(conn):
    conn.root.handle

def start(conn):
   conn.root.start()

if len(sys.argv) < 2:
   exit("Usage {} SERVER".format(sys.argv[0]))
 
server = sys.argv[1]
initially_granted_proc = "A"
procs = {"A", "B", "C"}
try:
   conn = rpyc.connect(server,18813)

   conn.root.initialize_thread("A", initially_granted_proc, procs)
   conn.root.initialize_thread("B", initially_granted_proc, procs)
   conn.root.initialize_thread("C", initially_granted_proc, procs)
   #signal.signal(signal.SIGINT, signal_handler)
   thread1 = threading.Thread(target = start, args={conn,}, daemon=True)
   thread1.start()
   while True:
         time.sleep(1.0)

except EOFError:
   print('exited')
except KeyboardInterrupt:
   print('exited')
  
   


 
 