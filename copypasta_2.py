import random

def rand_line(soubor):
    with open("./copypasta_2/" + soubor, encoding="utf-8") as file:
        file_content = file.read().split("\n")
    x = random.choice(file_content)
    return x

osoba1 = rand_line("osoby1.txt")
co_probiha = rand_line("aktivity.txt")
jak_se_to_dela = rand_line("jak_se_to_dela.txt")
co_to_neni = rand_line("aktivity.txt")

while(co_probiha == co_to_neni):
    co_to_neni = rand_line("aktivity.txt")

jaky_to_byva_1 = rand_line("jaky_to_byva.txt")
jaky_to_byva_2 = rand_line("jaky_to_byva.txt")

while(jaky_to_byva_1 == jaky_to_byva_2):
    jaky_to_byva_2 = rand_line("jakoy_to_byva.txt")

pro_koho_1 = rand_line("pro_koho.txt")
pro_koho_2 = rand_line("pro_koho.txt")

while(pro_koho_1 == pro_koho_2):
    pro_koho_2 = rand_line("pro_koho.txt")

cinnost = rand_line("cinnosti.txt")
kazdy_1 = rand_line("kazdy_1.txt")
kazdy_2 = rand_line("kazdy_2.txt")
kazdy_3 = rand_line("kazdy_2.txt")

while(kazdy_3 == kazdy_2):
    kazdy_3 = rand_line("kazdy_2.txt")

vic = rand_line("a_jelikoz_je_nas_vic.txt")
jen = rand_line("dvojice_jen.txt")
sehnali = rand_line("sehnali.txt")
osoba2 = rand_line("osoby2.txt")

def copypasta_2():
    skupinky = random.choice(["páry", "trojice", "čtveřice"])
    return ("Hii, zjistily jsme s " +
        osoba1 +
        ", že spoustu lidí neví, že na maturáku probíhá nějaké " + 
        co_probiha + 
        ". Jde o to, že po vystoupení " +
        random.choice(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]) + random.choice(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]) +
        " se musí dostat nějakým způsobem do " + 
        str(random.randint(2,4)) + 
        " řad, ze kterých potom jde nástup " + 
        random.choice(["jednotlivců", "dvojic", "trojic"]) + 
        ". A dělá se to tak, že " + 
        jak_se_to_dela + 
        ".\n\nNení to jako " +
        co_to_neni + 
        ", většinou to bývá víc " +
        jaky_to_byva_1 + 
        " a " +
        jaky_to_byva_2 +
        " - pro " +
        pro_koho_1 +
        " a " +
        pro_koho_2 +
        " ;)\n\nTak jsme si to s " +
        osoba1 +
        " představovaly tak, že by se " +
        cinnost +
        random.choice([" v párech", " ve trojicích", " ve čtveřicích"]) +
        ". Z praktických důvodů by bylo lepší, kdyby " +
        kazdy_1 +
        " k sobě " +
        kazdy_2 + 
        " a ne " +
        kazdy_3 +
        ", ale jelikož je nás " +
        vic +
        " víc, budou nějaké " + 
        skupinky +
        " jen " +
        jen + 
        " (teoreticky! " +
        str(random.randint(2,4)) +
        " " + skupinky +
        ").\n\nTakže by bylo super, kdybyste si během tohodle týdne sehnali " +
        sehnali +
        " a napsali to bud mně do chatu, nebo " + 
        osoba2 +
        ".\nDíky za spolupráci!"        
    )

if __name__ == "__main__":
    print(copypasta_2())