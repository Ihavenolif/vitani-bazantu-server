import random 

kdy = ["o velké přestávce", "o volné hodině", "před školou", "po škole", "o třídnické"]
mohli = ["tancovat", "počkat", "stát", "chlastat", "zůstat", "vydržet", "ležet"]
kde = ["ve třídě", "ve výtvarce", "v biologii", "ve škole", "v parku", "v hospodě"]
potřebujeme = ["vyřešit tu věc s Mádlem", "vyřešit grafika", "vyřešit předtančení", "vyřešit půlnočko", "dotočit video", "secvičit nástup"]
kdyby = ["u toho byla celá třída", "jste mohli", "jste donesli alkohol", "přišel Ivan", "jste se opili jenom trochu", "jste si donesli šaty", "se povedlo ušetřit"]
def random_kdy():
    return kdy[random.randint(0,len(kdy)-1)]
def random_mohli():
    return mohli[random.randint(0,len(mohli)-1)]
def random_kde():
    return kde[random.randint(0,len(kde)-1)]
def random_potřebujeme():
    return potřebujeme[random.randint(0,len(potřebujeme)-1)]
def random_kdyby():
    return kdyby[random. randint(0,len(kdyby)-1)]

def copypasta_3():
    return "Dobré ráno, chtěla bych vás všechny poprosit, jestli byste " + random_kdy() + " nemohli chvíli " + random_mohli() + " " + random_kde() + ", potřebujeme ještě " + random_potřebujeme() + " a bylo by dobře, kdyby " + random_kdyby() + ", děkuju :)"
