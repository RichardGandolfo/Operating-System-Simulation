#This program simulates some functionality of an operating system and focuses on CPU and hard disk scheduling

#Simplified PCB
class Process:
    def __init__(self,pid,prio):
        self.pid=pid
        self.prio=prio

#Error check for integer input
def numcheck(number):
    while(number.isdigit()==False):
        number = input("Enter a valid number: ")
    return int(number)

#Error check for valid integer
def rangecheck(number):
    while(number <= 0 or number > 4000000000):
        number = input("Enter a valid number: ")
        number=numcheck(number)
    return int(number)

#Breaks up user input to determine if valid command, then executes
def parse(cmd):
    if(cmd=='t'):
        if(len(CPU)==0):
            print("There is no process currently using the CPU")
        else:
            exet()
    elif(len(cmd)<3):
        return False
    elif(cmd[:2]=="A "):
        prio = ""
        for x in cmd[2::]:
            prio+=x
        if(prio.isdigit()):
            prio=int(prio)
            exeA(prio)
        else:
            return False
    elif(cmd[:2]=="d "):
        dn = ""
        filename = ""
        counter = 3
        for x in cmd[2::]:
            if(x!=" "):
                dn+=x
                counter+=1
            else:
                for y in cmd[counter::]:
                    filename+=y
                break
        if(dn.isdigit() and len(filename)!=0 and not filename.isspace()):
            dn=int(dn)
            exed(dn, filename)
        else:
            return False
    elif(cmd[:2]=="D "):
        dn = ""
        for x in cmd[2:]:
            dn+=x
        if(dn.isdigit()):
            dn=int(dn)
            if(dn>=len(harddisks)):
                print("Invalid disk number")
            elif(len(harddisks[dn])==0):
                print("There is no process using this hard disk")
            else:
                exeD(dn)
        else:
            return False
    elif(cmd[:2]=="m "):
        addr=""
        for x in cmd[2:]:
            addr+=x
        if(addr.isdigit()):
            addr=int(addr)
            if(len(CPU)!=0):
                exem(addr)
            else:
                print("There is no process currently using the CPU")
        else:
            return False
    elif(cmd=="S r"):
        exeSr()
    elif(cmd=="S i"):
        exeSi()
    elif(cmd=="S m"):
        exeSm()
    else:
        return False

#Returns index of least recently used page in frame table
def findOldestSpot():
    index=0
    target = framet[0]
    for i in range(0,len(framet)):
        if(framet[i][2]<target[2]):
            target = framet[i]
            index=i
    return index

#Helps t command by setting index to a "deleted" value -1
def removeFromFrame(proc):
    for i in range(0,len(framet)):
        if(framet[i][0]==proc.pid):
            framet[i]=(-1,0,0)

#Check is frame table has entry with specified process and page
def containsPage(proc,page):
    for x in framet:
        if(x[0]==proc.pid and x[1]==page):
            return True
    return False

#See if frame table is empty
def emptyTable():
    for x in framet:
        if(x[0]!=-1):
            return False
    return True

#Return index of table containing given process with page
def findIndex(proc,page):
    for i in range(0,len(framet)):
        if(framet[i][0]==proc.pid and framet[i][1]==page):
            return i

#Check if another entry can be added to frame table
def spaceAvailable():
    for x in framet:
        if(x[0]==-1):
            return True
    return False

#Find first available spot in frame table
def findFirstSpot():
    for i in range(0,len(framet)):
        if(framet[i][0]==-1):
            return i

