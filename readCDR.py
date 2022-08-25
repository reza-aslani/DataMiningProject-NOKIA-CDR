
# تابع کمکی خواندن بایت


def readByte(ff):
    res = hex(ord(ff.read(1))).replace('0x', '')
    if(len(res) == 1):
        res = '0'+res
    return res

# def iToHex(i):
#     return int(str(i),16)

# تبدیل هگز به عدد


def hexToi(c):
    return int(c, 16)

# دریافت شماره


def getPhoneNumber(arr, offset, l):
    res = ''
    for i in range(offset, offset+l):
        # sp=hex(arr[offset+i]).replace('0x','')
        # if(len(sp)==1):
        #     res+=sp+'0'
        # else:
        #     res+=sp[1]+sp[0]
        sp = arr[i]
        res += sp[1]+sp[0]

    res = res.replace('f', '')
    if res.startswith('98'):
        res = res[2:]

    # for i in range(0,10-len(res)):
    #     res+=' '

    return res

# عددهای BCD


def getBCD(arr, offset, l):
    res = ''
    for i in range(offset, offset+l):
        # sp=hex(arr[offset+i]).replace('0x','')
        res = arr[i]+res

    try:
        n = res.replace('f', '0')
        return int(n, 10)
    except:
        return 0

# خواندن فایل CDR


def readFile(fileName, out): #, g):
    with open(fileName, 'rb') as f:
        # off=f.tell()
        n0c = readByte(f)
        n0 = hexToi(n0c)
        ind = 1

        while n0:
            rec = []
            rec.append(n0c)

            c = readByte(f)
            rec.append(c)

            n1 = hexToi(c)

            # تصحیح اعداد FF
            if(n1 == 255):
                n0 = n1
                while n0 and n0 == 255:
                    rec = []
                    n0c = readByte(f)
                    rec.append(n0c)
                    n0 = hexToi(n0c)
            else:
                # استخراج طول رکورد
                l = n0+n1*256
                if(l > 2):
                    for i in range(l-2):
                        # rec.append(ord(f.read(1)))
                        c = readByte(f)
                        rec.append(c)

                    typ = hexToi(rec[2])
                    isOK = False
                    calling = ''
                    called = ''
                    dur = ''

                    # رکوردهای Mobile Originate
                    if typ == 1:  # MOC
                        if(len(rec) > 175+3):
                            isOK = True
                            calling = getPhoneNumber(rec, 44, 10)
                            called = getPhoneNumber(rec, 73, 12)
                            dur = getBCD(rec, 175, 3)

                            # حذف شماره های نا معتبر
                            if(len(calling) > 10 or len(called) > 10):
                                isOK = False

                            # حذف شماره های نا معتبر
                            if(len(calling) < 10 or len(called) < 10):
                                isOK = False

                            # حذف زمانهای کوتاه نامعتبر
                            if(dur < 15):
                                isOK = False
                    # رکوردهای Mobile Terminate
                    elif typ == 2:  # MTC
                        if(len(rec) > 126+3):
                            isOK = True
                            calling = getPhoneNumber(rec, 28, 10)
                            called = getPhoneNumber(rec, 54, 12)
                            dur = getBCD(rec, 126, 3)

                            # حذف شماره های نا معتبر
                            if(len(calling) > 10 or len(called) > 10):
                                isOK = False

                            # حذف شماره های نا معتبر
                            if(len(calling) < 10 or len(called) < 10):
                                isOK = False

                            # حذف زمانهای کوتاه نامعتبر
                            if(dur < 15):
                                isOK = False
                    # elif type==4: #ROAM
                    #     print(type,2+len(rec))
                    # elif type==8: #SMMO
                    #     print(type,2+len(rec))
                    # elif type==9: #SMMT
                    #     print(type,2+len(rec))
                    # elif type==11: #PSTN-originated call
                    #     print(type,2+len(rec))
                    # elif type==12: # PSTN-terminated call
                    #     print(type,2+len(rec))

                    # out.write(str(off)+'-type('+str(type)+'):,len('+str(2+len(rec))+'):')
                    # out.write(str(n0)+','+str(n1))
                    # for i in range(len(rec)):
                    #     out.write(','+str(rec[i]))
                    # out.write('\n')

                    if(isOK):
                        # print(type,'#',calling,'->',called,':',dur)
                        ind += 1

                        # تولید اکسل خروجی
                        out.write(str(ind)+','+calling+','+called +
                                  ','+str(dur))  # +','+str(off))
                        out.write('\n')

                        # # تولید گراف خروجی
                        # g.add_node(calling)
                        # g.add_node(called)

                        # # تصحیح وزن ارتباطات در صورت موجود بودن
                        # if g.has_edge(calling, called):
                        #     g[calling][called]['weight'] += dur
                        # else:
                        #     g.add_weighted_edges_from([(calling, called, dur)])

                # off=f.tell()
                n0c = readByte(f)
                n0 = hexToi(n0c)

        f.close()

# خواندن فایل csv


def readCSV(fileName, g):
    with open(fileName, 'rt') as f:
        for l in f.readlines():
            arr = l.replace('\n', '').split(',')
            calling = arr[1]
            called = arr[2]
            dur = arr[3]

            # تولید گراف خروجی
            g.add_node(calling)
            g.add_node(called)

            # تصحیح وزن ارتباطات در صورت موجود بودن
            if g.has_edge(calling, called):
                g[calling][called]['weight'] += 0 #dur
            else:
                g.add_weighted_edges_from([(calling, called, dur)])
