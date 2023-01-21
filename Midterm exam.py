#!/usr/bin/env python
# coding: utf-8

# # Kelompok 6
# 1. Akmal Zulkifli - 2101310
# 2. Bayu Wicaksono - 2106836
# 3. Fachri Najm Noer Kartiman - 2106515
# 4. Wildan Mauli Darojat - 2106330

# In[23]:


import random
from prettytable import PrettyTable


# In[2]:


guru = ["Everett Strickland", "Norma Watkins", "Ralph Chambers", "Belinda Rogers", "Ada Lindsey", "Velma Roberts" ,
"Susan Higgins", "Delores Gomez", "Vera Schmidt", "Sherry Holloway", "Paula Olson", "Sandy Norman", "Myrtle Mcguire", 
"Johnnie Chandler", "Shelley Jackson", "Jeannie Brewer", "Lillian Flores", "Alberta Foster", "Jacqueline Reid", "Roger Pratt",
"Tiffany Morris", "Thelma Lucas", "Sharon Garner", "Nichole Barnes", "Edgar Allison", "Stella Stephens", "Bobbie Farmer",
"Warren Nguyen", "Wilma Quinn", "Jacquelyn Clark", "Grace Perkins", "Geraldine Moran", "Ben Sanchez", "Guy Paul", 
"Beverly Baldwin", "Jacob Pearson", "Danny Burns", "Jessie Benson", "Malcolm Graham", "Angelica Thompson"]
time = ["07:00 - 08:30", "08:30 - 10:00", "10:30 - 12:00", "13:00 - 14:30"]
day = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at"]
kelas = ["7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H", "7I", "7J", 
        "8A", "8B", "8C", "8D", "8E", "8F", "8G", "8H", "8I", "8J", 
        "9A", "9B", "9C", "9D", "9E", "9F", "9G", "9H", "9I", "9J"]
matpel = ["Matematika", "IPA", "Bahasa Inggris", "Bahasa Indonesia", "Agama", "IPS", "PKN", "SBK", "Olahraga",
         "Prakarya", "Bahasa Daerah"]


# In[7]:


# membuat list berisi mata pelajaran dan guru pengampunya
guru_matpel = []
j = 0
for i in guru:
    if j == len(matpel):
        j = 0
    guru_matpel.append([i, matpel[j]])
    j = j + 1 


# In[8]:


# membuat list berisi hari dan waktu pelajarannya
day_time = []
for i in day:
    for j in time:
        day_time.append([i, j])


# In[9]:


init_pop = []
# membuat 50 jadwal lengkap / sebuah populasi
for x in range(50):
    jadwal = []
    for i in kelas:
        for j in day_time:
            lkosong = random.choices(guru_matpel)
            jadwal.append([i, j[0], j[1], lkosong[0][0], lkosong[0][1]])
    init_pop.append(jadwal)


# In[10]:


# fungsi untuk mengukur fitness function suatu jadwal lengkap / individu
def fitnessFunction(pop):
    n = len(jadwal)
    conflict = 0
    for i in range(0, n):
        for j in range(0, n):
            # jika bertemu dirinya sendiri maka akan di continue
            if pop[i] == pop[j]:
                continue
            # cek mata pelajaran tiap kelas dalam 1 hari agar tidak ada mata pelajaran yg duplikat
            if pop[i][0] == pop[j][0] and pop[i][1] == pop[j][1] and pop[i][4] == pop[j][4]:
                conflict += 1
            #cek guru pada hari tertentu dan waktu tertentu apakah mengajar dua kelas yg sama
            if pop[i][1] == pop[j][1] and pop[i][2] == pop[j][2] and pop[i][3] == pop[j][3]:
                conflict += 1
            # cek apakah guru yang mengajar mata pelajaran pada tiap kelas sama atau tidak
            if pop[i][0] == pop[j][0] and pop[i][4] == pop[j][4] and pop[i][3] != pop[j][3]:
                conflict += 1
    return conflict