#Adds new page to frame table when new process arrives or m command used
def addPage(proc,address):
    global time
    if(not containsPage(proc,address//pagesize)):
        if(spaceAvailable()):
            i = findFirstSpot()
            framet[i] = (proc.pid,address//pagesize,time)
            time+=1
        else:
            i = findOldestSpot()
            framet[i] = (proc.pid,address//pagesize,time)
            time+=1
    else:
        i = findIndex(proc,address//pagesize)
        framet[i] = (framet[i][0], framet[i][1], time)
        time+=1

#Executes m command by calling addPage
def exem(addr):
    addPage(CPU[0],addr)

#Executes A command by adding new process using preemptive prio scheduling
def exeA(prioval):
    global pidtracker
    proc = Process(pidtracker,prioval)
    pidtracker+=1
    if(len(CPU)==0):
        CPU.append(proc)
        addPage(proc,0)
    elif(CPU[0].prio<proc.prio):
        readyq.append(CPU[0])
        readyq.sort(key=lambda x: x.prio, reverse=True)
        CPU[0]=proc
        addPage(proc,0)
    else:
        readyq.append(proc)
        readyq.sort(key=lambda x: x.prio, reverse=True)
        addPage(proc,0)

#Terminates process on CPU
def exet():
    if(len(readyq)!=0):
        removeFromFrame(CPU[0])
        CPU[0] = readyq[0]
        readyq.pop(0)
    else:
        removeFromFrame(CPU[0])
        CPU.pop(0)

#Moves process obj from CPU to specified disk
def exed(disk,fname):
    if(disk<0 or disk>=len(harddisks)):
        print("Invalid disk index")
    elif(len(CPU)==0):
        print("There is no process currently using the CPU")
    else:
        harddisks[disk].append((CPU[0],fname))
        CPU.pop(0)
        if(len(readyq)!=0):
            CPU.append(readyq[0])
            readyq.pop(0)

#Returns process to ready queue from given disk
def exeD(dn):
    if(len(CPU)==0):
        CPU.append(harddisks[dn][0][0])
        harddisks[dn].pop(0)
    elif(CPU[0].prio<harddisks[dn][0][0].prio):
        readyq.append(CPU[0])
        readyq.sort(key=lambda x: x.prio, reverse=True)
        CPU[0] = harddisks[dn][0][0]
        harddisks[dn].pop(0)
    else:
        readyq.append(harddisks[dn][0][0])
        readyq.sort(key=lambda x: x.prio, reverse=True)
        harddisks[dn].pop(0)

#Displays ready queue and CPU processes
def exeSr():
    if(len(CPU)==0):
        print("CPU and ready queue are both empty")
    else:
        print("Using CPU:     PID:",CPU[0].pid,"Priority:",CPU[0].prio)
        print("Ready queue:")
        for x in readyq:
            print("               PID:",x.pid,"Priority:",x.prio)
        print("")

#Displays processes using disks and on i/o queue
def exeSi():
    counter = 0
    for disknum in harddisks:
        print("Hard disk #"+str(counter))
        for x in disknum:
            if(len(disknum)!=0):
                if(x==disknum[0]):
                    print("Currently using hard disk:    PID:",x[0].pid,"File:",x[1])
                else:
                    print("                   Waiting:   PID:",x[0].pid,"File:",x[1])
        print("")
        counter+=1

#Shows memory with each frame and the process/page in that frame
def exeSm():
    if(emptyTable()):
        print("The frame table is empty")
    else:
        for i in range(0,len(framet)):
            if(framet[i][0]!=-1):
                print("Frame #"+str(i)+" has:  PID:",framet[i][0],"Page:",framet[i][1],"Time:",framet[i][2])
                print("")

#Initializes OS and constantly waits for commands
def main():
    numbytes = input("How much RAM memory (in bytes) is on the computer? ")
    numbytes = numcheck(numbytes)
    numbytes = rangecheck(numbytes)

    global pagesize
    pagesize = input("What is the page size? ")
    pagesize = numcheck(pagesize)
    pagesize = rangecheck(pagesize)
    while(pagesize>numbytes):
        pagesize = input("Enter a valid number: ")
        pagesize = numcheck(pagesize)
        pagesize = rangecheck(pagesize)

    numdisks = input("How many hard disks does the simulated computer have? ")
    numdisks = numcheck(numdisks)
    numdisks = rangecheck(numdisks)

    global numpages
    numpages = numbytes//pagesize

    global harddisks
    harddisks = [[] for x in range(0,numdisks)]

    global framet
    framet = [(-1,0,0) for x in range(0,numpages)]

    while(True):
        cmd = input("> ")
        if (parse(cmd)==False):
            print("Invalid command")

pagesize = 0
numpages = 0
pidtracker = 1
time = 1
framet = []
CPU = []
harddisks = []
readyq = []

main()
