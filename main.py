import math
import random

## 1. PARAMETER ALGORITMA
ukuran_populasi = 50
panjang_kromosom = 32
prob_crossover = 0.8
prob_mutasi = 0.05
maksimal_generasi = 100

## 2. PROSES ALGORITMA GENETIKA
# Proses 1: Inisialisasi populasi
def buat_populasi_awal():
    populasi = []
    for i in range(ukuran_populasi):
        kromosom = []
        
        for j in range(panjang_kromosom):
            angka_acak = random.randint(0, 1)
            kromosom.append(angka_acak)
        populasi.append(kromosom)
    return populasi

# Proses 2: Dekode kromosom
def dekode(kromosom):
    # Memotong kromosom menjadi dua bagian
    biner_x1 = kromosom[0:16]
    biner_x2 = kromosom[16:32]
    
    # Mengubah array biner menjadi teks string
    teks_x1 = ""
    for bit in biner_x1:
        teks_x1 = teks_x1 + str(bit)
        
    teks_x2 = ""
    for bit in biner_x2:
        teks_x2 = teks_x2 + str(bit)
        
    # Mengubah teks biner menjadi angka desimal
    desimal_x1 = int(teks_x1, 2)
    desimal_x2 = int(teks_x2, 2)
    
    # Rumus pemetaan nilai ke batas domain -10 sampai 10
    # Nilai maksimal dari 16 bit biner adalah 65535
    x1 = -10 + ((10 - (-10)) / 65535) * desimal_x1
    x2 = -10 + ((10 - (-10)) / 65535) * desimal_x2
    
    return x1, x2

# Proses 3: Perhitungan fitness
def hitung_fitness(kromosom):
    x1, x2 = dekode(kromosom)
    
    # Memasukkan x1 dan x2 ke dalam fungsi
    # f(x1,x2) = -(sin(x1)*cos(x2)*tan(x1+x2) + 0.5*exp(1-sqrt(x2^2)))
    bagian1 = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
    bagian2 = 0.5 * math.exp(1 - math.sqrt(x2**2))
    nilai_fungsi = -(bagian1 + bagian2)
    
    # Karena kita mencari nilai MINIMUM, maka fitness adalah kebalikannya.
    # Semakin kecil nilai fungsinya, semakin besar fitness-nya.
    nilai_fitness = -nilai_fungsi 
    
    return nilai_fitness, nilai_fungsi

# Proses 4: Pemilihan orangtua (Metode Turnamen Sederhana)
def seleksi_orangtua(populasi, semua_fitness):
    # Memilih 2 indeks secara acak
    indeks1 = random.randint(0, ukuran_populasi - 1)
    indeks2 = random.randint(0, ukuran_populasi - 1)
    
    # Mengadu dua individu tersebut, yang fitness-nya lebih besar yang menang
    if semua_fitness[indeks1] > semua_fitness[indeks2]:
        return populasi[indeks1]
    else:
        return populasi[indeks2]

# Proses 5: Crossover (Pindah Silang)
def pindah_silang(induk1, induk2):
    anak1 = []
    anak2 = []
    
    # Cek apakah terjadi pindah silang berdasarkan probabilitas
    if random.random() < prob_crossover:
        # Menentukan titik potong secara acak
        titik_potong = random.randint(1, panjang_kromosom - 1)
        
        # Menggabungkan potongan induk1 dan induk2
        anak1 = induk1[0:titik_potong] + induk2[titik_potong:panjang_kromosom]
        anak2 = induk2[0:titik_potong] + induk1[titik_potong:panjang_kromosom]
    else:
        # Jika tidak terjadi pindah silang, anak sama persis dengan induk
        anak1 = induk1.copy()
        anak2 = induk2.copy()
        
    return anak1, anak2

# Proses 6: Mutasi
def mutasi(kromosom):
    for i in range(panjang_kromosom):
        # Cek setiap bit, apakah bermutasi berdasarkan probabilitas
        if random.random() < prob_mutasi:
            if kromosom[i] == 0:
                kromosom[i] = 1
            else:
                kromosom[i] = 0
    return kromosom

## 3. PROGRAM UTAMA (LOOP EVOLUSI)
populasi = buat_populasi_awal()

# Variabel untuk menyimpan pencapaian terbaik sepanjang masa
kromosom_terbaik_global = None
nilai_minimum_global = 9999999.0

for generasi in range(maksimal_generasi):
    semua_fitness = []
    semua_nilai_fungsi = []
    
    # Hitung fitness untuk semua individu di populasi saat ini
    for kromosom in populasi:
        fitness, nilai_fungsi = hitung_fitness(kromosom)
        semua_fitness.append(fitness)
        semua_nilai_fungsi.append(nilai_fungsi)
        
        # Simpan jika menemukan solusi yang lebih baik
        if nilai_fungsi < nilai_minimum_global:
            nilai_minimum_global = nilai_fungsi
            kromosom_terbaik_global = kromosom.copy()
            
    # Proses 7: Pergantian Generasi
    populasi_baru = []
    
    # Looping sampai populasi baru penuh (50 individu)
    while len(populasi_baru) < ukuran_populasi:
        # Pilih 2 orangtua
        bapak = seleksi_orangtua(populasi, semua_fitness)
        ibu = seleksi_orangtua(populasi, semua_fitness)
        
        # Lakukan kawin silang
        anak1, anak2 = pindah_silang(bapak, ibu)
        
        # Lakukan mutasi
        anak1 = mutasi(anak1)
        anak2 = mutasi(anak2)
        
        # Masukkan ke populasi baru
        populasi_baru.append(anak1)
        if len(populasi_baru) < ukuran_populasi: # Mencegah kelebihan jumlah
            populasi_baru.append(anak2)
            
    # Gantikan populasi lama dengan yang baru
    populasi = populasi_baru

## 4. OUTPUT HASIL
x1_akhir, x2_akhir = dekode(kromosom_terbaik_global)

print("=== HASIL ALGORITMA GENETIKA ===")
print("Kromosom Terbaik :", kromosom_terbaik_global)
print("Nilai x1         :", x1_akhir)
print("Nilai x2         :", x2_akhir)
print("Nilai f(x1, x2)  :", nilai_minimum_global)