'''Problema blocurilor'''
'''234 Diaconu Beatrice'''

class input:
	def __init__(self, stive):
		self.stive = stive

	def pozitii(self):

		pozitii = {}
		for i, stiva in enumerate(self.stive):
			for j, cub in enumerate(stiva):
				pozitii[cub] = (i, j)
		return pozitii

	def euristica(self):

		global pozitii_finale
		distanta = 0
		pozitii = self.pozitii()
		for cub in cuburi:
			if pozitii[cub] != pozitii_finale[cub]:
				distanta += 1

		return distanta

	def __eq__(self, other):
		return self.stive == other.stive

	def __repr__(self):
		return f'{self.stive}'

N = 3

cuburi = ['a', 'b', 'c', 'd']

M = len(cuburi)

init= input([
	['a'],
	['c', 'b'],
	['d'],
])

scop = input([
	['b', 'c'],
	[],
	['d', 'a'],
])

pozitii_finale = scop.pozitii()


class Nod:
	def __init__(self, configuratie):
		self.info = configuratie
		self.h = configuratie.euristica()

	def __str__ (self):
		return "({}, h={})".format(self.info, self.h)
	def __repr__ (self):
		return f"({self.info}, h={self.h})"


class Arc:
	def __init__(self, capat, varf):
		self.capat = capat
		self.varf = varf
		self.cost = 1 # toate mutările au cost 1

class Problema:
	def __init__(self):
		self.noduri = [
			Nod(init)
		]
		self.arce = []
		self.nod_start = self.noduri[0]
		self.nod_scop = scop

	def cauta_nod_nume(self, info):

		for nod in self.noduri:
			if nod.info == info:
				return nod
		return None


class NodParcurgere:

	problema = None

	def __init__(self, nod_graf, parinte=None, g=0, f=None):
		self.nod_graf = nod_graf
		self.parinte = parinte
		self.g = g
		if f is None :
			self.f = self.g + self.nod_graf.h
		else:
			self.f = f


	def drum_arbore(self):

		nod_c = self
		drum = [nod_c]
		while nod_c.parinte is not None :
			drum = [nod_c.parinte] + drum
			nod_c = nod_c.parinte
		return drum


	def contine_in_drum(self, nod):

		nod_curent = self
		while nod_curent:
			if nod_curent.nod_graf.info == nod.info:
				return True
			nod_curent = nod_curent.parinte
		return False

	def expandeaza(self):
		configuratie = self.nod_graf.info
		succesori = []
		for stiva_sursa in range(N):
			for stiva_destinatie in range(N):
				if stiva_sursa == stiva_destinatie:
					continue

				if not configuratie.stive[stiva_sursa]:
					continue


				cub_de_mutat = configuratie.stive[stiva_sursa][-1]

				stive_noi = []
				for i in range(N):
					if i == stiva_sursa:
						stiva_noua = configuratie.stive[i][:-1]
					elif i == stiva_destinatie:
						stiva_noua = configuratie.stive[i] + [cub_de_mutat]
					else:
						stiva_noua = configuratie.stive[i]

					stive_noi.append(stiva_noua)

				configuratie_noua = input(stive_noi)

				succesor = problema.cauta_nod_nume(configuratie_noua)

				if not succesor:
					nod_nou = Nod(configuratie_noua)
					problema.noduri.append(nod_nou)
					succesor = nod_nou

				cost = 1
				succesori.append((succesor, cost))

		return succesori


	def test_scop(self):
		return self.nod_graf.info == self.problema.nod_scop


	def __str__ (self):
		parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
		return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"



""" Algoritmul A* """


def str_info_noduri(l):
	sir=""
	for x in l:
		sir+=str(x)+"  "
	return sir


def afis_succesori_cost(l):

	sir=""
	for (x, cost) in l:
		sir+="\nnod: "+str(x)+", cost arc:"+ str(cost)
	return sir


def in_lista(l, nod):
	for i in range(len(l)):
		if l[i].nod_graf.info == nod.info:
			return l[i]
	return None


def a_star():
	rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
	open = [rad_arbore]
	closed = []

	while open: # cât timp mai avem noduri neexplorate
		# se scoate nodul din open
		nod_curent = open.pop(0)

		# se pune în closed
		closed.append(nod_curent)

		if nod_curent.test_scop(): # am ajuns la țintă
			break

		drum = nod_curent.drum_arbore()

		for succesor, cost in nod_curent.expandeaza():
			if in_lista(drum, succesor):
				continue

			nod_open = in_lista(open, succesor) # îl caut în lista open
			nod_closed = in_lista(closed, succesor) # îl caut în lista closed

			# calculez distanța dacă ar fi să trec prin `nod_curent` să ajung la succesor
			g_nou = nod_curent.g + cost

			if nod_open: # dacă l-am găsit încerc să îl actualizez
				# dacă am găsit o distanță mai bună
				if g_nou < nod_open.g:
					nod_open.g = g_nou
					nod_open.f = g_nou + nod_open.nod_graf.h
					nod_open.parinte = nod_curent

			elif nod_closed:
				f_nou = g_nou + nod_closed.nod_graf.h

				if f_nou < nod_closed.f:
					nod_closed.g = g_nou
					nod_closed.f = f_nou + nod_closed.nod_graf.h
					nod_closed.parinte = nod_curent

					# dacă l-am actualizat, se mută înapoi în open,
					# ca să îi re-explorez vecini
					open.append(nod_closed)
			else:
				# nu e în nicio listă, îl pun în open inițial
				nod_nou = NodParcurgere(
					nod_graf=succesor,
					parinte=nod_curent,
					g=g_nou
				)

				open.append(nod_nou)

		# teoretic ar trebui ca `open` să fie max heap,
		# dar merge și dacă îl sortez și scot mereu minimul
		open.sort(key=lambda nod: nod.f)

	print("\n------------------ Concluzie -----------------------")

	if(len(open)==0):
		print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
	else:
		print("Drum de cost minim: \n" + str_info_noduri(nod_curent.drum_arbore() ))





if __name__ == "__main__":
	problema = Problema()
	NodParcurgere.problema = problema
	a_star()