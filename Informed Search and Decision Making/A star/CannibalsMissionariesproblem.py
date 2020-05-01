import copy
from timeit import default_timer as timer

numar_persoane = 3
numar_locuri_barca = 2


class Nod:
    def __init__(self, info, h=0):
        self.info = info
        self.h = h

    def __str__(self):
        if self.info[0] == 0:
            return "Malul stang: {}, {}, Barca ........ Malul drept: {}, {}".format(self.info[1], self.info[2],
                                                                                    numar_persoane - self.info[1],
                                                                                    numar_persoane - self.info[2])
        else:
            return "Malul stang: {}, {} ........ Malul drept: {}, {}, Barca".format(self.info[1], self.info[2],
                                                                                    numar_persoane - self.info[1],
                                                                                    numar_persoane - self.info[2])

    def calculeaza_euristica(self):
        if self.info[0] == 0:
            return 2 * (self.info[1] + self.info[2]) // numar_locuri_barca - 1
        else:
            return 2 * (numar_persoane + numar_persoane - self.info[1] - self.info[2]) //  numar_persoane

    def este_in_lista(self, noduri):
        for i in range(len(noduri)):
            if noduri[i].nod.info == self.info and noduri[i].nod.h == self.h:
                return i
        return None

    def __repr__(self):
        if self.info[0] == 0:
            return "Malul stang: {}, {}, Barca ........ Malul drept: {}, {}".format(self.info[1], self.info[2],
                                                                                    numar_persoane - self.info[1],
                                                                                    numar_persoane - self.info[2])
        else:
            return "Malul stang: {}, {} ........ Malul drept: {}, {}, Barca".format(self.info[1], self.info[2],
                                                                                    numar_persoane - self.info[1],
                                                                                    numar_persoane - self.info[2])


class NodParcurgere:
    def __init__(self, nod, parinte, g=0, f=None):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        if f is None:
            self.f = self.g + self.nod.h
        else:
            self.f = f

    def face_parte_din_drum(self):
        parinte = self.parinte
        while parinte is not None:
            if parinte.nod.info == self.nod.info and parinte.nod.h == self.nod.h:
                return True
            parinte = parinte.parinte
        return False

    def este_nod_scop(self, nod_scop):
        return self.nod.info == nod_scop.info

    def genereaza_succesori(self):
        lista_succesori = []
        for i in range(numar_locuri_barca+1):
            for j in range(numar_locuri_barca+1):
                if i >= j or i == 0:
                    if i+ j >= 1 and i+j <= numar_locuri_barca:
                        nod_temp = copy.deepcopy(self.nod.info)
                        if nod_temp[0] == 0:
                            start_misionari = nod_temp[1] - i
                            start_canibali = nod_temp[2] - j
                            end_misionari = numar_persoane - nod_temp[1] + i
                            end_canibali = numar_persoane - nod_temp[2] + j
                        else:
                            start_misionari = nod_temp[1] + i
                            start_canibali = nod_temp[2] + j
                            end_misionari = numar_persoane - nod_temp[1] - i
                            end_canibali = numar_persoane - nod_temp[2] - j

                        if(start_misionari >= start_canibali or start_misionari == 0) and (end_misionari >= end_canibali or end_misionari == 0):
                            nod_temp[0] = 1 - nod_temp[0]
                            nod_temp[1] = start_misionari
                            nod_temp[2] = start_canibali
                            nod_nou = Nod(nod_temp)
                            nod_nou.h = nod_nou.calculeaza_euristica()
                            succesor = NodParcurgere(nod_nou, self, self.g+1, self.g+1+nod_nou.h)
                            lista_succesori.append(succesor)
        return lista_succesori



class Problema:
    def __init__(self, nod_start, nod_scop):
        self.nod_start = nod_start
        self.nod_scop = nod_scop


    def a_star(self):
        open = []
        closed = []
        open.append(NodParcurgere(self.nod_start, None, 0, 0))
        drum_gasit = False
        while len(open) > 0:
            nod_actual = open.pop(0)
            closed.append(nod_actual)
            #print(nod_actual.nod)

            if nod_actual.este_nod_scop(nod_scop):
                drum_gasit = True
                parinte = nod_actual
                while parinte is not None:
                    print(parinte.nod)
                    parinte = parinte.parinte
                break

            lista_succesori = nod_actual.genereaza_succesori()
            for succesor in lista_succesori:
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

        if drum_gasit == False:
            print("Imposibil")


if __name__ == "__main__":
    nod_start = Nod([0, numar_persoane, numar_persoane])
    nod_scop = Nod([1, 0, 0])
    problema_can_mis = Problema(nod_start, nod_scop)
    start = timer()
    problema_can_mis.a_star()
    end = timer()
    print("Timpul de executie: {}".format(end - start))