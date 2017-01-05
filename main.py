#!/usr/bin/python
import subprocess
import os
import sys
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from math import *

# 91.123.176.254

vpn = ["bombay", "california", "frankfurt", "sao-paulo", "sydney", "tokyo", "virginia"]

map_cordinate = {}

"""
try:
    geolocator = Nominatim()
    location = geolocator.geocode("ul. Olkuska 43, Suloszowa")
    HOME = (location.latitude, location.longitude)
except Exception:
    print("Nie udalo sie pobrac lokalizacji.")
"""

for item in vpn:
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(item)
        map_cordinate[item] = (location.latitude, location.longitude)
    except Exception:
        print("Nie udalo sie pobrac lokalizacji dla: " + item)

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

    test = subprocess.call(["whois", ip_test], stdout=open('whois.out', 'w'))
    filter_country = subprocess.call(["grep", "country", "whois.out"], stdout=open('./temp/country.out', 'w'))
    filter_country = subprocess.call(["grep", "Country", "whois.out"], stdout=open('./temp/Country.out', 'w'))
    filter_adres = subprocess.call(["grep", "address", "whois.out"], stdout=open('./temp/address.out', 'w'))
    filter_adres = subprocess.call(["grep", "Address", "whois.out"], stdout=open('./temp/Address.out', 'w'))
    filter_as = subprocess.call(["grep", "origin", "whois.out"], stdout=open('./temp/as.out', 'w'))
    filter_as = subprocess.call(["grep", "Origin", "whois.out"], stdout=open('./temp/AS.out', 'w'))
    filter_organization = subprocess.call(["grep", "org-name", "whois.out"], stdout=open('./temp/org.out', 'w'))
    filter_organization = subprocess.call(["grep", "Org-name", "whois.out"], stdout=open('./temp/Org.out', 'w'))
    filter_organization = subprocess.call(["grep", "orgname", "whois.out"], stdout=open('./temp/orgn.out', 'w'))
    filter_organization = subprocess.call(["grep", "OrgName", "whois.out"], stdout=open('./temp/OrgN.out', 'w'))
    in_ip = ip_test
    ip_test = check(ip_test)

    shift = " " * len("         Szerokosc geograficzna: ")

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

    if ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][1] is not None and AS_COUNTRY[IP_AS[ip_test][1]][2] is not None:
        ADDITIONAL = AS_COUNTRY[IP_AS[ip_test][1]][1] + " " + AS_COUNTRY[IP_AS[ip_test][1]][2]
    elif ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][1] is not None:
        ADDITIONAL = AS_COUNTRY[IP_AS[ip_test][1]][1]
    elif ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][2] is not None:
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

    try:
        geolocator = Nominatim()
        location = geolocator.geocode(KRAJ)

        if location is not None:
            print("         Szerokosc geograficzna: " + " " * (len(shift) - len("         Szerokosc geograficzna: ")) + "\n" + shift + str(round(location.latitude, 4)))
            print("         Dlugosc geograficzna: " + " " * (len(shift) - len("         Dlugosc geograficzna: ")) + "\n" + shift + str(round(location.longitude, 4)))
    except Exception:
        print("Nie udalo sie pobrac lokalizacji dla: " + KRAJ)

    print("\nNa podstawie wynikow otrzymanych z whois: \n")
    AS = ""
    MASKA = "niesustalono"
    KRAJ = "nieustalono"
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

    if AS == "":
        AS = "nieustalono"

    print("     AS: " + " " * (len(shift) - len("     AS: ")) + AS)
    print("     Kraj: " + " " * (len(shift) - len("     Kraj: ")) + KRAJ)
    print("     Dodatkowe informacje: " + " " * (len(shift) - len("     Dodatkowe informacje: ")) + ADDITIONAL)

    tekst = KRAJ

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

    if os.stat("./temp/orgn.out").st_size != 0:
        print("     Organizacja: ")
        open_plik = open("./temp/orgn.out", "r")
        for line in open_plik:
            print(shift + line[(len("country:        ")):-1])
        open_plik.close()

    if os.stat("./temp/OrgN.out").st_size != 0:
        print("     Organizacja: ")
        open_plik = open("./temp/OrgN.out", "r")
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
                if tekst == KRAJ:
                    tekst = line[(len("country:        ")):-1]
            k += 1
        open_plik.close()

    if os.stat("./temp/Address.out").st_size != 0:
        print("         Adres organizacji: ")
        open_plik = open("./temp/Address.out", "r")
        k = 0
        for line in open_plik:
            if k < 4:
                print(shift + line[(len("country:        ")):-1])
                if tekst == KRAJ:
                    tekst = line[(len("country:        ")):-1]
            k += 1
        open_plik.close()

    try:
        geolocator = Nominatim()
        location = geolocator.geocode(tekst)
        if location is not None:
            print("         Szerokosc geograficzna: " + " " * (len(shift) - len("         Szerokosc geograficzna: ")) + "\n" + shift + str(round(location.latitude, 4)))
            print("         Dlugosc geograficzna: " + " " * (len(shift) - len("         Dlugosc geograficzna: ")) + "\n" + shift + str(round(location.longitude, 4)))
        else:
            location = geolocator.geocode(KRAJ)
            if location is not None:
                print("         Szerokosc geograficzna: " + " " * (len(shift) - len("         Szerokosc geograficzna: ")) + "\n" + shift + str(round(location.latitude, 4)))
                print("         Dlugosc geograficzna: " + " " * (len(shift) - len("         Dlugosc geograficzna: ")) + "\n" + shift + str(round(location.longitude, 4)))
    except Exception:
        print("Nie udalo sie pobrac lokalizacji dla: " + tekst)

    print("\nNa podstawie wynikow otrzymanych z pingow i pomiarow na mapie swiata: \n")
    AS = ""
    MASKA = ""
    KRAJ = ""
    ADDITIONAL = ""

    pary = {}
    odleglosc = {}
    waga = {}

    """
    SUMA = 0
    C = 0
    """

    SREDNIA_PREDKOSC = float(20165129.2815)

    for item in vpn:
        if item in map_cordinate:
            print("Trwa nawiazywanie polaczenia vpn poprzez: " + item)
            test = subprocess.call(["./getPingTime.sh", item, in_ip, "./vpn/" + item])
            """
            print(item + " " + str(round(map_cordinate[item][0], 4)) + " " + str(round(map_cordinate[item][1], 4)))
            print(str(HOME[0]) + " " + str(HOME[1]))
            print("ODLEGLOSC: " + str(round(great_circle(HOME, map_cordinate[item]).m, 3)))
            """
            connnect = open("./vpn/" + item)
            counter = 0
            suma = 0
            ile = 0
            for line in connnect:
                counter += 1
                if 5 >= counter >= 2:
                    temp = line[:-1]
                    pos = len(temp) - 4
                    while pos >= 0 and temp[pos] != ' ':
                        pos -= 1
                    temp = temp[(pos + 6):-3]
                    try:
                        suma += float(temp)
                        ile += 1
                    except ValueError:
                        pass
            if ile != 0:
                print("Sredni czas pingu wynosi: " + str(round(suma / ile, 3)) + " ms.")
                pary[item] = str(suma / ile)
                """
                SUMA +=  great_circle(HOME, map_cordinate[item]).m / (suma / (ile * 1000))
                C += 1
                """
                DROGA_W_LINI_PROSTEJ = SREDNIA_PREDKOSC * (suma / (ile * 1000))
                odleglosc[item] = DROGA_W_LINI_PROSTEJ
            else:
                print("Cos poszlo nie tak.")
    # print(str(SUMA / C))

    print("\nPrzypuszczalne odleglosci szukanego punktu od podanych miast w metrach: \n")

    for key in sorted(odleglosc, key=odleglosc.get):
        print("         " + key + " " * (20 - len(key)) + str(round(odleglosc[key], 3)))
        waga[key] = odleglosc[key]
    print("\n")

    for key, value in waga.iteritems():
        waga[key] = float(1 / value)

    suma = sum(waga.values())
    # print(suma)

    for key, value in map_cordinate.iteritems():
        # print(key)
        # print(str(value[0]) + " " + str(value[0] * pi / 180))
        # print(str(value[1]) + " " + str(value[1] * pi / 180))
        map_cordinate[key] = (value[0] * pi / 180, value[1] * pi / 180)

    zmienne = {}

    for key, value in map_cordinate.iteritems():
        # print(key)
        x = cos(map_cordinate[key][0]) * cos(map_cordinate[key][1])
        y = cos(map_cordinate[key][0]) * sin(map_cordinate[key][1])
        z = sin(map_cordinate[key][0])
        # print(x, y, z)
        zmienne[key] = (x, y, z)

    X = 0
    Y = 0
    Z = 0

    for key, value in zmienne.iteritems():
        X += zmienne[key][0] * waga[key]
        Y += zmienne[key][1] * waga[key]
        Z += zmienne[key][2] * waga[key]

    X = X / suma
    Y = Y / suma
    Z = Z / suma

    # print(X, Y, Z)

    Lon = atan2(Y, X)
    Hyp = sqrt(X * X + Y * Y)
    Lat = atan2(Z, Hyp)

    lat = Lat * 180 / pi
    lon = Lon * 180 / pi

    print("Najprawdopodobniej szukany punkt to: ")
    print("         Szerokosc geograficzna: " + " " * (len(shift) - len("         Szerokosc geograficzna: ")) + "\n" + shift + str(round(lat, 4)))
    print("         Dlugosc geograficzna: " + " " * (len(shift) - len("         Dlugosc geograficzna: ")) + "\n" + shift + str(round(lon, 4)))

    try:
        geolocator = Nominatim()
        location = geolocator.reverse(str(lat) + ", " + str(lon))
        print("         Miejsce:\n" + shift + location.address)
    except Exception:
        print("Nie udalo sie pobrac adresu dla punktu o wspolrzednych: (" + str(round(lat, 4)) + ", " + str(
            round(lon, 4)) + ")")