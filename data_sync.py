import random
import sys
import datetime
import _thread
import time

# global variables
processes = []
running = False
system_start = datetime.datetime.now()
t = 10
CSQueue = []
time_cs = random.randint(10, 20)


class Process:
    def __init__(self, id, name, data,label):
        self.id = id
        self.name = name
        self.data = data
        self.label= label
        self.elections = 0
        self.held_time = time 
        self.time_start = time
        self.set_time = time

    # starts a thread that runs the process
    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        # with 5 second interval, update clock
        while True:
            time.sleep(random.randint(5, t))
            self.update_data()

    def update_data(self):
        #self.data = 'DO-NOT-WANT' if self.data == 'WANTED' else 'WANTED'
        if(self.data == 'DO-NOT-WANT'):
            self.data = 'WANTED'
            CSQueue.append(self)
        if(self.data == 'WANTED'):
            if(len([p for p in processes if p.data == 'HELD']) == 0):
                p = CSQueue.pop(0)
                p.data = 'HELD'
                p.held_time = time.time()
        if(self.data == 'HELD'):
            now = time.time()
            if((now - self.held_time) >= time_cs):
                self.data = 'DO-NOT-WANT'
                if(len(CSQueue) > 0):
                    next_process = CSQueue.pop(0)
                    next_process.data = 'HELD'
                    next_process.held_time = time.time()
    def kill(self):
        _thread.kill()

def tick(running, processes):
    # program ticks evey second 
    while running:
        time.sleep(1)

def update_master(value):     
        for p in processes:
            if p.label == 'C':
                p.data = value

def update_p_t(tm):
    global t
    #print(f'Caching time for update {t}')
    t = tm

def update_cs_t(tm):
    global time_cs
    #print(f'Caching time for update {t}')
    time_cs = random.randint(10, time_cs)

def list(processes):
    # utility method to list proceeses
    for p in processes:
        str = f"{p.name}, {p.data}" 
        print(str, end="\n")


def parse_lines(lines):
    # utility method to parse input
    result = []
    for l in lines:
        p = l.split(",")
        id = int(p[0].strip())
        name = p[1].strip().split("_")[0]
        data = p[2]
        label=p[3].strip()
        result.append([id, name, data,label])
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
    elif command == "update":
        try:
            update_master(inp.split(" ")[1])
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
