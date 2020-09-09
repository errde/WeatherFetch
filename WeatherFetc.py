print("Käynnistetään ohjelma...")

import sqlite3
conn = sqlite3.connect('PAIKKAKUNTA.db')
#VAIHE1: tietokannan rakenteen luonti
sql = """ CREATE TABLE IF NOT EXISTS paikkakunta (
    nimi blob
)"""
print("Lisätään taulu tietokantaan")
kursori = conn.cursor()
kursori.execute(sql)


print("Tervetuloa sääsovellukseen")

print("Seuraavat paikkakunnat löydetty:")

sql = "SELECT nimi FROM paikkakunta" 
for rivi in kursori.execute(sql):
    print(rivi)


syöttö = False

while syöttö == False:

    vastaus = input("Haluatko syöttää uudet paikkakunnat (KYLLÄ/EI): ")

    if vastaus.upper() == "KYLLÄ":
        sql = "delete from paikkakunta"
        kursori.execute(sql)
        conn.commit()
        jatkaa = True
    else:
        jatkaa = False


    #VAIHE2: tietojen syöttö silmukassa
    while (jatkaa == True): 
        paikkakunta = input("Anna paikkakunta tai X lopettaaksesi: ")

        if paikkakunta.upper() == "X":
            jatkaa = False
        else:
            sql = 'INSERT INTO paikkakunta (nimi) VALUES(?)'
            kursori.execute(sql, [paikkakunta])
            conn.commit()
            print("Paikkakunta lisätty")

    #VAIHE3: tietojen haku tietokannasta ja tulostus ruudulle
    print()
    print("Paikkakunnat")
    sql = "SELECT nimi from paikkakunta"
    for rivi in kursori.execute(sql):
        print(rivi)

    vastaus2 = input("Haetaanko paikkakuntien säätiedot ilmatieteen laitokselta (KYLLÄ/EI): ")

    if vastaus2.upper() == "KYLLÄ":
        jatkaa2 = True
    else:
        exit()

    while (jatkaa2 == True):

        sql = "SELECT nimi from paikkakunta"

        maara = 0
        
        for rivi in kursori.execute(sql):

            print("Etsitään...")

            

            try:
                import http.client
                conn = http.client.HTTPSConnection("www.ilmatieteenlaitos.fi")
                conn.request("GET", f"/saa/{rivi[0]}")

                vastaus = conn.getresponse()
                html = str(vastaus.read())
            #print(html[:500])
                indeksi = html.index('<span class="temperature-plus')
                alku = indeksi + 47
                loppu = alku + 2
                lämpötila = html[alku:loppu]
                

                print(f"Lämpötila paikkakunnalla {rivi[0]} on tällä hetkellä {lämpötila} astetta")
                maara += 1
                
                from datetime import date

                aika = date.today()

                print(f"Hakuaika {aika}")

            except:
                print(f"Paikkakuntaa {rivi[0]} ei löytynyt")
                jatkaa2 = False

        jatkaa2 = False

    print(f"{maara}:n paikkakunnan sää haettiin onnistuneesti!")
    vastaus3 = input("Haluatko suorittaa uuden haun (KYLLÄ/EI)?")

    if vastaus3.upper() == "KYLLÄ":
        syöttö = False

    else:
        syöttö = True


kursori.close()
exit()
              
