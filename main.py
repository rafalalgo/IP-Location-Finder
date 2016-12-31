#!/usr/bin/python
import subprocess
import os

vpn = []
vpn.append("bombay")
vpn.append("california")
vpn.append("frankfurt")
vpn.append("saopaulo")
vpn.append("sydney")
vpn.append("tokyo")
vpn.append("virginia")

get_bin = lambda x, n: format(x, 'b').zfill(n)

data01 = open("data01.in", "r")
data02 = open("data02.in", "r")
data03 = open("data03.in", "r")

AS_COUNTRY = {}
IP_AS = {}
COUNTRY_CODE = {}

for line in data01:
    line = line.replace('\n', '').split('%')
    COUNTRY_CODE[line[0]] = line[1]

for line in data02:
    line = line.replace('\n', '').split('%')
    AS_COUNTRY[line[0]] = (line[1], line[2], line[3])

for line in data03:
    line = line.replace('\n', '').split('%')
    IP_AS[line[0]] = (line[1], line[2], line[3], line[4], line[5])

data01.close()
data02.close()
data03.close()

def check(ip):
    val = ip
    ip = ip.split('.')
    temp = ""
    for item in ip:
        temp += get_bin(int(item), 8)
    for key, value in IP_AS.iteritems():
        ip_bin = value[2]
        mask = int(value[4])
        ip_bin = ip_bin[0:mask]
        akt = temp[0:mask]
        if ip_bin == akt:
            return key
    return val

