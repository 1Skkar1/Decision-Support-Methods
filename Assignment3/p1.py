from prettytable import PrettyTable
import scipy.stats
import random
import math

dailyPackets = 0
toHome = 0
toLocker = 0
homeRemaining = 0
lockerRemaining = 0
dailyOC = 0
dailyPF = 0
dailyPickUp = 0
dailyCostOC = 0
dailyCostPF = 0
maxLockerItems = 0
maxItemsDay = 0

dailyHome = []
dailyLocker = []

deliveryPF = []
deliveryOC = []
deliveryLocker = []

accDeliveryPF = []
accDeliveryOC = []
accDeliveryLocker = []

costsPF = []
costsOC = []
costsAcc = []

toHomeStatus = []
toLockerStatus = []

totalCost = []
maxItems = []

def main():
    confidence = .99
    alpha = 1 - confidence
    observations = 10000
    compensation = 0
    probability = 0

    choice = input("Choose compensation:\n> 1) 0.0 € [  1 % probability ]\n> 2) 0.5 € [ 25 % probability ]\n> 3) 1.0 € [ 50 % probability ]\n> 4) 1.5 € [ 60 % probability ]\n> 5) 1.8 € [ 75 % probability ]\n")
    if choice == '1':
        compensation = 0
        probability = 1
    elif choice == '2':
        compensation = 0.5
        probability = 25
    elif choice == '3':
        compensation = 1
        probability = 50
    elif choice == '4':
        compensation = 1.5
        probability = 60
    elif choice == '5':
        compensation = 1.8
        probability = 75

    for n in range(0,observations):
        for days in range(1,121):
            RecipientPickUp(compensation, probability)
            LockerOrHome()
            DailyResults(days)
        PrintResults(compensation)
    ConfidenceInterval(compensation, alpha)

def RecipientPickUp(compensation, probability):
    global dailyCostOC, dailyCostPF
    global toHome, toLocker, dailyOC, dailyPF, dailyPickUp
    global homeRemaining, lockerRemaining
    
    dailyLimit = 0
    dailyCostOC = 0
    dailyCostPF = 0
    dailyOC = 0
    dailyPF = 0
    dailyPickUp = 0
    
    for i in range(0,lockerRemaining):
        lockerPickUp = random.randrange(0,101)  # 75% chance packet gets picked up
        if lockerPickUp < 75: # Packet gets picked up
            dailyPickUp += 1
            lockerRemaining -= 1
            if homeRemaining > 0:
                courier = random.randrange(0,101) # Chance of OC depending on chosen compensation
                if courier < probability:  # OC accepted
                    homeRemaining -= 1
                    dailyOC += 1
                    dailyCostOC += compensation
    
    while homeRemaining > 0:
        if dailyLimit < 10:
            dailyLimit += 1
            dailyCostPF += 1
        elif dailyLimit >= 10:
            dailyCostPF += 2
        dailyPF += 1
        homeRemaining -= 1

def LockerOrHome():
    global dailyPackets
    global toHome, toLocker
    global homeRemaining, lockerRemaining

    toHome = 0
    toLocker = 0
    dailyPackets = random.randrange(10,51)  # Number of packets to be delivered to a Locker

    for i in range(0,dailyPackets):
        destDelivery = random.randrange(1,3)    # 50/50 on packet destination
        if destDelivery == 1:   # Packet is to be delivered home
            toHome += 1
        elif destDelivery == 2: # Packet stays in locker
            toLocker += 1
    
    homeRemaining += toHome
    lockerRemaining += toLocker

