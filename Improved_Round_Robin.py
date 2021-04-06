import pandas as pd

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
        ready_queue[i], ready_queue[0] = ready_queue[0], ready_queue[i]
        heapify(ready_queue, rem_bt, i, 0)

    return ready_queue
    

if __name__ == "__main__":

    data = pd.read_csv('dataset-200.csv')

    arrival_time = data['Arrival Time']
    burst_time = data['Burst Time']

    n = len(arrival_time)

    p = 0.85

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

    print()
    print("pid | Arrival Time | Burst Time | Response Time | Completion Time | Waiting Time | Turn-Around Time")
    print("---------------------------------------------------------------------------------------------------")

    for i in range(n):
        print("%3d | %12.2f | %10.2f | %13.2f | %15.2f | %12.2f | %16.2f" % (i+1, arrival_time[i], burst_time[i], rt[i], ct[i], wt[i], tat[i]))

    print("\nAverage Response Time: %.3f"%(sum(rt)/n))
    print("Average Waiting Time: %.3f"%(sum(wt)/n))
    print("Average Turn-Around Time: %.3f"%(sum(tat)/n))
    print("Context Switches:", ncs)
    print()