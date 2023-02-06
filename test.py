import serial, time, csv, os
import matplotlib.pyplot as plt
import numpy as np
import math

def menu():
    print("Menu:")
    print("1. Test connection")
    print("2. Data from 1000 packets")
    print("3. Deleting a data file")
    print("4. Generate a graphic from a data file")
    print("5. Generate a graphic with all data in X distance")
    print("6. Generate a graphic from all the data files")

    choice = input("Enter your choice (1-6): ")
    return choice

def convert(bytevalue):
    data = bytevalue.decode('utf-8')
    data = data[0:][:-2]
    return data

def checkfirstline(line):
    if line[2] == 93:
        return True


# Inicialitzar Port
port = serial.Serial('COM6', 9600)
port.reset_input_buffer
port.reset_output_buffer


print("Starting device")
time.sleep(2)

while True:
    choice = menu()
    if choice == '1':
        print("1. Testing connection")
        begin = "CHECK"
        port.write(begin.encode()) #Write CHECK on PORT6 (Program in Arduino will detect)
        time.sleep(2)
        data = port.readline()
        if checkfirstline(data):
            port.write(begin.encode())
            t = port.readline()
            print("\n")
            print(convert(t))
            print("\n")
        else:
            print("\n")
            print(convert(data))
            print("\n")
    elif choice == '2':
        print("2. Getting Data from 1000 packets")

        horizontal = input("Ingrese distancia horizontal: ")
        vertical = input("Ingrese distancia vertical: ")
        muestra = input("Ingrese numero de muestra: ")

        nom = "data" + "_" + horizontal + "_" + vertical + "_" + muestra + ".csv"
        begin = "BEGIN"
        port.write(begin.encode())
        with open(nom, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["RSSI;SNR"])
            i= 0
            while i < 100:
                i += 1
                data = port.readline()
                if checkfirstline(data):
                    continue
                writer.writerow([convert(data)])
                print(convert(data))
    elif choice == '3':
        # Prompt the user to select a file to delete
        horizontal = input("Ingrese distancia horizontal: ")
        vertical = input("Ingrese distancia vertical: ")
        muestra = input("Ingrese numero de muestra: ")
        delete_file = "data" +"_" + horizontal + "_" + vertical + "_" + muestra + ".csv"

        if os.path.exists(delete_file):
            confirmation = input(f"Are you sure you want to delete {delete_file}? (y/n)")
            if confirmation.lower() == 'y':
                os.remove(delete_file)
                print(f"{delete_file} has been deleted.")
            else:
                print("Deletion cancelled.")
        else:
            print("File does not exist")
    elif choice == '4':

        horizontal = input("Ingrese distancia horizontal: ")
        vertical = input("Ingrese distancia vertical: ")
        muestra = input("Ingrese numero de muestra: ")
        file_path = "data" + "_" + horizontal + "_" + vertical + "_" + muestra + ".csv"

        if os.path.exists(file_path):
            # Lists to store the data
            x = []
            y = []
            # Open the file and read the data
            with open(file_path,"r", newline='') as csvfile:
                # Create a CSV reader object
                reader = csv.reader(csvfile,delimiter=';')
                # Skip the header row
                next(reader)
                    # Extract the data from the file
                for row in reader:
                    x.append(horizontal)
                    y.append(int(row[0]))
                # Create the graph
            mean = np.mean(y)
            var = np.var(y)
            plt.plot(x, y,"o")
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Graph of X vs Y')
            plt.annotate(f'media = {mean:.2f}', xy=(1, 0), xycoords='axes fraction',
                    xytext=(-20, 20), textcoords='offset points',
                    ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.7))
            plt.annotate(f'var = {var:.2f}', xy=(1, 0), xycoords='axes fraction',
                    xytext=(-20, 40), textcoords='offset points',
                    ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.7))
            plt.show()
        else:
            print("File does not exist")            
    elif choice == '5':
        horizontal = input("Ingrese distancia horizontal: ")

        list = os.listdir()
        csvfiles = []
        nums = []
        medias = []

        for file in list:
            if file.endswith('.csv'):
                parts = file.split('_')
                if parts[1] == horizontal:
                    csvfiles.append(file)
                    if parts[2] not in nums:
                        nums.append(parts[2])
        rssimedia = []
        rssivarianza = []
        snrmedia = []
        snrvarianza = []
        lineax = []
        for num in nums:
            rssinums = []
            snrnums = []
            for file in csvfiles:
                partes = file.split('_')
                if partes[2] == num:
                    with open(file,"r") as csvfile:
                        reader = csv.reader(csvfile,delimiter=';')
                        next(reader)
                        for row in reader:
                            rssinums.append(int(row[0]))
                            snrnums.append(int(row[1]))
            rssimedia.append(np.mean(rssinums))
            snrmedia.append(np.mean(snrnums))
            lineax.append(horizontal)
        plt.plot(lineax,rssimedia,"o")
        plt.plot(lineax,snrmedia,"*")
        plt.show()
    elif choice == '6':
        list = os.listdir()
        csvfiles = []
        nums = []
        medias = []
        numeros = []
        for file in list:
            if file.endswith('.csv'):
                parts = file.split('_')
                csvfiles.append(file)
                if parts[2] not in nums:
                    nums.append(parts[2])
                if parts[1] not in numeros:
                    numeros.append(parts[1])
        rssimedia = []
        rssivarianza = []
        snrmedia = []
        snrvarianza = []
        lineax = []
        numeros = [int(numero) for numero in numeros]
        numeros = sorted(numeros)
        print(numeros)
        numeros = [str(numero) for numero in numeros]
        print(numeros)
        print(nums)
        for numero in numeros:
            for num in nums:
                rssinums = []
                snrnums = []
                for file in csvfiles:
                    partes = file.split('_')
                    if partes[1] == numero and partes[2] == num:
                        with open(file,"r") as csvfile:
                            reader = csv.reader(csvfile,delimiter=';')
                            next(reader)
                            for row in reader:
                                rssinums.append(int(row[0]))
                                snrnums.append(int(row[1])) 
                if rssinums and snrnums:
                    rssimedia.append(np.mean(rssinums))
                    snrmedia.append(np.mean(snrnums))
                    lineax.append(numero)
        print(rssimedia)
        print(snrmedia)
        print(lineax)

        lineax = [int(numero) for numero in lineax]
        rssimedia = [int(n) for n in rssimedia]
        for i, j in zip(lineax, rssimedia):
            plt.text(i, j, f'{j}')
        plt.plot(lineax,snrmedia,"o")
    
        plt.show()
    else:
        print("Invalid choice. Please try again.")


