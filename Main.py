# Cade Fisher
#Student ID: 011020270
# C950 Task 2
# 08/13/2024

#Imports
import csv
import datetime
from cmath import inf


# Hashtable class, initializes changing hashtable
class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
    # Defines the insert function that inserts items into hashtable
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
    # Function for searching for items in hashtable
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None
    # Function to remove items in hashtable
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

# Package class, initializes the package object
class Package:
    def __init__(self, Id, address, city, state, zip, deadLine, weight, status):
        self.Id = Id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadLine = deadLine
        self.weight = weight
        self.status = status
        self.deliveryTime = None
        self.leaveHub = None
    # Defines a string representation of object
    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s" % (self.Id, self.address, self.city, self.state, self.zip, self.deadLine, self.weight, self.status)

    # Function that updates the status of the packages based on the time the user selects.
    def updateStatus(self, convertTime):
        # Initialize the truck variable to denote which truck is used
        tru = 0
        # Packages with these IDs leave at the time with specific truck
        if self.Id in {2,3,9,18,36,38,39,7,8,10,11,12,23,24}:
            self.leaveHub = datetime.timedelta(hours=11, minutes=0, seconds=0)
            tru = 2
        if self.Id in {13,1,14,19,16,15,20,40,29,30,31,34,37,17}:
            self.leaveHub = datetime.timedelta(hours=8, minutes=0, seconds=0)
            tru = 1
        if self.Id in {4,5,6,28,32,33,21,22,35,27,25,26,24}:
            self.leaveHub = datetime.timedelta(hours=9, minutes=6, seconds=0)
            tru = 3
        # Special case for package ID 9 to handle different addresses based on the current time
        if self.Id == 9:
            if convertTime >= datetime.timedelta(hours=10, minutes=20, seconds=0):
                # After 10:20, the address and zip code change
                self.address = "410 S State St"
                self.zip = '84111'
            else:
                # Before 10:20, use the original address and zip code
                self.address = "300 State St"
                self.zip = "84103"
        # Update the package status based on the current time and delivery status
        if self.deliveryTime and self.deliveryTime <= convertTime:
            self.status = "Delivered: " + str(self.deliveryTime) + " by truck" + str(tru)
        elif self.leaveHub <= convertTime < self.deliveryTime:
            self.status = "En route on truck" + str(tru)
        elif self.leaveHub > convertTime:
            self.status = "AT HUB"

# Initializes the truck object
class Truck:
    def __init__(self, speed, capacity, packages, mileage, currentLocation, departureTime):

        self.speed = speed
        self.capacity = capacity
        self.packages = packages
        self.mileage = mileage
        self.currentLocation = currentLocation
        self.departureTime = departureTime

# Defines string for truck object
    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (
        self.speed, self.capacity, self.packages, self.mileage, self.currentLocation, self.departureTime)

# Creats myHash using the ChainingHashTable class
myHash = ChainingHashTable()

#Reads Distance csv
with open('Distances.csv') as csvfile:
    csvDistances = csv.reader(csvfile)
    csvDistances = list(csvDistances)

#Reads Address csv
with open('Addresses.csv', encoding='utf-8-sig') as csvfile1:
    csvAddress = csv.reader(csvfile1)
    csvAddress = list(csvAddress)

#Function that read package csv and loads the data to the variables
def loadPackageData(filename):
    with open(filename) as packageFile:
        packageData = csv.reader(packageFile, delimiter=',')
        next(packageData)
        for package in packageData:
            pId = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadLine = package[5]
            pWeight = package[6]
            pStatus = "AT HUB"

            # Creates a new Package object with the extracted data
            newPackage = Package(pId, pAddress, pCity, pState, pZip, pDeadLine, pWeight, pStatus)
            # Insert the new Package object into the hash table with the package ID as the key
            myHash.insert(pId, newPackage)


# Gets the distance between two addresses
def distanceBewteenAddresses(addressOne, addressTwo):
    distance = csvDistances[addressOne][addressTwo]
    if distance == '':
        distance = csvDistances[addressTwo][addressOne]
    return float(distance)

# Finds the ID associated with given address
def addressFinder(address):
    for row in csvAddress:
        if address in row[2]:
            return int(row[0])


# Calculates total mileage from all the trucks
def totalMileage(truckOne, truckTwo, truckThree):
    return truckOne.mileage + truckTwo.mileage + truckThree.mileage