# In[11]:


# memasukkan jadwal dengan fitness functionnya
populasi = []
for item in init_pop:
    populasi.append([fitnessFunction(item), item])


# In[12]:


populasi.sort()
new_pop = []
# dari 50 jadwal, dipilih 5 jadwal/individu dengan fitness function paling kecil (artinya bagus)
for item in range(5):
    new_pop.append(populasi[item][1])


# In[13]:


# fungsi untuk mutasi suatu kromosom
def mutate(child):
    temp = random.choices(guru_matpel)[0]
    child[3] =  temp[0]
    child[4] = temp[1]


# In[14]:


# untuk menampung 1 individu terbaik yang nilai fitness functionnya 0
schedule = []


# In[15]:


# algoritma genetic algoritma untuk 5 individu terbaik
for i in range(200):
    rankedFitness = []
    for pop in new_pop:
        rankedFitness.append([fitnessFunction(pop), pop])
    rankedFitness.sort()
    
    print("=== Gen " + str(i) + " best solution ===")
    print(rankedFitness[0][0])
    
    # cek nilai fitness function
    if rankedFitness[0][0] == 0:
        schedule = rankedFitness[0][1]
        break
    
    new_populasi = []
    for item in range(5):
        new_populasi.append(rankedFitness[item][1])
    # perulangan genetik algoritma
    for pop in new_populasi:
        for i in range(0, len(pop)):
            for j in range(0, len(pop)):
                # jika bertemu dirinya sendiri maka akan di continue
                if pop[i] == pop[j]:
                    continue
                #cek mata pelajaran tiap kelas yg duplikat dalam 1 hari
                if pop[i][0] == pop[j][0] and pop[i][1] == pop[j][1] and pop[i][4] == pop[j][4]:
                    mutate(pop[i])
                #cek guru pada hari tertentu dan waktu tertentu apakah mengajar dua kelas yg sama
                if pop[i][1] == pop[j][1] and pop[i][2] == pop[j][2] and pop[i][3] == pop[j][3]:
                    mutate(pop[i])
                    
    for pop in new_populasi:
        for i in range(0, len(pop)):
            for j in range(0, len(pop)):
                # jika bertemu dirinya sendiri maka akan di continue
                if pop[i] == pop[j]:
                    continue
                # cek apakah guru yang mengajar mata pelajaran pada tiap kelas sama atau tidak
                if pop[i][0] == pop[j][0] and pop[i][4] == pop[j][4] and pop[i][3] != pop[j][3]:
                    pop[j][3] = pop[i][3]
    
    new_pop = new_populasi


# In[16]:


# membuat kolom tiap kelas
kolom = []
tanda = 0
kolom2 = []
for j in range(0, len(schedule)):
    if j % 4 == 0:
        if j % 20 == 0:
            kolom.append([schedule[j][0], schedule[j][1], schedule[j][2], schedule[j][3], schedule[j][4]])
        else:
            kolom.append(['', schedule[j][1], schedule[j][2], schedule[j][3], schedule[j][4]])
    else:
        kolom.append(['', '', schedule[j][2], schedule[j][3], schedule[j][4]])
    if len(kolom) == 20:
        kolom2.append(kolom)
        kolom = []


# In[17]:


for i in range(len(kolom2)):
    kolom = PrettyTable(['Kelas', 'Hari', 'Jam', 'Guru', 'Mata Pelajaran'])
    for j in range(len(kolom2[i])):
        kolom.add_row([kolom2[i][j][0], kolom2[i][j][1], kolom2[i][j][2], kolom2[i][j][3], kolom2[i][j][4]])
    print(kolom, "\n")


# In[25]:


for item in schedule:
    if(item[1] == "Senin" and item[2] == "07:00 - 08:30"):
        print(item)


# In[26]:


for item in schedule:
    if(item[0] == "7A" and item[1] == "Senin"):
        print(item)


# In[ ]:




