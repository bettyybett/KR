import enum
import time

vecinii_pozitilor = {}
inapoi = set()
nr_pozitii={}

def muchie(u, v):
    vecinii_pozitilor.setdefault(u, []).append(v)
    vecinii_pozitilor.setdefault(v, []).append(u)

def invers(u, v):
    inapoi.add((u, v))


muchie(0, 1)
muchie(0, 2)
muchie(0, 3)
nr_pozitii.update({0:3})

muchie(1, 2)
muchie(1, 4)
muchie(1, 5)
invers(1, 0)
nr_pozitii.update({1:3})
muchie(2, 1)
muchie(2, 3)
muchie(2, 5)
invers(2, 0)
nr_pozitii.update({2:3})
muchie(3, 2)
muchie(3, 5)
muchie(3, 6)
invers(3, 0)
nr_pozitii.update({3:3})
muchie(4, 5)
muchie(4, 7)
invers(4, 1)
nr_pozitii.update({4:2})
muchie(5, 4)
muchie(5, 6)
muchie(5, 7)
muchie(5, 8)
muchie(5, 9)
invers(5, 1)
invers(5, 2)
invers(5, 3)
nr_pozitii.update({5:5})
muchie(6, 5)
muchie(6, 9)
invers(6, 3)
nr_pozitii.update({6:2})
muchie(7, 8)
muchie(7, 10)
invers(7, 4)
invers(7, 5)
nr_pozitii.update({7:1})
muchie(8, 7)
muchie(8, 9)
muchie(8, 10)
invers(8, 5)
nr_pozitii.update({8:1})
muchie(9, 8)
muchie(9, 10)
invers(9, 5)
invers(9, 6)
nr_pozitii.update({9:1})
invers(10, 7)
invers(10, 8)
invers(10, 9)
nr_pozitii.update({10:0})

inf = float("inf")

def pattern_table(values):
    return "  "+str(values[1])+"-"+str(values[4])+"-"+str(values[7])+"\n"+" /|\|/|\\"+"\n"\
           +str(values[0])+"-"+str(values[2])+ "-"+str(values[5])+"-"+str(values[8])+"-"+str(values[10])+"\n"+" \|/|\|/"+"\n"\
           + "  " +str(values[3])+"-"+str(values[6])+"-"+ str(values[9])
class Jucator(enum.Enum):
    hare = 1
    hounds = 2
    #se seteaza jucatorul
    def jucatorul_oponent(self):
        if self == self.hare:
            return self.hounds
        else:
            return self.hare

    def maximizare(self):
        return self == self.hare

class Hares_and_Hounds:
    def __init__(self, poz_hare, poz_hounds):
        self.poz_hare = poz_hare
        self.poz_hounds=poz_hounds

    @staticmethod
    def punctul_start():
        return Hares_and_Hounds(10,(0, 1, 3))

    def __repr__(self):
        tabla = ['*'] * 11

        tabla[self.poz_hare] = 'i'
        for poz_hound in self.poz_hounds:
            tabla[poz_hound] = 'c'

        return pattern_table(tabla)

    def hare_moves(self):
        mutari = []

        for v in vecinii_pozitilor[self.poz_hare]:
            if v in self.poz_hounds:
                continue

            nou_poz_hare = v

            mutari.append(Hares_and_Hounds(nou_poz_hare, self.poz_hounds))

        return mutari


    # verfifica care vecin nu este pozitionat inapoi
    def verif_inapoi(self):
        return lambda v: v not in inapoi

    def hound_moves(self):
        mutari = []

        for hound in range(3):
            poz_hound = self.poz_hounds[hound]


            nu_e_inapoi = self.verif_inapoi()

            for v in filter(nu_e_inapoi, vecinii_pozitilor[poz_hound]):
                if v == self.poz_hare or v in self.poz_hounds:
                    continue

                nou_poz_hounds = self.poz_hounds[:hound] + (v,) + self.poz_hounds[hound + 1:]
                mutari.append(Hares_and_Hounds(self.poz_hare, nou_poz_hounds))

        return mutari

    # daca iepurele a ajuns la pozitia 0
    def iepurele_a_evadat(self):
        return self.poz_hare == 0

    # daca cainii au incoltit iepurele
    def iepurele_e_inconjurat(self):
        return self.poz_hare == 10 and set(self.poz_hounds) == {7, 8, 9}

    def euristica(self):
        if self.iepurele_a_evadat():
            return inf

        if self.iepurele_e_inconjurat():
            return -inf

        return nr_pozitii[self.poz_hare] + sum(nr_pozitii[position] for position in self.poz_hounds)
