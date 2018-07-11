#!/bin/python2
# -*- coding: utf-8 -*-

'''
-----------------------------------------
Funció MixColumn del xifratge AES
-----------------------------------------

La intenció d'aquesta funció és ser sufi-
cientment autoexplicativa. També hi han
aclaracions del que està està fent. 

Per tal de facilitar la comprovació del tutor,
posi les xifres de la columna en aquesta variable
(recordi que els valors són de 8 bits. No possi
cap valor superior a 255 o inferior a 0)
'''

column = [255, 21, 43, 111]



from copy import copy

def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    i=0
    while i <= 8:
             #Operació a nivell binari AND
        if (b & 1) == 1:
            #Operació a nivell binari XOR
            p ^= a
                     #Operació a nivell binari AND
        hiBitSet = a & 0x80
          # MOU BITS A L'ESQUERRA
        a <<= 1
        if hiBitSet == 0x80:
            #Operació a nivell binari XOR
            a ^= 0x1b
          # MOU BITS A LA DRETA
        b >>= 1
             # MODUL
        i+=1
    return (p % 256)

def mixColumn(column):
    temp = copy(column)
    # matriu:
    #     [ 2  3  1  1]
    #     [ 1  2  3  1]
    #     [ 1  1  2  3]
    #     [ 3  1  1  2]
    
    # fem la multiplicació (en un cos finit 256) entre la matriu i la columna 
    column[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ \
                galoisMult(temp[2],1) ^ galoisMult(temp[1],3)

    column[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ \
                galoisMult(temp[3],1) ^ galoisMult(temp[2],3)

    column[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ \
                galoisMult(temp[0],1) ^ galoisMult(temp[3],3)

    column[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ \
                galoisMult(temp[1],1) ^ galoisMult(temp[0],3)
    return column

def mixColumnInv(column):
    temp = copy(column)
    # matriu:
    #     [14 11 13  9]
    #     [ 9 14 11 13]
    #     [13  9 14 11]
    #     [11 13  9 14]
    column[0] = galoisMult(temp[0],14) ^ galoisMult(temp[3],9) ^ \
                galoisMult(temp[2],13) ^ galoisMult(temp[1],11)

    column[1] = galoisMult(temp[1],14) ^ galoisMult(temp[0],9) ^ \
                galoisMult(temp[3],13) ^ galoisMult(temp[2],11)

    column[2] = galoisMult(temp[2],14) ^ galoisMult(temp[1],9) ^ \
                galoisMult(temp[0],13) ^ galoisMult(temp[3],11)

    column[3] = galoisMult(temp[3],14) ^ galoisMult(temp[2],9) ^ \
                galoisMult(temp[1],13) ^ galoisMult(temp[0],11)
    return column

print "columna a barregar: ", column
mixColumn(column)
print "barregada:          ", column
mixColumnInv(column)
print "desbarregada:       ", column
