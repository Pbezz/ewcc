import numpy as np

def evaluate(factor, arrival, bonus, reward, duration, time_bonus):
    t = len(factor)
    p = len(factor[0])
    niceness = [0 for _ in range(t)]
    for i in range(t):
        niceness[i]=factor[i][np.argmax(factor[i])] * (2*reward[i]+bonus[i]-duration[i]-0.5*time_bonus[i]);
        #niceness[i]=factor[i][np.argmax(factor[i])] * (bonus[i]/2 + reward[i]);
        #niceness[i]=factor[i][np.argmax(factor[i])] * (reward[i]+bonus[i])

    return niceness

def too_long(start, arrival, time_bonus, duration):
    return start 

def assign_tasks(factor, arrival, bonus, reward, duration, time_bonus):
    t = len(factor)
    p = len(factor[0])
    niceness = evaluate(factor, arrival, bonus, reward, duration, time_bonus)
    # each processor has a list of tasks and their beginning times 
    assignment = [(0,0) for _ in reward]
    time_slots = [[(0,-1)] for _ in range(p)]
    # get indexes of tasks by reward
    indexes = np.argsort(niceness)[::-1]
    
    for i in indexes:
        # get indexes of processors by factor
        
        got_slot = False
        p_idx = np.argsort(factor[i])[::-1]
        j = 0
        while not got_slot:
            fav_p = p_idx[j]
            slots = time_slots[fav_p]
            slots.sort(key=lambda x: x[0])
            s = 0

            for s in range(len(slots)):
                if slots[s][1] == -1 or max(slots[s][0], arrival[i]) + duration[i] <= slots[s][1]:
                    if j < p-1 and  slots[s][0] > 3*arrival[i]:
                        break
                    # put task in slot, starting at max(slots[s][0], arrival[i])
                    start = max(slots[s][0], arrival[i])
                    if start < arrival[i]:
                        continue
                    assignment[i] = (fav_p, start)
                    
                    # remove slot and add new slots if necessary
                    t_slots = slots.copy()
                    if start > t_slots[s][0]:
                        slots.append((slots[s][0], start))
                    if t_slots[s][1] == -1 or start + duration[i] < t_slots[s][1]:
                        slots.append((start + duration[i], slots[s][1]))
                    
                    slots.pop(s)
                    slots = sorted(slots, key=lambda x: x[0])
                    time_slots[fav_p] = slots
                    got_slot = True
                    break 
            j += 1
    return assignment