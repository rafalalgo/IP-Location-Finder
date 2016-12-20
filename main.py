#!/usr/bin/python

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
    IP_AS[line[0]] = (line[1], line[2], line[3], line[4])

data01.close()
data02.close()
data03.close()

while 1:
    print("\n#####################################################\n")
    ip_test = raw_input("Podaj IP: ")

    print("")
    if ip_test in IP_AS:
        print("Numer AS: " + IP_AS[ip_test][1])
    else:
        print("Numer AS: nieustalono")
    if ip_test in IP_AS:
        print("Maska podsieci: " + IP_AS[ip_test][0])
    else:
        print("Maska podsieci: nieustalono")
    if ip_test in IP_AS and IP_AS[ip_test][1] in AS_COUNTRY and AS_COUNTRY[IP_AS[ip_test][1]][0] in COUNTRY_CODE:
        print("Kraj przypisany do AS: " + COUNTRY_CODE[AS_COUNTRY[IP_AS[ip_test][1]][0]])
    else:
        print("Kraj przypisany do AS: nieustalono")