while 1:
    print("\n********************************************************\n")
    ip_test = raw_input("Podaj IP: ")
    test = subprocess.call(["whois", ip_test], stdout=open('whois.out','w'))
    filter_country = subprocess.call(["grep", "country", "whois.out"],stdout=open('./temp/country.out', 'w'))
    filter_country = subprocess.call(["grep", "Country", "whois.out"],stdout=open('./temp/Country.out', 'w'))
    filter_adres = subprocess.call(["grep", "address", "whois.out"], stdout=open('./temp/address.out', 'w'))
    filter_adres = subprocess.call(["grep", "Address", "whois.out"], stdout=open('./temp/Address.out', 'w'))
    filter_as = subprocess.call(["grep", "origin", "whois.out"], stdout=open('./temp/as.out', 'w'))
    filter_as = subprocess.call(["grep", "Origin", "whois.out"], stdout=open('./temp/AS.out', 'w'))
    filter_organization = subprocess.call(["grep", "org-name", "whois.out"], stdout=open('./temp/org.out', 'w'))
    filter_organization = subprocess.call(["grep", "Org-name", "whois.out"], stdout=open('./temp/Org.out', 'w'))
    in_ip = ip_test
    ip_test = check(ip_test)

    shift = " " * len("         Adres organizacji: ")

    print("\nNa podstawie plikow data-raw-table i data-used-autnums:\n")
    if ip_test in IP_AS:
        AS = IP_AS[ip_test][1]
        MASKA = IP_AS[ip_test][0]
    else:
        AS = "nieustalono"
        MASKA = "nieustalono"
    
    if ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][0] in COUNTRY_CODE:
        KRAJ = COUNTRY_CODE[AS_COUNTRY[IP_AS[ip_test][1]][0]]
    else:
        KRAJ = "nieustalono"

    if ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][1] != None and AS_COUNTRY[IP_AS[ip_test][1]][2] != None:
        ADDITIONAL = AS_COUNTRY[IP_AS[ip_test][1]][1] + " " + AS_COUNTRY[IP_AS[ip_test][1]][2]
    elif ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][1] != None:
        ADDITIONAL = AS_COUNTRY[IP_AS[ip_test][1]][1]
    elif ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][2] != None:
        ADDITIONAL = AS_COUNTRY[IP_AS[ip_test][1]][2]
    else:
        ADDITIONAL = "brak"

    print("     AS: " + " " * (len(shift) - len("     AS: ")) + AS)
    print("     Maska: " + " " * (len(shift) - len("     Maska: ")) + MASKA)
    print("     Kraj: " + " " * (len(shift) - len("     Kraj: ")) + KRAJ)
    if ADDITIONAL[0] != " ":
        print("     Dodatkowe informacje: " + " " * (len(shift) - len("     Dodatkowe informacje: ")) + ADDITIONAL)
    else:
        print("     Dodatkowe informacje: " + " " * (len(shift) - len("     Dodatkowe informacje: ")) + ADDITIONAL[1:])
    
    print("\nNa podstawie wynikow otrzymanych z whois: \n")
    AS = ""
    MASKA = ""
    KRAJ = ""
    ADDITIONAL = ""

    if os.stat("./temp/country.out").st_size != 0:
        open_plik = open("./temp/country.out", "r")
        for line in open_plik:
            KRAJ = COUNTRY_CODE[line[(len("country:        ")):-1]]
        open_plik.close()
    if os.stat("./temp/Country.out").st_size != 0:
        open_plik = open("./temp/Country.out", "r")
        for line in open_plik:
            KRAJ = COUNTRY_CODE[line[(len("Country:        ")):-1]]
        open_plik.close()

    if os.stat("./temp/as.out").st_size != 0:
        open_plik = open("./temp/as.out", "r")
        for line in open_plik:
            AS += line[(len("country:        ")):-1][2:]
            AS += " "
        open_plik.close()
    if os.stat("./temp/AS.out").st_size != 0:
        open_plik = open("./temp/AS.out", "r")
        for line in open_plik:
            AS += line[(len("country:        ")):-1][2:]
            AS += " "
        open_plik.close()

    print("     AS: " + " " * (len(shift) - len("     AS: ")) + AS)
    print("     Kraj: " + " " * (len(shift) - len("     Kraj: ")) + KRAJ)
    print("     Dodatkowe informacje: " + " " * (len(shift) - len("     Dodatkowe informacje: ")) + ADDITIONAL)
    
    if os.stat("./temp/org.out").st_size != 0:
        print("         Organizacja: ")
        open_plik = open("./temp/org.out", "r")
        for line in open_plik:
            print(shift + line[(len("country:        ")):-1])
        open_plik.close()

    if os.stat("./temp/Org.out").st_size != 0:
        print("     Organizacja: ")
        open_plik = open("./temp/Org.out", "r")
        for line in open_plik:
            print(shift + line[(len("country:        ")):-1])
        open_plik.close()


    if os.stat("./temp/address.out").st_size != 0:
        print("         Adres organizacji: ")
        open_plik = open("./temp/address.out", "r")
        k = 0
        for line in open_plik:
            if k < 4:
                print(shift + line[(len("country:        ")):-1])
            k += 1
        open_plik.close()

    if os.stat("./temp/Address.out").st_size != 0:
        print("         Adres organizacji: ")
        open_plik = open("./temp/Address.out", "r")
        k = 0
        for line in open_plik:
            if k < 4:
                print(shift + line[(len("country:        ")):-1])
            k += 1
        open_plik.close()


    print("\nNa podstawie wynikow otrzymanych z pingow i pomiarow na mapie swiata: \n")
    AS = ""
    MASKA = ""
    KRAJ = ""
    ADDITIONAL = ""

    for item in vpn:
        print("Trwa nawiazywanie polaczenia vpn poprzez: " + item)
        test = subprocess.call(["./getPingTime.sh", item, in_ip, "./vpn/"+item])
        connnect = open("./vpn/" + item)
        counter = 0
        suma = 0
        ile = 0
        for line in connnect:
            counter += 1
            if 3 >= counter >= 2:
                temp = line[:-1]
                pos = len(temp) - 4;
                while pos >= 0 and temp[pos] != ' ': 
                    pos -= 1
                temp = temp[(pos + 6):-3]
                try:
                    suma += float(temp)
                    ile += 1
                except ValueError:
                    pass
        if ile != 0:
            print("Sredni czas pingu wynosi: " + str(suma / ile) + "ms.")
        else:
            print("Cos poszlo nie tak.")
