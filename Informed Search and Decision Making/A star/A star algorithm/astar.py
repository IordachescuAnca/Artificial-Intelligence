import math
from timeit import default_timer as timer

class Nod:
    def __init__(self, info, h=math.inf):
        self.info = info
        self.h = h

    def este_in_lista(self, noduri):
        for i in range(len(noduri)):
            if noduri[i].nod.info == self.info and noduri[i].nod.h == self.h:
                return i
        return None

    def __str__(self):
        return "(info: {}, h: {})".format(self.info, self.h)

    def __repr__(self):
        return "(info: {}, h: {})".format(self.info, self.h)


class Arc:
    def __init__(self, nod1, nod2, cost):
        self.nod1 = nod1
        self.nod2 = nod2
        self.cost = cost

    def __str__(self):
        return "(Costul de la nodul {} la nodul {}: {})".format(self.nod1, self.nod2, self.cost)

    def __repr__(self):
        return "(Costul de la nodul {} la nodul {}: {})".format(self.nod1, self.nod2, self.cost)


class NodParcurgere:
    def __init__(self, nod, parinte=None, g=0, f=math.inf):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = f

    def este_nod_scop(self, nod_scop):
        return self.nod.info == nod_scop.info

    def genereaza_succesori(self, arce, noduri):
        lista_succesori = []
        for arc in arce:
            if arc.nod1 == self.nod.info:
                for nod in noduri:
                    if arc.nod2 == nod.info:
                        if self.f == math.inf:
                            lista_succesori.append(NodParcurgere(nod, self, arc.cost, arc.cost + nod.h))
                        else:
                            lista_succesori.append(
                                NodParcurgere(nod, self, self.g + arc.cost, self.g + arc.cost + nod.h))
                        break
        return lista_succesori

    def face_parte_din_drum(self):
        parinte = self.parinte
        while parinte is not None:
            if parinte.nod.info == self.nod.info and parinte.nod.h == self.nod.h:
                return True
            parinte = parinte.parinte
        return False

    def __str__(self):
        return "(nod: {}, parinte: {}, g: {}, f: {})".format(self.nod,
                                                             self.parinte if self.parinte is None else self.parinte.nod.info,
                                                             self.g, self.f)

    def __repr__(self):
        return "(nod: {}, parinte: {}, g: {}, f: {})".format(self.nod,
                                                             self.parinte if self.parinte is None else self.parinte.nod.info,
                                                             self.g, self.f)


class Problema:
    def __init__(self):
        self.noduri = []
        self.arce = []
        self.nod_start = None
        self.nod_scop = None

    def citire_date_noduri(self, path_file):
        fisier_intrare_noduri = open(path_file, "r")
        numar_noduri = int(fisier_intrare_noduri.readline())
        for _ in range(numar_noduri):
            info, h = fisier_intrare_noduri.readline().split()
            if h == "inf":
                nod_nou = Nod(info, math.inf)
            else:
                nod_nou = Nod(info, int(h))
            self.noduri.append(nod_nou)

        info_start, h_start = fisier_intrare_noduri.readline().split()
        self.nod_start = Nod(info_start, math.inf)

        info_scop, h_scop = fisier_intrare_noduri.readline().split()
        self.nod_scop = Nod(info_scop, int(h_scop))
        fisier_intrare_noduri.close()

    def citire_date_arce(self, path_file):
        fisier_intrare_arce = open(path_file, "r")
        numar_arce = int(fisier_intrare_arce.readline())
        for _ in range(numar_arce):
            nod1, nod2, cost = fisier_intrare_arce.readline().split()
            arc_nou = Arc(nod1, nod2, int(cost))
            self.arce.append(arc_nou)
        fisier_intrare_arce.close()

    def citire_date(self, path_file_noduri, path_file_arce):
        self.citire_date_noduri(path_file_noduri)
        self.citire_date_arce(path_file_arce)

    def a_star(self):
        open = []
        closed = []
        open.append(NodParcurgere(self.nod_start))

        while len(open) > 0:
            nod_curent = open.pop(0)
            closed.append(nod_curent)

            if nod_curent.este_nod_scop(self.nod_scop):
                drum = []
                while nod_curent is not None:
                    drum.append(nod_curent)
                    nod_curent = nod_curent.parinte
                drum.reverse()
                print(drum)
                break

            succesori_nod_curent = nod_curent.genereaza_succesori(self.arce, self.noduri)
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
    problema = Problema()
    problema.citire_date("noduri.txt", "arce.txt")
    start = timer()
    problema.a_star()
    end = timer()
    print("Timpul de executie: {}".format(end - start))
