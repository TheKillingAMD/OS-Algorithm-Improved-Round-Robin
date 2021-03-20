import pandas as pd
import csv
import numpy
import pytz
import dateutil

def calc_quantum(ready_queue, burst_time, c, p):

    if len(ready_queue) == c:
        return 0
 
    quantum = 0
    for k in ready_queue:
        quantum += burst_time[k]

    quantum = quantum / (len(ready_queue)-c)
    quantum = round(quantum, 2)

    quantum *= p

    return quantum

def heapify(ready_queue, rem_bt, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and rem_bt[ready_queue[largest]] < rem_bt[ready_queue[l]]:
        largest = l
 
    if r < n and rem_bt[ready_queue[largest]] < rem_bt[ready_queue[r]]:
        largest = r

    if largest != i:
        ready_queue[i], ready_queue[largest] = ready_queue[largest], ready_queue[i]
        heapify(ready_queue, rem_bt, n, largest)
 
 
def sort(ready_queue, rem_bt):
    n = len(ready_queue)
 
    for i in range(n//2 - 1, -1, -1):
        heapify(ready_queue, rem_bt, n, i)

    for i in range(n-1, 0, -1):
        ready_queue[i], ready_queue[0] = ready_queue[0], ready_queue[i]  # swap
        heapify(ready_queue, rem_bt, i, 0)

    return ready_queue
    

# if __name__ == "__main__":
for p in range(1,101):

    data = pd.read_csv('dataset-200.csv')

    arrival_time = data['Arrival Time']
    burst_time = data['Burst Time']

    # arrival_time = [0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,7,8,8,8,10,10,10,10,10,10]
    # burst_time = [3,12,4,9,12,2,2,10,11,5,9,1,1,3,9,8,2,5,8,8,10,4,6,8,1,9,3,8,11,10,12,5,3,3,5,6,2,4,7,9,1,1,3,8,11,8,1,12,6,2]

    n = len(arrival_time)

    p = p/100

    ready_queue = []

    i = 0
    while i < n and arrival_time[i] == 0:
        ready_queue.append(i)
        i += 1

    t = arrival_time[ready_queue[0]]
    k = 0
    c = 0

    ct = []
    wt = []
    tat = []
    rt = []

    rem_bt = [0] * n
    for j in range(n): 
        rem_bt[j] = burst_time[j]
        wt.append(0)
        tat.append(0)
        ct.append(0)
        rt.append(0)

    ncs = 0

    quantum = calc_quantum(ready_queue, burst_time, 0, p)
    ready_queue = sort(ready_queue, rem_bt)

    while c < n:

        if rem_bt[ready_queue[k]] == burst_time[ready_queue[k]]:
            rt[ready_queue[k]] = t - arrival_time[ready_queue[k]]

        if rem_bt[ready_queue[k]] > quantum:
            rem_bt[ready_queue[k]] -= quantum
            t += quantum
            
        elif rem_bt[ready_queue[k]] != 0:
            t += rem_bt[ready_queue[k]]
            rem_bt[ready_queue[k]] = 0
            ct[ready_queue[k]] = t
            tat[ready_queue[k]] = ct[ready_queue[k]] - arrival_time[ready_queue[k]]
            wt[ready_queue[k]] = tat[ready_queue[k]] - burst_time[ready_queue[k]]
            c += 1

        if rem_bt[ready_queue[k]] != 0 and rem_bt[ready_queue[k]] <= quantum:
            t += rem_bt[ready_queue[k]]
            rem_bt[ready_queue[k]] = 0
            ct[ready_queue[k]] = t
            tat[ready_queue[k]] = ct[ready_queue[k]] - arrival_time[ready_queue[k]]
            wt[ready_queue[k]] = tat[ready_queue[k]] - burst_time[ready_queue[k]]
            c += 1

        if c == n:
            break

        j = i
        while i < n and t >= arrival_time[i]:
            ready_queue.append(i)
            i += 1

        if j!=i:
            w = ready_queue[0]
            quantum = calc_quantum(ready_queue, rem_bt, c, p)
            ready_queue = sort(ready_queue, rem_bt)

            k = 0
            while rem_bt[ready_queue[k]] == 0:
                k  = (k+1)%len(ready_queue)

            if ready_queue[k] != w:
                ncs += 1
        else:    
            k  = (k+1)%len(ready_queue)

            if c != n-1:
                ncs += 1

            while rem_bt[ready_queue[k]] == 0:
                k  = (k+1)%len(ready_queue)

    ncs += 1

    # print()
    # print("pid | Arrival Time | Burst Time | Response Time | Completion Time | Waiting Time | Turn-Around Time")
    # print("---------------------------------------------------------------------------------------------------")

    # for i in range(n):
    #     print("%3d | %12.2f | %10.2f | %13.2f | %15.2f | %12.2f | %16.2f" % (i+1, arrival_time[i], burst_time[i], rt[i], ct[i], wt[i], tat[i]))

    print(p*100,"%.3f"%(sum(rt)/n),"%.3f"%(sum(wt)/n),"%.3f"%(sum(tat)/n),ncs)
