import pickle
import math
import time
from typing import NamedTuple

info_frunze = {} #dictionarul cu informatiile despre frunze

lista_fisiere_input = ['input_1','input_2','input_3','input_4']
lista_fisiere_output = ['output_1',"output_2","output_3","output_4"]

iterator_input=0
iterator_output=0

#"struct" punct
class Coordonate(NamedTuple):
    x: float
    y: float
#struct frunza
class Info_Frunza(NamedTuple):
    id: str
    poz:tuple
    insecte:int
    greutate:float

#distanta dintre doua puncte

def distanta_puncte(a, b):

    return math.sqrt(pow((a.x - b.x),2) + pow((a.y - b.y), 2))


class Nod:
    def __init__(self, frunze, ident_frunza, greutate):
        self.frunze = frunze
        self.ident_frunza = ident_frunza
        self.greutate = greutate
        self.info = (frunze, ident_frunza, greutate)
        self.h = self.distanta_de_la_punct_la_cerc(self.dict.poz)

    @property
    def dict(self):
        return self.frunze[self.ident_frunza]

    # distanta de la punct la marginea lacului
    def distanta_de_la_punct_la_cerc(self, p):
        return raza - distanta_puncte(p, Coordonate(0, 0))


class NodParcurgere:

    problema = None  # atribut al clasei

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf  # obiect de tip Nod
        self.parinte = parinte  # obiect de tip Nod
        self.g = g  # costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f
    def drum_arbore(self):

        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):

        nod_c = self
        while nod_c.parinte is not None:
            if nod.info == nod_c.nod_graf.info:
                return True
            nod_c = nod_c.parinte
        return False

    def expandeaza(self):

        frunze, id, greutate = self.nod_graf.info
        frunza = frunze[id]  #salvez tuplurile frunzelor existente in dict frunze
        l_succesori = []

        for frz in frunze.values():
            if frunza.id == frz.id: #verifica daca exista in tuplu
                continue

            for insecte in range(frunza.insecte + 1):
                gr_noua = greutate + insecte #adauga insectele la greutatea avuta

                if distanta_puncte(frunza.poz, frz.poz) > gr_noua / 3:
                    continue

                gr_noua -= 1 #scadem energia pierduta pentru saritura

                if gr_noua > frz.greutate: #daca greutatea mormolocului e mai mare ca greutatea frunzei continua
                    continue

                if gr_noua < 0: #daca mormolocul are greutatea mai mica ca 0 nu poate iesi din lac
                    break

                frunze_noi = pickle.loads(pickle.dumps(frunze))  #stocam noiile frunze gasite
                frunze_noi[frunza.id] = Info_Frunza(frunza.id,frunza.poz,frunza.insecte - insecte,frunza.greutate)

                nod = Nod(frunze_noi, frz.id, gr_noua)
                l_succesori.append((nod, 1))
        return l_succesori

    # se modifica in functie de problema
    def test_scop(self):
        frunza = self.nod_graf.dict #dau coordonatele frunzei actuale
        greutate = self.nod_graf.greutate #greutatea avuta
        return self.nod_graf.distanta_de_la_punct_la_cerc(frunza.poz) <= greutate / 3


def in_lista(l, nod):

    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None


def a_star():
    start_time=time.clock()

    nod_start = Nod(info_frunze, frunza_start, greutate_initiala) #nodul start est eprimul nod din dictionar
    rad_arbore = NodParcurgere(nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere
    if rad_arbore.test_scop():
        g.write("mormolocul este deja la mal \n")
        open.append(rad_arbore)

    while len(open)>0:  # cât timp mai avem noduri neexplorate

        nod_curent = open.pop(0)     # scoatem primul element din lista open

        closed.append(nod_curent)    # si il adaugam la finalul listei closed

        # testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
        if nod_curent.test_scop():
            break

        drum = nod_curent.drum_arbore() #lista de noduri,drumul de la nod pana la radacina

        l_succesori = nod_curent.expandeaza()  # contine tupluri de tip (Nod, numar)
        for nod_succesor, cost_succesor in l_succesori:

            nod_open = in_lista(open, nod_succesor)  # caut nodul in open
            nod_closed = in_lista(closed, nod_succesor)  # caut nodul in closed
            # calculez distanța dacă ar fi să trec prin `nod_curent` să ajung la succesor
            g_succesor = nod_curent.g + cost_succesor

            if nod_open:  # dacă l-am găsit încerc să îl actualizez
                # dacă am găsit o distanță mai bună
                if g_succesor < nod_open.g:
                    nod_open.g = g_succesor
                    nod_open.f = g_succesor + nod_open.nod_graf.h
                    nod_open.parinte = nod_curent

            elif nod_closed:
                f_succesor = g_succesor + nod_closed.nod_graf.h

                if f_succesor < nod_closed.f: #verific daca drumul actual e mai bun ca drumul vechi
                    nod_closed.g = g_succesor #acualizez g
                    nod_closed.f = f_succesor + nod_closed.nod_graf.h #actualizez f
                    nod_closed.parinte = nod_curent # actualizez parintele

                    # dacă l-am actualizat, se muta înapoi în open,
                    # ca să îi re-explorez vecini
                    open.append(nod_closed)
            else:
                # daca nu e in nicio lista il pun in lista open
                nod_nou = NodParcurgere( nod_graf=nod_succesor,parinte=nod_curent, g=g_succesor)
                open.append(nod_nou)


    if (len(open) == 0):
        g.write("mormolocul nu poate evada\n")
    else:
        drum = nod_curent.drum_arbore()
        for nod in drum:
            nod_graf = nod.nod_graf
            frunze, ident_frunza, greutate = nod_graf.info
            g.write("mormolocul este la frunza: "+ident_frunza+" si are greutatea actuala: "+str(greutate)+"\n")
    end_time=time.clock()
    print(end_time-start_time)


while (iterator_input < lista_fisiere_input.__len__()):
    with open(lista_fisiere_input[iterator_input]) as f:
        raza =float(f.readline())
        greutate_initiala = float(f.readline())
        frunza_start = f.readline().strip()
        for line in f:
            id, x, y, nr_insecte, greutate_max = line.split()
            poz = Coordonate(float(x), float(y))
            info_frunze[id] = Info_Frunza(id, poz, int(nr_insecte), float(greutate_max))

    g = open(lista_fisiere_output[iterator_output], mode='wt')
    a_star()
    iterator_input = iterator_input + 1
    iterator_output = iterator_output + 1




