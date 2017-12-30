# Operating-System-Simulation

***Requires Python 3 Installation***

Simulation of operating system key features and helps the user understand how the OS interacts with hardware. The simulation handles CPU scheduling using preemptive priority, disk scheduling using first come first serve (FCFS), and memory management using paging (virtual memory). 

***Valid commands***

A priority    ‘A’ input means that a new process has been created. This process has the specified priority. For example, the    input A 2 means that a new process has arrived. This process has the priority of 2.

t     The process that is currently using the CPU terminates. It leaves the system immediately. 

d number file_name    The process that is currently using the CPU requests the hard disk <number>. It wants to read or write file <file_name>.

D number   The hard disk has finished the work for one process.

m address   The process that is currently using the CPU requests a memory operation for the address.

S r     Shows what process is currently using the CPU and what processes are waiting in the ready-queue.

S i      Shows what processes are currently using the hard disks and what processes are waiting to use them. For each busy hard disk it shows the process that uses it and its I/O-queue. 

S m    Shows the state of memory. For each used frame, it displays the process number that occupies it and the page number stored in it.

***Running the program***
Linux: python3 OperatingSystem.py
Windows: py OperatingSystem.py



