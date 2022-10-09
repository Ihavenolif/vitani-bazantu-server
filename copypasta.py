import random

AKTIVITY = ["natáčí video", "zařizuje Jitku", "designuje plakát", "zakládá Instagram", "secvičuje předtančení", "má schůzku s agenturou"]
TYMY = ["sestaví scénář", "se sejde s pánem na Jitce", "domluví grafika", "bude spravovat sociální sítě", "vymyslí a zorganizuje choreografii", "domluví, co vlastně od od Agentury chceme", "se s agenturou domluví na finančním poradenství", "přesvědčí tu otravnou půlku třídy, že nechtějí nafukovací rukavice"]
TRIDY = ["Béčko", "Céčko", "Áčko ze zdrávky", "Béčko ze zdrávky", "Céčko ze zdrávky", "Áčko z obchodky", "Béčko z obchodky", "Céčko z obchodky", "Áčko ze sošky", "Béčko ze sošky", "Céčko ze sošky"]

def random_trida():
    return TRIDY[random.randint(0,len(TRIDY)-1)]

def random_aktivita():
    return AKTIVITY[random.randint(0,len(AKTIVITY)-1)]

def random_tym():
    return TYMY[random.randint(0,len(TYMY)-1)]

def copypasta():
    pocet_dnu = random.randint(1,14)
    den = ""

    if pocet_dnu == 1:
        den = " den "
    elif pocet_dnu > 1 and pocet_dnu < 5:
        den = " dny "
    else:
        den = " dní "

    return ("Jen bych chtěla poznamenat, že " + 
    random_trida() + 
    " už za " +
    str(pocet_dnu) + 
    den + 
    random_aktivita() +
    ", měli bychom fakt sestavit tým, který " +
    random_tym()+
    ".")

if __name__ == "__main__":
    for x in range(20):
        print(copypasta())

