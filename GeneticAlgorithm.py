from itertools import combinations
import random

#List for keeping track of the population
pop = []

#Create chromosomes based on randomly selected items from the list
#where the lowest number of choice is 2
def create_gnom(l):
    rand = random.sample(l, k = random.randint(2, len(l))) 
    gnom = [i if i in rand else 0 for i in l]
    return gnom

#Calculate the sum of non-zero elements from the list
def fitness(chrm):
    s = sum(chrm)
    if s<0:
        return s*-1
    return s

def crossover(x, y):
    #Check common elements between the lists
    li = list(set(x).intersection(y))
    #To prevent having a list of duplicate elements after crossover
    for i in li:
        if x.index(i) != y.index(i):
            return [x, y]
    n = len(x)
    r = random.randint(0, n - 1)
    a = x[0:r] + y[r:n]
    b = y[0:r] + x[r:n]
    return [a, b]

def mutation(x, l):
    n = len(x)
    r = random.randint(0, n - 1)
    c = random.choice(l)
    #To prevent having a list of duplicate elements after mutation
    if c not in x:
        x[r] = c
    return x

def bin_str(list, l):
    str = ""
    #To keep the original order same in the result
    for i in list:
        if i != 0:
            l[l.index(i)] = 1
    
    for i in l:
        if i == 1:
            str += "1"
        else:
            str += "0"
    return str

def genetic_algo(l):
    global pop
    #Check the total number of combinations having at least elements
    comb = [s for i in range(len(l), 1, -1) for s in combinations(l, i)]
    #Define number of chromosomes per run
    cpr = int((len(comb)+10)/2)
    #Maximum number of iterations after which the execution will be terminated
    mx = 100000
    for i in range(cpr):
        gnom = create_gnom(l)
        if gnom in pop:
            i-=1
        else:
            pop.append(gnom)
    
    while mx >0:
        #Sort the population based on fitness in ascending order
        pop.sort(key = fitness)
        
        #Return the string if the portion is found
        if fitness(pop[0]) == 0:
            return bin_str(pop[0], l)
        
        #Otherwise create new population for next generation
        npop = []
        
        for i in range(0, len(pop), 2):
            #Choose parents from the first 50% of the population 
            p1 = random.choice(pop[:len(pop)/2])
            p2 = random.choice(pop[:len(pop)/2])
            #Make crossover between the two
            npop.extend(crossover(p1, p2))
            prob = random.random()
            #Mutate based on the probability to create diverse offspring
            if prob < 0.5:
                mutation(npop[i], l)
            else:
                mutation(npop[i+1], l)
        pop = npop.copy()
        mx-=1
    return -1


filename = input("Enter the file name: ")
l= []
with open(filename) as f:
    n = int(f.readline().rstrip())
    #Check if 1<= N <=10^2
    if n in range(1, (10**2)+1):
        for idx, line in enumerate(f):
            s = int(line.split()[1])
            #Check if 1<= S <=10^5
            if s in range(1, (10**5)+1):
                l.append(s)
                if line.startswith('l'):
                    l[idx] *= -1
            else:
                print('Invalid amount of transaction')
                break
    else:
        print('Invalid number for daily transactions')

#print(l)
print(genetic_algo(l))