# Executes the package delivery algorithm by using the nearest neighbor
def package_delivery_algo(truck):
    # Initialize the list of packages that have not yet been delivered and clears the truck package list
    notDelivered = [myHash.search(packageId) for packageId in truck.packages]
    for packageId in truck.packages:
        package = myHash.search(packageId)
        notDelivered.append(package)
        truck.packages.clear()
    # While there are still packages to deliver and tracks the shortest distance of the remaining packages
    while len(notDelivered) > 0:
        nextAddress = float(inf)
        nextPackage = None
        for package in notDelivered:
            if distanceBewteenAddresses(addressFinder(truck.currentLocation),
                                        addressFinder(package.address)) <= nextAddress:
                nextAddress = distanceBewteenAddresses(addressFinder(truck.currentLocation), addressFinder(package.address))
                nextPackage = package
        # Adds the next package's ID to the truck's package list
        truck.packages.append(nextPackage.Id)
        # Removes the delivered package from the list of not delivered packages
        notDelivered.remove(nextPackage)
        # Updates the truck's mileage by adding the distance traveled
        truck.mileage += nextAddress
        # Updates the truck's current location to the address of the delivered package
        truck.currentLocation = nextPackage.address
        # Calculates the travel time based on the distance and the truck's average speed
        travelTime = (nextAddress / 18) * 60
        travelTimeDelta = datetime.timedelta(minutes=travelTime)
        # Updates the truck's departure time to account for the travel time
        truck.departureTime += travelTimeDelta
        # Sets the delivery time of the delivered package to the truck's updated departure time
        nextPackage.deliveryTime = truck.departureTime

# Creates the instances of the truck class for each truck
truckOne = Truck(18, 16, [13,1,14,19,16,15,20,40,29,30,31,34,37], 0, '4001 South 700 East',datetime.timedelta(hours=8, minutes=0, seconds=0))

truckTwo = Truck(18, 16, [2,3,9,18,36,38,39,7,8,10,11,12,23,24,17], 0, '4001 South 700 East',
                 datetime.timedelta(hours=11, minutes=0, seconds=0))
truckThree = Truck(18, 16, [4,5,6,28,32,33,21,22,35,27,25,26],  0, '4001 South 700 East',
                   datetime.timedelta(hours=9, minutes=6, seconds=0))

# Loads the package.csv into hashtable
loadPackageData("Packages.csv")
# Executes the delivery algorithm for each truck
package_delivery_algo(truckOne)

package_delivery_algo(truckTwo)

package_delivery_algo(truckThree)
# Calculates the total mileage of all three trucks
total = totalMileage(truckOne, truckTwo, truckThree)

#User interface
print("Welcome to WGUPS!")
print("Type ALL to see all package Status and total Mileage")
print("Type P to see a single package status")
print("Type T to see all the packages a specific time")
print("Type Q to quit")


# Asks for user to select an option
while True:
    choice = input("Choose from above: ")
    if choice == 'ALL':
        # Display total mileage covered by all trucks
        print("Total Mileage: ", total)
        # Iterate over all package IDs and display their status
        for packageId in range(1, 41):
            # Searches hashtable using package Id
            package = myHash.search(packageId)
            # Determines which truck handled the package and displays package information
            if packageId in {2, 3, 9, 18, 36, 38, 39, 7, 8, 10, 11, 12, 23, 24}:
                print("Package", str(package.Id) + ": " + package.address, package.city, package.state,
                      str(package.zip), package.deadLine, package.weight,
                      "Delivered at", package.deliveryTime, "by Truck 2")

            elif packageId in {13, 1, 14, 19, 16, 15, 20, 40, 29, 30, 31, 34, 37, 17}:
                print("Package", str(package.Id) + ": " + package.address, package.city, package.state,
                      str(package.zip), package.deadLine, package.weight,
                      "Delivered at", package.deliveryTime, "by Truck 1")

            elif packageId in {4, 5, 6, 28, 32, 33, 21, 22, 35, 27, 25, 26, 24}:
                print("Package", str(package.Id) + ": " + package.address, package.city, package.state,
                      str(package.zip), package.deadLine, package.weight,
                      "Delivered at", package.deliveryTime, "by Truck 3")


    elif choice == 'P':
        # Gets the package ID from the user
        while True:
            userChoice = int(input("Type a package id: "))
            if 1 <= userChoice <= 40:
                break
            print("Invalid choice")
        # Gets the time from the user
        while True:
            userTime = input("Enter a time in the format HH:MM:SS: ")
            try:
                h, m, s = map(int, userTime.split(":"))
                convertTime = datetime.timedelta(hours=h, minutes=m, seconds=s)
                break
            except ValueError:
                print("Invalid time")
        # Retrieves the selected package and update its status
        package = myHash.search(userChoice)
        package.updateStatus(convertTime)
        # Displays package info
        print("Package", str(package.Id) + ": " + package.address, package.city, package.state,
              str(package.zip), package.deadLine, package.weight, package.status)


    elif choice == 'T':
        while True:
            # Gets the time from the user
            userTime = input("Enter a time in the format HH:MM:SS: ")
            try:
                h, m, s = map(int, userTime.split(":"))
                convertTime = datetime.timedelta(hours=h, minutes=m, seconds=s)
                break
            except ValueError:
                print("Invalid time")
        # Updates and displays package based on users time
        for packageId in range(1, 41):
            package = myHash.search(packageId)
            package.updateStatus(convertTime)
            print("Package", str(package.Id) + ": " + package.address, package.city, package.state,
                  str(package.zip), package.deadLine, package.weight, package.status)
    # Terminates the program
    elif choice == 'Q':
        break
    # Handler for invalid input
    else:
        print("Invalid choice")
