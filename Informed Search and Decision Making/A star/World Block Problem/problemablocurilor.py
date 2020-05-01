import copy
import math
from timeit import default_timer as timer

class Nod:
    def __init__(self, stive, h=0):
        self.stive = stive
        self.h = h

    def este_in_lista(self, noduri):
        for i in range(len(noduri)):
            if noduri[i].nod.stive == self.stive:
                return i
        return None

    def __str__(self):
        return "({}, h: {})".format(self.stive, self.h)

    def __repr__(self):
        return "({}, h: {})".format(self.stive, self.h)

    def calculeaza_euristica(self, nod_scop):
        dict_curent = {}
        for i in range(len(self.stive)):
            for j in range(len(self.stive[i])):
                dict_curent[self.stive[i][j]] = (i, j)
        dict_scop = {}
        for i in range(len(nod_scop.stive)):
            for j in range(len(nod_scop.stive[i])):
                dict_scop[nod_scop.stive[i][j]] = (i, j)

        contor_euristica = 0
        for key in dict_curent:
            if dict_curent[key] != dict_scop[key]:
                contor_euristica += 1
        return contor_euristica

    def este_nod_scop(self, nod_scop):
        return self.stive == nod_scop.stive


class NodParcurgere:
    def __init__(self, nod, parinte, g, f):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = f

    def genereaza_succesori(self, nod_scop):
        lista_succesori = []
        for i in range(len(self.nod.stive)):
            if len(self.nod.stive[i]) > 0:
                for j in range(len(self.nod.stive)):
                    if i != j:
                        stive_temp = copy.deepcopy(self.nod.stive)
                        bloc = stive_temp[i].pop()
                        stive_temp[j].append(bloc)
                        nod = Nod(stive_temp)
                        nod.h = nod.calculeaza_euristica(nod_scop)
                        if self.f == math.inf:
                            succesor = NodParcurgere(nod, self, self.g + 1, 1 + nod.h)
                        else:
                            succesor = NodParcurgere(nod, self, self.g + 1, self.g + nod.h + 1)
                        lista_succesori.append(succesor)
        return lista_succesori

    def face_parte_din_drum(self):
        parinte = self.parinte
        while parinte is not None:
            if parinte.nod.stive == self.nod.stive:
                return True
            parinte = parinte.parinte
        return False

    def __str__(self):
        return "(nod: {}, parinte: {}, f: {}, g: {})".format(self.nod,
                                                             self.parinte if self.parinte is None else self.parinte.nod.stive,
                                                             self.f, self.g)

    def __repr__(self):
        return "(nod: {}, parinte: {}, f: {}, g: {})".format(self.nod,
                                                             self.parinte if self.parinte is None else self.parinte.nod.stive,
                                                             self.f, self.g)


class Problema:
    def __init__(self):
        self.stive_start = None
        self.stive_scop = None

    def citire_date_stiva(self, path_file):
        stive = []
        fisier_citire_start = open(path_file, "r")
        numar_stive = int(fisier_citire_start.readline())
        for _ in range(numar_stive):
            stiva = fisier_citire_start.readline().split()
            stive.append(stiva)
        fisier_citire_start.close()
        return stive

    def citire_date(self, path_file_start, path_file_scop):
        st_start = self.citire_date_stiva(path_file_start)
        self.stive_start = Nod(st_start)

        st_scop = self.citire_date_stiva(path_file_scop)
        self.stive_scop = Nod(st_scop, 0)
        self.stive_start.h = self.stive_start.calculeaza_euristica(self.stive_scop)

    def a_star(self):
        open = []
        closed = []
        open.append(NodParcurgere(self.stive_start, None, 0, self.stive_start.h))

        contor = 0
        while len(open) > 0:
            nod_curent = open.pop(0)
            closed.append(nod_curent)
            # print(nod_curent)

            if nod_curent.nod.este_nod_scop(self.stive_scop):
                drum = []
                while nod_curent is not None:
                    drum.append(nod_curent)
                    nod_curent = nod_curent.parinte
                drum.reverse()
                print(drum)
                break

            succesori_nod_curent = nod_curent.genereaza_succesori(self.stive_scop)
            for succesor in succesori_nod_curent:
                if not succesor.face_parte_din_drum():
                    in_lista_open = succesor.nod.este_in_lista(open)
                    if in_lista_open is not None:
                        if succesor.f < open[in_lista_open].f:
                            open[in_lista_open] = succesor
                    else:
                        in_lista_closed = succesor.nod.este_in_lista(closed)
                        if in_lista_closed is not None:
                            if succesor.f < closed[in_lista_closed].f:
                                open.append(succesor)
                                closed.pop(in_lista_closed)
                        else:
                            open.append(succesor)

            open.sort(key=lambda x: (x.f, -x.g))


if __name__ == "__main__":
    problemablocurilor = Problema()
    problemablocurilor.citire_date("stive_start.txt", "stive_scop.txt")
    start = timer()
    problemablocurilor.a_star()
    end = timer()
    print("Timpul de executie: {}".format(end-start))
