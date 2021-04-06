import pandas as pd

def calc_quantum(burst_time, p):
 
    quantum = 0
    for k in burst_time:
        quantum += k

    quantum = quantum / (len(burst_time))
    quantum = round(quantum, 2)

    quantum *= p

    return quantum

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

    quantum = calc_quantum(burst_time, p)

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

        if c == n:
            break

        j = i
        while i < n and t >= arrival_time[i]:
            ready_queue.append(i)
            i += 1

         
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
    print("Average Turn-Around Tme: %.3f"%(sum(tat)/n))
    print("Context Switches:", ncs)
    print()