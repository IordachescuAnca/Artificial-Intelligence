import copy

dimensiune = 3

class Nod:
    def __init__(self, info, h=0):
        self.info = [int(value) for value in info]
        self.h = h

    def __str__(self):
        str_output = ""
        for i in range(dimensiune):
            for j in range(dimensiune):
                str_output += (str(self.info[i * dimensiune + j]) if self.info[i * dimensiune + j] != 0 else "-") + " "
            str_output += "\n"
        return str_output

    def __repr__(self):
        str_output = ""
        for i in range(dimensiune):
            for j in range(dimensiune):
                str_output += (str(self.info[i * dimensiune + j]) if self.info[i * dimensiune + j] != 0 else "-") + " "
            str_output += "\n"
        return str_output

    def este_nod_scop(self, nod):
        return self.info == nod.info

    def calculeaza_euristica(self, nod_scop):
        misplaced_tiles = 0
        for i in range(len(self.info)):
            if self.info[i] != 0 and self.info[i] != nod_scop.info[i]:
                misplaced_tiles += 1
        return misplaced_tiles

    def determina_pozitie_0(self):
        for i in range(len(self.info)):
            if self.info[i] == 0:
                return i

    def este_in_lista(self, noduri):
        for i in range(len(noduri)):
            if noduri[i].nod.info == self.info:
                return i
        return None

    def determina_numar_inversiuni(self):
        numar_inversiuni = 0;
        for i in range(len(self.info)):
            for j in range(i+1, len(self.info)):
                if self.info[i] > self.info[j] != 0:
                    numar_inversiuni += 1
        return numar_inversiuni


class NodParcurgere:
    def __init__(self, nod, parinte = None, g = 0, f = None):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        if f is None:
            self.f = self.g + self.nod.h
        else:
            self.f = f

    def genereaza_succesori(self, nod_scop):
        lista_succesori = []
        pozitie_0 = self.nod.determina_pozitie_0()
        rand = pozitie_0 // dimensiune
        coloana = pozitie_0 % dimensiune

        if rand - 1 >= 0:
            info_temp = copy.deepcopy(self.nod.info)
            info_temp[rand * dimensiune + coloana], info_temp[(rand - 1) * dimensiune + coloana] = info_temp[(rand - 1)* dimensiune + coloana], info_temp[rand * dimensiune + coloana]
            nod = Nod(info_temp)
            nod.h = nod.calculeaza_euristica(nod_scop)
            succesor = NodParcurgere(nod, self, self.g+1, self.g+1+nod.h)
            lista_succesori.append(succesor)

        if rand + 1 < dimensiune:
            info_temp = copy.deepcopy(self.nod.info)
            info_temp[rand * dimensiune + coloana], info_temp[(rand + 1) * dimensiune + coloana] = info_temp[(rand + 1) * dimensiune + coloana], info_temp[rand * dimensiune + coloana]
            nod = Nod(info_temp)
            nod.h = nod.calculeaza_euristica(nod_scop)
            succesor = NodParcurgere(nod, self, self.g + 1, self.g + 1 + nod.h)
            lista_succesori.append(succesor)

        if coloana - 1 >= 0:
            info_temp = copy.deepcopy(self.nod.info)
            info_temp[rand * dimensiune + coloana], info_temp[rand * dimensiune + coloana - 1] = info_temp[rand * dimensiune + coloana - 1], info_temp[rand * dimensiune + coloana]
            nod = Nod(info_temp)
            nod.h = nod.calculeaza_euristica(nod_scop)
            succesor = NodParcurgere(nod, self, self.g + 1, self.g + 1 + nod.h)
            lista_succesori.append(succesor)

        if coloana + 1 < dimensiune:
            info_temp = copy.deepcopy(self.nod.info)
            info_temp[rand * dimensiune + coloana], info_temp[rand * dimensiune + coloana + 1] = info_temp[rand * dimensiune + coloana + 1], info_temp[rand * dimensiune + coloana]
            nod = Nod(info_temp)
            nod.h = nod.calculeaza_euristica(nod_scop)
            succesor = NodParcurgere(nod, self, self.g + 1, self.g + 1 + nod.h)
            lista_succesori.append(succesor)

        return lista_succesori

    def face_parte_din_drum(self):
        parinte = self.parinte
        while parinte is not None:
            if parinte.nod.info == self.nod.info and parinte.nod.h == self.nod.h:
                return True
            parinte = parinte.parinte
        return False


class Problema:
    def __init__(self, nod_start = None, nod_scop = None):
        self.nod_start = nod_start
        self.nod_scop = nod_scop

    def citire_date(self, path_file):
        fisier_intare = open(path_file, "r")
        start_state = fisier_intare.readline().split()
        goal_state = fisier_intare.readline().split()
        self.nod_scop = Nod(goal_state)
        self.nod_start = Nod(start_state)
        self.nod_start.h = self.nod_start.calculeaza_euristica(self.nod_scop)

    def a_star(self):
        if self.nod_start.determina_numar_inversiuni() % 2 == 1:
            print("Nu exista solutie")
            return
        open = []
        closed = []
        open.append(NodParcurgere(self.nod_start, None, 0, self.nod_start.h))

        while len(open) > 0:
            nod_curent = open.pop(0)
            closed.append(nod_curent)
            #print(nod_curent.nod)

            if nod_curent.nod.este_nod_scop(self.nod_scop):
                drum = []
                while nod_curent is not None:
                    drum.append(nod_curent)
                    nod_curent = nod_curent.parinte
                drum.reverse()
                for parte in drum:
                    print(parte.nod)
                break

            lista_succesori = nod_curent.genereaza_succesori(self.nod_scop)
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


a = Problema()
a.citire_date("eightpuzzle.txt")
a.a_star()