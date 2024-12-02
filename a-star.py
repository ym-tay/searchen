openl=[]
closel=[]
t=[[0,2,4,-1,-1],
   [-1,0,1,7,-1],
   [-1,-1,0,3,5],
   [-1,-1,-1,0,2],
   [-1,-1,-1,-1,0]]
def heur(s):
    match s:
        case 1:
            return 7
        case 2:
            return 6
        case 3:
            return 3
        case 4:
            return 2
        case 5:
            return 0
def voisin(s):
    l=[]
    r=t[s]
    for i in range(len(r)):
        if r[i]!= -1 and r[i]!=0:
            l.append(i)
    return l
def a_star(start, goal):
    openl.append((start, 0, heur(start)))
    while openl:
        openl.sort(key=lambda x: x[2])
        current, g, f = openl.pop(0)
        closel.append(current)
        if current == goal:
            print(f"Goal atd: {goal}")
            return
        for neighbor in voisin(current):
            if neighbor in closel:
                continue
            new_g = g + t[current][neighbor]
            new_f = new_g + heur(neighbor)
            found = False
            for i, (n, g_old, f_old) in enumerate(openl):
                if n == neighbor:
                    found = True
                    if new_f < f_old:
                        openl[i] = (neighbor, new_g, new_f)
            if not found:
                openl.append((neighbor, new_g, new_f))

    print("Goal non atd")

a_star(0, 4)
 
