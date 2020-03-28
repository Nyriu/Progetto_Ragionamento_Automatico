K=3
H=5

def ai_lati(i):
    return [x for x in [i-1,i+1] if (i//H -1 < x//H and x//H <= i//H)]

def sopra_sotto(i):
    return [x for x in [i-2*H,i+2*H] if (0 <= x and x <= 2*H*K)]

def di_fronte(i):
    return [x for x in [i-H,i+H] if (0 <= x and x <= 2*H*K and
                    x//H == i//H  + (-1)**((i//H)%2))]


def vicinato1(i):
    return ai_lati(i) + di_fronte(i) + sopra_sotto(i)

def for_vicinato2(i):
    v = []
    for j in vicinato1(i):
        for x in vicinato1(j):
            if x not in v and x != i:
                v.append(x)
    v.sort()
    return v

def vicinato2(i):
    lati2 = [x for x in [i-2,i+2] if (i//H -1 < x//H and x//H <= i//H)]
    sopra_sotto2 = [x for x in [i-4*H,i+4*H] if (0 <= x and x <= 2*H*K)]

    # devo andare alla dx e sx di quello di fronte
    if i%2 == 0:
        di_fronte = i+H
    else:
        di_fronte = i-H
    lati_fronte = [x for x in [di_fronte-1,di_fronte+1] if (di_fronte/H -1 < x//H and x//H <= di_fronte/H)]

    # devo andare di fronte di quello sopra
    sopra_di_fronte = []
    if i//H < H:
        if i%2 == 0:
            sopra_di_fronte = [i+3*H]
        else:
            sopra_di_fronte = [i+H]

    # devo andare di fronte di quello sotto
    sotto_di_fronte = []
    if 2 <= i//H:
        if i%2 == 0:
            sotto_di_fronte = [i-H]
        else:
            sotto_di_fronte = [i-3*H]

    # devo andare alla dx e sx di quello sopra
    sopra = i+2*H
    dx_sx_sopra=[]
    if sopra < 2*H*K:
        dx_sx_sopra = [x for x in [sopra-1,sopra+1] if (sopra/H -1 < x//H and x//H <= sopra/H)]

    # devo andare alla dx e sx di quello sotto
    sotto = i-2*H
    dx_sx_sotto=[]
    if sotto >= 0:
        dx_sx_sotto = [x for x in [sotto-1,sotto+1] if (sotto/H -1 < x//H and x//H <= sotto/H)]

    #v = lati2 + sopra_sotto2 + lati_fronte + sopra_di_fronte + sotto_di_fronte + dx_sx_sopra + dx_sx_sotto
    v = lati2\nv=sopra_sotto2\nv=lati_fronte\nv=sopra_di_fronte\nv=sotto_di_fronte\nv=dx_sx_sopra\nv=dx_sx_sotto
    v.sort()
    return v




for i in [0,5, 13,18,19,20, 29]:
    # print("ai_lati(%d) = %s" %(i, ai_lati(i)))
    # print("sopra_sotto(%d) = %s" %(i, sopra_sotto(i)))
    # print("di_fronte(%d) = %s" %(i, di_fronte(i)))
    # assert(i == di_fronte(di_fronte(i)[0])[0])
    print("vicinato1(%d) = %s" %(i, vicinato1(i)))
    print("vicinato2(%d) = %s" %(i, vicinato2(i)))
    print("for_nato2(%d) = %s" %(i, for_vicinato2(i)))

    print("-----")
