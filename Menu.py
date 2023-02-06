import serial, time, csv, os
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import glob

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
            x = []
            y = []
            with open(file_path,"r", newline='') as csvfile:
                reader = csv.reader(csvfile,delimiter=';')
                next(reader)
                for row in reader:
                    x.append(horizontal)
                    y.append(int(row[0]))
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

        horizontal = input("Insert horitzontal distance: ")
        list = os.listdir()
        csvfiles = []
        verticales = []
        medias = []

        for file in list:
            if file.endswith('.csv'):
                parts = file.split('_')
                if parts[1] == horizontal:
                    csvfiles.append(file)
                    if parts[2] not in verticales:
                        verticales.append(parts[2])
        rssimedia = []
        rssivarianza = []
        snrmedia = []
        snrvarianza = []
        x = []

        for i in verticales:
            rssinums = []
            snrnums = []
            for file in csvfiles:
                partes = file.split('_')
                if partes[2] == i:
                    with open(file,"r") as csvfile:
                        reader = csv.reader(csvfile,delimiter=';')
                        next(reader)
                        for row in reader:
                            rssinums.append(int(row[0]))
                            snrnums.append(int(row[1]))
            rssimedia.append(np.mean(rssinums))
            snrmedia.append(np.mean(snrnums))
            x.append(horizontal)
        plt.plot(x,rssimedia,"o")
        plt.plot(x,snrmedia,"*")
        plt.show()
    elif choice == '6':
        path = os.getcwd()
        csv_files = glob.glob(os.path.join(path, "*.csv"))

        dic=dict()


        for e in csv_files:
            nombre=e.split("\\")
            docu=nombre[-1]
            Vertical=docu.split("_")[-2]
            Horitzonal=docu.split("_")[-3]
            if Vertical not in dic:
                dic[Vertical]=dict()
                dic[Vertical][Horitzonal]=[docu]    
            else:
                if Horitzonal not in dic[Vertical]:
                    dic[Vertical][Horitzonal]=[docu]
                else:
                    dic[Vertical][Horitzonal].append(docu)
                
        dicDatRSSI=dict()
        dicDatSNR=dict()
        DatosRSSI=[]
        DatosSNR=[]
        for e in dic:
            l1=[]
            l11=[]
            l2=[]
            l22=[]
            for i in dic[e]:
                vacio=pd.DataFrame()
                for j in dic[e][i]:
                    arch=pd.read_csv(j,sep=';',engine='python')
                    vacio=pd.concat([vacio,arch])
                DatosRSSI.append([vacio['RSSI'].mean(),i,e])
                DatosSNR.append([vacio['SNR'].mean(),i,e])
                #l1.append([vacio['RSSI'].mean(),i,e])
                #l11.append((e,i))
                #l2.append([vacio['SNR'].mean(),i,e])
                #l22.append((e,i))
            #DatosRSSI.append(l1)
            #DatosSNR.append(l2)
                

        RSSI = pd.DataFrame(DatosRSSI)
        SNR = pd.DataFrame(DatosSNR)
        RSSI[1] = RSSI[1].astype('float64')
        SNR[1] = SNR[1].astype('float64')

        RSSI.rename(columns={0:'RSSI',
                                1:'Eje Horizontal',2:'Eje Vertical'},
                    inplace=True)
        SNR.rename(columns={0:'SNR',
                                1:'Eje Horizontal',2:'Eje Vertical'},
                    inplace=True)
        RSSI = RSSI.sort_values('Eje Horizontal')
        SNR = SNR.sort_values('Eje Horizontal')

        for value in RSSI['Eje Vertical'].unique():
            temp_df = RSSI[RSSI['Eje Vertical'] == value]
            plt.plot(temp_df['Eje Horizontal'], temp_df['RSSI'])

        plt.show()

    else:
        print("Invalid choice. Please try again.")