def min_max(config, jucator, adancime):
    if adancime == 0:
        return config.euristica()

    celalalt_jucator = jucator.jucatorul_oponent()

    # mutarile posibila
    if jucator == Jucator.hare:
        urm_mutare = config.hare_moves()
    else:
        urm_mutare = config.hound_moves()

    # initializeaza scorul
    if jucator.maximizare():
        score = -inf
    else:
        score = +inf

    # verific mutarile posibile
    for conf in urm_mutare:
        #aleg fii pozitiei pe care sunt
        value = min_max(conf, celalalt_jucator, adancime - 1)
        #iau fiul cu scor max
        if jucator.maximizare():
            score = max(score, value)
        #iau fiul cu scor min
        else:
            score = min(score, value)

    return score

def alpha_beta(config, jucator, adancime, alpha=-inf, beta=+inf):

    if adancime == 0:
        return config.euristica()

    celalalt_juactor = jucator.jucatorul_oponent()


    if jucator == Jucator.hare:
        urm_mutare = config.hare_moves()
    else:
        urm_mutare = config.hound_moves()

    if jucator.maximizare():
        score = -inf
    else:
        score = +inf


    for conf in urm_mutare:
        value = alpha_beta(conf, celalalt_juactor, adancime - 1, alpha, beta)

        if jucator.maximizare():
            score = max(score, value)
            alpha = max(alpha, value)

        else:
            score = min(score, value)
            beta = min(beta, value)
        #conditia de retezare
        if alpha >= beta:
            break
    return score


#alegere alg
rasp=False
while not rasp:
    tip_algoritm=input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
    if tip_algoritm in ['1','2']:
        rasp=True
    else:
        print("Nu ati ales o varianta corecta. Alege 1 sau 2.")

#alegere adancime
rasp = False
while not rasp:
    nivel = input("nivelul de dificultate? \n 1.Incepator\n 2.Mediu\n 3.Avansat\n ")
    if nivel in ['1']:
        ADANCIME_MAX = 6
        rasp = True
    elif nivel in ['2']:
        ADANCIME_MAX = 8
        rasp = True
    elif nivel in ['3']:
        ADANCIME_MAX = 10
        rasp = True
    else:
        print("alegeti un numar intreg dintre 1, 2 sau 3.")


#alegere jucator
rasp=False
while not rasp:
    jucator1=input("hounds sau hare? ").lower()
    if (jucator1 in ['hounds']):
        rasp=True
        jucator1 = Jucator.hounds
        jucator2 = Jucator.hounds
    elif (jucator1 in ['hare']):
        rasp=True
        jucator1 = Jucator.hare
        jucator2 = Jucator.hare
    else:
        print("trebuie sa alegi hounds sau hare.")

computer_player = jucator1.jucatorul_oponent()
current_configuration = Hares_and_Hounds.punctul_start()