def DailyResults(days):
    global dailyPackets, dailyCostOC, dailyCostPF
    global toHome, toLocker, dailyOC, dailyPF
    global homeRemaining, lockerRemaining
    global dailyHome, dailyLocker
    global deliveryPF, deliveryOC, deliveryLocker
    global accDeliveryPF, accDeliveryOC, accDeliveryLocker
    global costsPF, costsOC, costsAcc
    global toHomeStatus, toLockerStatus
    global maxLockerItems, maxItemsDay

    if days == 1:
        dailyHome.append(toHome)
        dailyLocker.append(toLocker)

        deliveryPF.append(0)
        deliveryOC.append(0)
        deliveryLocker.append(0)

        accDeliveryPF.append(0)
        accDeliveryOC.append(0)
        accDeliveryLocker.append(0)
        
        costsPF.append(0)
        costsOC.append(0)
        costsAcc.append(0)
        
        toHomeStatus.append(toHome)
        toLockerStatus.append(toLocker)
    
    else:
        dailyHome.append(toHome)
        dailyLocker.append(toLocker)

        deliveryPF.append(dailyPF)
        deliveryOC.append(dailyOC)
        deliveryLocker.append(dailyPickUp)

        accDeliveryPF.append(dailyPF + accDeliveryPF[-1])
        accDeliveryOC.append(dailyOC + accDeliveryOC[-1])
        accDeliveryLocker.append(dailyPickUp + accDeliveryLocker[-1])
        
        costsPF.append(dailyCostPF)
        costsOC.append(round(dailyCostOC,1))
        costsAcc.append(round(dailyCostPF + dailyCostOC + costsAcc[-1],1))
        
        toHomeStatus.append(homeRemaining)
        toLockerStatus.append(lockerRemaining)
    
    if homeRemaining + lockerRemaining > maxLockerItems:
        maxLockerItems = homeRemaining + lockerRemaining
        maxItemsDay = days

def PrintResults(compensation):
    global dailyHome, dailyLocker
    global deliveryPF, deliveryOC, deliveryLocker
    global accDeliveryPF, accDeliveryOC, accDeliveryLocker
    global costsPF, costsOC, costsAcc
    global toHomeStatus, toLockerStatus
    global totalCost, maxItems
    global maxLockerItems, maxItemsDay
    print("+-------+-----------------+----------------------+----------------------------+-----------------------------+-----------------+")
    print("|  DAY  |   NEW PACKAGES  |      DELIVERIES      |   ACCUMULATED DELIVERIES   |            COSTS            |  LOCKER STATUS  |")
    
    t = PrettyTable()
    #DAY
    t.add_column('  t  ', range(1,121))
    #NEW PACKAGES
    t.add_column(' Home ', dailyHome)
    t.add_column('Locker', dailyLocker)
    #DELIVERIES
    t.add_column(' PF ', deliveryPF)
    t.add_column(' OC ', deliveryOC)
    t.add_column('Locker', deliveryLocker)
    #ACC DELIVERIES
    t.add_column('  PF  ', accDeliveryPF)
    t.add_column('  OC  ', accDeliveryOC)
    t.add_column(' Locker ', accDeliveryLocker)
    #COSTS
    t.add_column('  PF  ', costsPF)
    t.add_column('  OC  ', costsOC)
    t.add_column('   Acc   ', costsAcc)
    #LOCKER STATUS
    t.add_column(' Home ', toHomeStatus)
    t.add_column('Locker', toLockerStatus)

    #TOTAL COST FOR ONE OBSERVATION
    totalCost.append(costsAcc[-1])

    #MAX ITEMS FOR ONE OBSERVATION
    maxItems.append(maxLockerItems)

    print(t)
    print("> Compensation:", compensation, "€")
    print("> Total Cost:", costsAcc[-1], "€")
    print("> Max Items:", maxLockerItems, "@ Day", maxItemsDay)

    #EMPTY ARRAYS
    dailyHome = []
    dailyLocker = []
    deliveryPF = []
    deliveryOC = []
    deliveryLocker = []
    accDeliveryPF = []
    accDeliveryOC = []
    accDeliveryLocker = []
    costsPF = []
    costsOC = []
    costsAcc = []
    toHomeStatus = []
    toLockerStatus = []

def ConfidenceInterval(compensation, alpha):
    global totalCost, maxItems
    
    #TOTAL COST
    n = len(totalCost)
    costM = float(sum(totalCost)) / n
    var = sum([(x - costM)**2 for x in totalCost]) / float(n - 1)
    fact = scipy.stats.t._ppf(1 - alpha / 2., n - 1)
    h1 = fact * math.sqrt(var / n)

    #MAX ITEMS
    n = len(totalCost)
    itemM = float(sum(maxItems)) / n
    var = sum([(x - itemM)**2 for x in maxItems]) / float(n - 1)
    fact = scipy.stats.t._ppf(1 - alpha / 2., n - 1)
    h2 = fact * math.sqrt(var / n)

    print("\n")
    print("FINAL RESULTS:")
    print("> Compensation:", compensation, "€")
    print("> Expected Total Cost: (", costM - h1, ",", costM + h1, ")")
    print("> Expected Maximum Number of Items in Locker: (", itemM - h2, ",", itemM + h2, ")")

main()