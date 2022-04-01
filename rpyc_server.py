import rpyc
from rpyc.utils.server import ThreadedServer
import lamport2
import datetime
import sys
import threading
import time
import signal 
date_time=datetime.datetime.now()

class MonitorService(rpyc.Service):
  stat = False
  threads = []
  def on_connect(self,conn):
    print("\nconnected on {}".format(date_time))
  
  def exposed_change_stat(self):
    MonitorService.stat = True

  def exposed_return_stat(self):
    return MonitorService.stat

  def on_disconnect(self,conn):
    MonitorService.stat = False
    print("disconnected on {}\n".format(date_time))

  def exposed_initialize_thread(self, name, initially_granted, procs):
    self.threads.append(lamport2.Process(name, initially_granted, list(set(procs) - {name})))

  def exposed_start(self):
        lamport2.main(self.threads)
 
def start_server(server):
  server.start()
if __name__=='__main__': 
  try:
      t=ThreadedServer(MonitorService, port=18813, )
      thread = threading.Thread(target = start_server, args={t,}, daemon=True)
      
      thread.start()
      while True:
        time.sleep(1.0)

  except KeyboardInterrupt:
      print("Ctrl-c pressed")
      print("Resource usage:")
      print(lamport2.current_resource_usage())
      sys.exit(1)