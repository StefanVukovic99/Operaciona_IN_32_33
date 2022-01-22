# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 17:41:00 2022

@author: Mateja Miletić IN33-2018
"""

import numpy as np
import math


np.set_printoptions(suppress = True, precision = 3)

# C = [2, 1.5, 0, 0]
# A = np.matrix([[6, 3, 1, 0], [75, 100, 0, 1]])
# b = np.array([[1200], [25000]])
# base = np.array([[2], [3]])

C = [6, 14, 13, 0, 0]
A = np.matrix([[0.5, 2, 1, 1, 0], [1, 2, 4, 0, 1]])
b = np.array([[24], [60]])
base = np.array([[3], [4]])

# C = [1, 2, 3, 0, 0, 0]
# A = np.matrix([[1, 2, 3, 1, 0, 0], [2, 3, 1, 0, 1, 0], [4, 5, 6, 0, 0, 1]])
# b = np.array([[100], [200], [250]])
# base = np.array([[3], [4], [5]])

#print(base)

l = len(base) + 1
#print(l)


#simpleks tabela
tabela = np.zeros((l, l+2))
tabela[1:,1:l] = np.eye(l-1)
tabela[1:,l:l+1] = b
tabela[1:,0:1] = base

#print("Tabela bez pivot kolone:")
#print(tabela)

def simplexStep(base, tabela):
    #print("Tabela:")
    #print(tabela)
    w = tabela[0:1,1:l]
    #print("w:")
    #print(w)
    #kandidati za novu bazu
    base_candidates = np.zeros(len(C))
    base_candidates[:] = math.inf
    #print("base_candidates = ", base_candidates)
    
    arr = [i for i in range(len(C))] #pomocni niz koji predstavlja indekse svih promenljivih kako bi napravili razliku izmedju baznih i nebaznih
    #print(arr)
    #print("len(C) = ",len(C)) 
    
    non_base = np.setdiff1d(arr, base)
    #print("non_base = ",non_base)
    
    for j in non_base:
        aj = A[0:,j:j+1]
        cj = C[j]
        #print("aj:")
        #print(aj, "\n")
        #print("cj:")
        #print(cj, "\n")
        mul = w*aj-cj
        #print("mul = ",mul, "\n")
        base_candidates[j] = mul
    
    #Ovde biramo novi bazni element
    #print("base_candidates = ", base_candidates)
    new_base = min(base_candidates)
    #print("base_candidates = ", base_candidates)
    min_index_array = np.where(base_candidates == min(base_candidates))
    #print(min_index_array[0])
    if len(min_index_array[0]) == 0: #ovo je sad mozda suvisan uslov ali mi je u jednom trenutku trebao tako da ga nisam obrisao cisto radi bezbednosti
        print("kraj simpleksa")
        return
    min_index = min_index_array[0][0] #koji cheat juuuuuu
    #print("min_index = ", min_index)
    #print("new_base = ", new_base)
    
    tabela[0:1,l+1:] = new_base
    tabela[1:,l+1:] = tabela[1:,1:len(base)+1] * A[0:,min_index:min_index+1]
    print("\nTabela:")
    print(tabela,"\n")
    
    if new_base >= 0:
        print("Kraj simpleksa\n==============")
        print("Vrednost kriterijuma:", tabela[0,l])
        for i in range(1, l):
            if tabela[i,0] < len(C) - len(base):
                print("Vrednost parametra X", tabela[i,0].astype(int), " = ", tabela[i, l], sep='')
        print("Podrazumevana vrednost nedostajućih početnih parametra (ukoliko takvi postoje) iznosi 0.")
        print("Vrednosti dodatnih parametara nas ne zanimaju.")
        return
    
    pvt_col_candidate = np.zeros(len(base))
    #print(pvt_col_candidate)
    for i in range(1,l):
        pvt_col_candidate[i-1] = tabela[i:i+1, l:l+1]/tabela[i:i+1,l+1:l+2]
    #print("pvt_col_candidate = ", pvt_col_candidate)
    pvt_col_candidate_min_index_array = np.where(pvt_col_candidate == min(pvt_col_candidate))
    pvt_el_row = pvt_col_candidate_min_index_array[0][0]+1
    #print("pivot element row = ",pvt_el_row)
    pvt_el = tabela[pvt_el_row,l+1]
    #print("pvt_el = ", pvt_el)    
    
    #racunanje nove tabele
    new_tabela = tabela
    new_tabela[pvt_el_row:pvt_el_row+1, 0:1] = min_index
    base = new_tabela[1:,0:1]
    # print("new_tabela:")
    # print(new_tabela)
    # print("base:")
    # print(base)
    
    pomocna_tabela = tabela.copy()
    # print("pomocna_tabela:")
    # print(pomocna_tabela)
    for row in range(l):
        #print("\n")
        for col in range(1,len(C)):
            if row == pvt_el_row:
                new_tabela[row, col] = tabela[row,col]/pvt_el
            else:
                #print(tabela[row,col],"-",pomocna_tabela[pvt_el_row, col],"*",pomocna_tabela[row, l+1],"/",pvt_el)
                new_tabela[row, col] = pomocna_tabela[row,col] - pomocna_tabela[pvt_el_row, col]*pomocna_tabela[row, l+1]/pvt_el
                #print("new_tabela = ", new_tabela[row, col])
    
    simplexStep(base, new_tabela)
    
simplexStep(base, tabela)






























