#!/usr/bin/python

get_bin = lambda x, n: format(x, 'b').zfill(n)

as_and_kraj = open("./data/data01.txt", "r")
ip_and_as = open("./data/data02.txt", "r")
kraj_and_kod = open("./data/data03.txt", "r")

as_kraj = {}
ip_as = {}
kraj_kod = {'': ''}

for line in kraj_and_kod:
    line = line.replace('\n', '').split(',')
    kraj = str(line[0])
    kod = str(line[1])
    kraj_kod[kod] = kraj

for line in as_and_kraj:
    is_kraj = 0
    if line[-5] == ',':
        is_kraj = 1
    line = ' '.join(line.split()).replace('\n', '').split(' ')
    nr_as = line[0]
    if is_kraj == 1:
        kraj = str(line[len(line) - 1])
        info = ""
        for item in range(1, len(line) - 1):
            info += line[item]
            if item != len(line) - 2:
                info += " "
        kraj = kraj.replace(' ', '')
        info = info.replace(',', '')
    else:
        kraj = ""
        info = ""
        for item in range(1, len(line)):
            info += line[item]
            if item != len(line) - 1:
                info += " "
        kraj = kraj.replace(' ', '')
        info = info.replace(',', '')
    if '-' in info:
        info = info.split(" -")
        add = info[0].replace(',', ' ')
        if len(info) >= 2:
            place = info[1].replace(',', ' ')
        else:
            place = " "
        if len(place) > 0 and place[0] == ' ':
            place = place[1:]
        if len(add) > 0 and add[0] == ' ':
            add = add[1:]
        info = place
    else:
        if len(info) > 0 and info[0] == ' ':
            info - info[1:]
        add = ""
    as_kraj[nr_as] = (kraj, info, add)

for line in ip_and_as:
    line = ' '.join(line.split()).split(' ')
    ip = line[0]
    nr_as = line[1]
    pack = ip.split('/')
    nr_ip = pack[0]
    num = int(pack[1])
    mask = int(pack[1])
    count = 32 - mask
    part = mask / 8
    res = mask - 8 * part;
    mask = ("1" * 8 + ".") * part + "1" * res + "0" * (8 - res) + "." + ("0" * 8 + ".") * (3 - part)
    mask_bin = mask[0:-1]
    nr_ip_bin  = nr_ip.split('.')
    ip_bin = str(get_bin(int(nr_ip_bin[0]), 8))
    ip_bin += str(get_bin(int(nr_ip_bin[1]), 8))
    ip_bin += str(get_bin(int(nr_ip_bin[2]), 8))
    ip_bin += str(get_bin(int(nr_ip_bin[3]), 8))
    mask = mask.split('.')
    asn = []
    for item in mask:
        if item != '':
            if '1' in item:
                asn.append(str(int(item, 2)))
            else:
                asn.append("0")
    asn = '.'.join(asn)
    ip_as[nr_ip] = (asn, nr_as, ip_bin, mask_bin, str(32 - count))

KRAJ_KOD = open("data01.in", 'w')
for key, value in kraj_kod.iteritems():
    KRAJ_KOD.write(key + "%" + value + "\n")
KRAJ_KOD.close()

AS_KRAJ = open("data02.in", "w")
for key, value in as_kraj.iteritems():
    AS_KRAJ.write(key + "%" + value[0] + "%" + value[1] + "%" + value[2] + "\n")
AS_KRAJ.close()

IP_AS = open("data03.in", "w")
for key, value in ip_as.iteritems():
    IP_AS.write(key + "%" + value[0] + "%" + value[1] + "%" + value[2] + "%" + value[3] + "%" + value[4] + "\n")
IP_AS.close()

as_and_kraj.close()
ip_and_as.close()
kraj_and_kod.close()