start_time = time.clock()
cnt_mutari=0
g=open("output","at")
g.write("\n--------------Ineputul unui nou joc-------------")
while True:
    if current_configuration.iepurele_a_evadat():
        print("hare a castigat")
        end_time = time.clock()
        timp=end_time-start_time
        g.write("\ntimpul jocului total: " + str(timp))
        if jucator2==jucator1:
            g.write("\nnr de mutari a lui hare: "+str(cnt_mutari))
            g.write("\nnr de mutari a lui hounds: "+str( cnt_mutari))
        else:
            g.write("\nnr de mutari a lui hounds: "+str( cnt_mutari))
            cnt_mutari = cnt_mutari + 1
            g.write("\nr de mutari a lui hare: "+str(cnt_mutari))
        break
    if current_configuration.iepurele_e_inconjurat():
        print("hounds a castigat")
        end_time = time.clock()
        timp = end_time - start_time
        g.write("\ntimpul jocului total: " + str(timp))
        if jucator2==jucator1:
            g.write("\nnr de mutari a lui hare: "+str(cnt_mutari))
            g.write("\nnr de mutari a lui hounds: "+str( cnt_mutari))
        else:
            g.write("\nnr de mutari a lui hare: "+str(cnt_mutari))
            cnt_mutari = cnt_mutari + 1
            g.write("\nnr de mutari a lui hounds: "+str( cnt_mutari))
        break
    start_time = time.clock()
    if jucator2 == jucator1:
        print(pattern_table(list(range(11))))

        print(current_configuration)
        try:
            if jucator2 == Jucator.hare:
                incerc_exit=input("care este pozitia pe care vrei sa mergi? (un numar intreg) : ").lower()
                if(incerc_exit=="exit"):
                    print("hounds a castigat")
                    end_time = time.clock()
                    timp = end_time - start_time
                    g.write("\ntimpul jocului total: " + str(timp))
                    g.write("\nnr de mutari a lui hare: "+str(cnt_mutari))
                    g.write("\nnr de mutari a lui hounds: "+str( cnt_mutari))
                    break
                else:
                    urm_mutare = int(incerc_exit)

                if urm_mutare == current_configuration.poz_hare:
                    raise ValueError("!!nu te poti muta aici")

                if urm_mutare in current_configuration.poz_hounds:
                    raise ValueError("!!nu te poti muta aici")
                if urm_mutare in vecinii_pozitilor[current_configuration.poz_hare] or (current_configuration.poz_hare,urm_mutare) in inapoi:
                    current_configuration = Hares_and_Hounds(urm_mutare, current_configuration.poz_hounds)
                    cnt_mutari = cnt_mutari + 1
                else:
                    raise ValueError("!!nu te poti muta aici")
            else:
                incerc_exit =input("de pe ce pozitie pleci si pe ce pozitie vrei sa ajungi? (doua numere intregi) :  ").lower()
                if (incerc_exit == "exit"):
                    print("hare a castigat")
                    end_time = time.clock()
                    timp = end_time - start_time
                    g.write("\ntimpul jocului total: " + str(timp))
                    g.write("\nnr de mutari a lui hare: "+str(cnt_mutari))
                    g.write("\nnr de mutari a lui hounds: "+str( cnt_mutari))
                    break
                else:
                    move = incerc_exit.split()
                if len(move) != 2:
                    raise ValueError("trebuie introduse doua numere intregi")
                poz_hound, urm_poz = map(int, move)
                if poz_hound not in current_configuration.poz_hounds:
                    raise ValueError("nu se poate misca acest caine")
                if (poz_hound, urm_poz) in inapoi:
                    raise ValueError("cainele nu se poate deplasa inapoi")

                hound = current_configuration.poz_hounds.index(poz_hound)

                if urm_poz == current_configuration.poz_hare:
                    raise ValueError("!!nu te poti muta aici")
                if urm_poz in current_configuration.poz_hounds:
                    raise ValueError("!!nu te poti muta aici")

                hpositions = current_configuration.poz_hounds
                if urm_poz in vecinii_pozitilor[poz_hound]:
                    current_configuration = Hares_and_Hounds(current_configuration.poz_hare,hpositions[:hound] + (urm_poz,) + hpositions[hound + 1:])
                    cnt_mutari = cnt_mutari + 1
                else:
                    raise ValueError("!!nu te poti muta aici")

        except ValueError as err:
            print("nu poti face miscarea asta:", err)
            continue
        end_time = time.clock()
        timp = end_time - start_time
        g.write("\nTimpul tau de gandire a fost: "+str(timp)+" la mutare cu numarul: "+ str(cnt_mutari)+"\n")
    else:
        if jucator2 == Jucator.hare:
            conf = current_configuration.hare_moves()
        else:
            conf = current_configuration.hound_moves()
        if computer_player.maximizare():
            func = max
        else:
            func = min

        if(tip_algoritm=='1'):
            best_config = func(conf, key=lambda config: min_max(config, jucator2, ADANCIME_MAX) )
        else:
            best_config = func(conf,key=lambda config: alpha_beta(config, jucator2, ADANCIME_MAX))

        current_configuration = best_config

        end_time = time.clock()
        timp = end_time - start_time
        g.write("\nTimpul de gandire a oponentului: "+str(timp)+ " la mutarea cu numarul: "+str(cnt_mutari)+"\n")


    jucator2 = jucator2.jucatorul_oponent()