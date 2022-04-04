import random
from sqlite3 import Timestamp
import sys
import datetime
import _thread
import time

# global variables
processes = []
running = False
system_start = datetime.datetime.now()
t = 10
time_cs = random.randint(5, 5)

class Process:
    def __init__(self, id, name, state,label):
        self.id = id
        self.name = name
        self.state = state
        self.label= label
        self.elections = 0
        self.held_time = time 
        self.time_start = time
        self.set_time = time
        self.requestQueue = {}
        self.permissions = {}
        self.request_timestamp = time
        self.timeout = random.randint(5, t)

    # starts a thread that runs the process
    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        # with t second interval, update clock
        while True:
            time.sleep(self.timeout)
            self.update_state()

    def update_state(self):
        global p_holding_CS
        if(self.state == 'DO-NOT-WANT'):
            self.state = 'WANTED'
            self.request_timestamp = time.time()
            if(self.send_request()):
                self.state = 'HELD'
                p_holding_CS = self
                _thread.start_new_thread(critical_section_tick, ())
                self.held_time = time.time()
        elif(self.state == 'WANTED'):
            if(self.is_available()):
                self.state = 'HELD'
                p_holding_CS = self
                _thread.start_new_thread(critical_section_tick, ())
                self.held_time = time.time()
        elif(self.state == 'HELD'):
            now = time.time()
            self.state = 'DO-NOT-WANT'
            p_holding_CS = None
            for p in processes:
                self.grant_permission(p)
            self.request_timestamp = time

    def kill(self):
        _thread.kill()

    def permission(self, sent_by, time):
        if(self.state == 'DO-NOT-WANT'):
            return True
        if(self.state == 'HELD'):
            self.requestQueue[sent_by] = time
            return False
        if(self.state == 'WANTED'):
            if(self.request_timestamp > time):
                return True
            return False

    def send_request(self):
        t = time.time()
        for p in processes:
            self.permissions[p.id] = p.permission(self.id, t)
                
        return self.is_available()

    def is_available(self):
        return len([p for p in self.permissions.values() if p == True]) == (len(processes) - 1)

    def grant_permission(self, to):
        to.permissions[self.id] = True

p_holding_CS = Process
def critical_section_tick():
    time.sleep(time_cs)
    try:
        if(p_holding_CS != None):
            print(p_holding_CS.id, p_holding_CS.state)
            p_holding_CS.update_state()
        return None   
    except AttributeError:
        return None



def tick(running, processes):
    # program ticks evey second 
    while running:
        time.sleep(1)

def update_master(value):     
        for p in processes:
            if p.label == 'C':
                p.state = value

def update_p_t(tm):
    #print(f'Caching time for update {t}')
    for p in processes:
        p.timeout = random.randint(5, tm)

def update_cs_t(tm):
    global time_cs
    #print(f'Caching time for update {t}')
    time_cs = random.randint(10, tm)

def list(processes):
    # utility method to list proceeses
    for p in processes:
        str = f"{p.name}, {p.state}" 
        print(str, end="\n")


def parse_lines(lines):
    # utility method to parse input
    result = []
    for l in lines:
        p = l.split(",")
        id = int(p[0].strip())
        name = p[1].strip().split("_")[0]
        state = p[2]
        label=p[3].strip()
        result.append([id, name, state,label])
    return result


def main(args):
    # main program function
    print(args)
    if len(args) == 1:
        try:
            n = int(args)
            ids = []
            for p in range(n):     
                if p not in ids:
                    #print(p[3])
                    processes.append(Process(p, f'p_{p}', 'DO-NOT-WANT','S'))
                    ids.append(p)
                else:
                    print("[WARNING] Duplicate procees id %d discarded" % p[0])
            
        except:
            raise
    else:
        print("[WARNING] No input file provided.")
        print("Loading default test values.")

    # start threads of all processes
    for p in processes:
        p.start()

    # start the main loop
    running = True

    # start a separate thread for system tick
    _thread.start_new_thread(tick, (running, processes))
    return processes

def isRunning():
    return running

def run_commands(inp, procs, stat):
    global running
    running = stat
    processes = procs
    cmd = inp.split(" ")

    command = cmd[0]

    if len(cmd) > 3:
        print("Too many arguments")

    # handle exit
    elif command == "exit":
        running = False
        print("Program exited")
    # handle list
    elif command == "list":
        try:
            list(processes)
        except: 
            print("Error")
    elif command == "time-p":
        try:
            update_p_t(int(inp.split(" ")[1]))
        except:
            print("Error")

    elif command == "time-cs":
        try:
            update_cs_t(int(inp.split(" ")[1]))
        except:
            print("Error")
    
    # handle unsupported command        
    else:
        print("Unsupported command:", inp)
