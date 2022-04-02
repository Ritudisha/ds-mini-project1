import rpyc
from rpyc.utils.server import ThreadedServer
import data_sync
import datetime
date_time=datetime.datetime.now()

class MonitorService(rpyc.Service):
 stat = False
 Processes = []
 def on_connect(self,conn):
  print("\nconnected on {}".format(date_time))
 
 def exposed_change_stat(self):
   MonitorService.stat = True

 def exposed_return_stat(self):
   return MonitorService.stat

 def on_disconnect(self,conn):
  MonitorService.stat = False
  print("disconnected on {}\n".format(date_time))

 def exposed_start_processes(self, params):
   MonitorService.Processes = data_sync.main(params)
   MonitorService.stat = True
   return True

 def exposed_execute_command(self, params):
   print('received command from client', params)
   return data_sync.run_commands(params, MonitorService.Processes, MonitorService.stat)

 def exposed_isrunning(self):
   #print(clock_sync.isRunning())
   return MonitorService.stat
 
if __name__=='__main__': 
    t=ThreadedServer(MonitorService, port=18813)
    t.start()