from timeit import default_timer as timer

coloana = 6


class Nod:
    """Un obiect de tip Nod contine numele copilului
       si costul estimat de la nodul curent la nodul scop(h)"""

    def __init__(self, copil, h=0):
        self.copil = copil
        self.h = h

    def __str__(self):
        return "({}, h: {})".format(self.copil, self.h)

    def __repr__(self):
        return "({}, h: {})".format(self.copil, self.h)

    def determina_euristica_manhattan(self, nod_final):
        """
            Euristica folosind distanta Manhattan
            Deoarece biletelul poate fi trimis doar de la o persoana la alta si doar in 4 directii,
            scenariul optim ar fi ca biletelul de la copilul care-l transmite la cel la care trebuie
            sa ajunga sa strabata o cale libera(fara copii certati, locuri libere). Numarul de mutari optim
            pentru a rezolva problema este cel putin mai mare sau egal decat lungimea calei descrise anterior
            deoarece se poate sa nu existe o cale libera pana la nodul scop datorita nodurilor unde copii
            sunt certati sau unde locurile sunt libere. Astfel euristica este admisibila
        """
        rand_self, coloana_self = pozitii_copii[self.copil]
        rand_nod_final, coloana_nod_final = pozitii_copii[nod_final.copil]
        return abs(rand_self - rand_nod_final) + abs(coloana_self - coloana_nod_final)

    def determina_euristica_euclidiana(self, nod_final):
        """
            Euristica folosind distanta euclidiana
            Aceasta euristica este admisibila deoarece reda lungimea(aproximativ)a caii de la nod start la
            nod scop mergand pe diagonala, care nu supraestimeaza numarul de mutari optim pentru a rezolva problema,
            aceasta fiind o subevaluare a euristicii manhattan
        """
        rand_self, coloana_self = pozitii_copii[self.copil]
        rand_nod_final, coloana_nod_final = pozitii_copii[nod_final.copil]
        return (rand_self - rand_nod_final) ** 2 + (coloana_self - coloana_nod_final) ** 2

    def determina_euristica_neadmisibila(self, nod_final):
        rand_self, coloana_self = pozitii_copii[self.copil]
        rand_nod_final, coloana_nod_final = pozitii_copii[nod_final.copil]
        if rand_self == rand_nod_final and coloana_self == coloana_nod_final:
            return 0
        return coloana * rand * rand + (0 if coloana_self % 2 == 0 else - (coloana - rand_self) * coloana_self)

    def este_nod_scop(self, nod_final):
        """
            Functia de testare a scopului care verifica
            daca numele copilului al nodului curent este
            egal cu numele copilului al nodului dat ca parametru
        """
        return self.copil == nod_final.copil

    def este_in_lista(self, noduri):
        """
            Functie care returneaza pozitia nodului intr-o lista de noduri
        """
        for i in range(len(noduri)):
            if noduri[i].nod.copil == self.copil:
                return i
        return None


class NodParcurgere:
    """Un obiect de tip NodParcurgere contine un nod, parintele
       nodului curent, costul de la nodul start la nodul curent(g),
       costul estimat al unui drum, semn care indica simbolul care
       face trecerea de la pozitia copilului din nodul parinte si
       pozitia copilului din nodul curent"""

    def __init__(self, nod, parinte=None, g=0, f=None, semn=None):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.semn = semn
        if f is None:
            self.f = self.g + self.nod.h
        else:
            self.f = f

    def __str__(self):
        return "(nod: {}, parinte: {}, g: {}, f: {})".format(self.nod,
                                                             self.parinte if self.parinte is None else self.parinte.nod,
                                                             self.g, self.f)

    def __repr__(self):
        return "(nod: {}, parinte: {}, g: {}, f: {})".format(self.nod,
                                                             self.parinte if self.parinte is None else self.parinte.nod,
                                                             self.g, self.f)

    def genereaza_succesori(self, nod_final, euristica):
        """ Functia genereaza succesorii nodurilor ai caror copii se afla
            in fata si in spatele copilului din nodul actual(daca acestia exista),
            daca copilul din nodul actual se afla pe coloane impare genereaza succesorul
            care va contine copilul vecin din stanga, daca copilul din nodul actual se afla
            pe coloane pare genereaza succesorul care va contine copilul vecin din dreapta.
            In plus, daca copilul din nodul actual se afla in penultima/ultima banca,
            daca se afla pe coloane impare genereaza succesorul care va contine copilul vecin
            din dreapta(daca exista) sau daca se afla pe coloane pare genereaza succesorul
            care va contine copilul vecin din stanga. - numerotarea coloanelor incepe de la 0."""

        lista_succesori = []
        rand_self, coloana_self = pozitii_copii[self.nod.copil]

        if rand_self - 1 >= 0:
            copil_succesor = nume_copii[(rand_self - 1, coloana_self)]
            if copil_succesor != "liber" and not (
                    self.nod.copil in copii_certati and copil_succesor in copii_certati[self.nod.copil]):
                succesor = self.configureaza_succesor(copil_succesor, nod_final, euristica)
                succesor.semn = "^"
                lista_succesori.append(succesor)

        if rand_self + 1 < rand:
            copil_succesor = nume_copii[(rand_self + 1, coloana_self)]
            if copil_succesor != "liber" and not (
                    self.nod.copil in copii_certati and copil_succesor in copii_certati[self.nod.copil]):
                succesor = self.configureaza_succesor(copil_succesor, nod_final, euristica)
                succesor.semn = "v"
                lista_succesori.append(succesor)

        if coloana_self % 2 == 0:
            copil_succesor = nume_copii[(rand_self, coloana_self + 1)]
            if copil_succesor != "liber" and not (
                    self.nod.copil in copii_certati and copil_succesor in copii_certati[self.nod.copil]):
                succesor = self.configureaza_succesor(copil_succesor, nod_final, euristica)
                succesor.semn = ">"
                lista_succesori.append(succesor)

        if coloana_self % 2 == 1:
            copil_succesor = nume_copii[(rand_self, coloana_self - 1)]
            if copil_succesor != "liber" and not (
                    self.nod.copil in copii_certati and copil_succesor in copii_certati[self.nod.copil]):
                succesor = self.configureaza_succesor(copil_succesor, nod_final, euristica)
                succesor.semn = "<"
                lista_succesori.append(succesor)

        if rand_self + 2 >= rand:
            if coloana_self % 2 == 1 and coloana_self != coloana - 1:
                copil_succesor = nume_copii[(rand_self, coloana_self + 1)]
                if copil_succesor != "liber" and not (
                        self.nod.copil in copii_certati and copil_succesor in copii_certati[self.nod.copil]):
                    succesor = self.configureaza_succesor(copil_succesor, nod_final, euristica)
                    succesor.semn = ">>"
                    lista_succesori.append(succesor)

            if coloana_self % 2 == 0 and coloana_self != 0:
                copil_succesor = nume_copii[(rand_self, coloana_self - 1)]
                if copil_succesor != "liber" and not (
                        self.nod.copil in copii_certati and copil_succesor in copii_certati[self.nod.copil]):
                    succesor = self.configureaza_succesor(copil_succesor, nod_final, euristica)
                    succesor.semn = "<<"
                    lista_succesori.append(succesor)

        return lista_succesori

    def configureaza_succesor(self, copil_succesor, nod_final, euristica):
        """
            Creeaza un NodParcurgere folosind una din cele 3 euristici
        """
        nod_succesor = Nod(copil_succesor)
        if euristica == 1:
            nod_succesor.h = nod_succesor.determina_euristica_manhattan(nod_final)
        elif euristica == 2:
            nod_succesor.h = nod_succesor.determina_euristica_euclidiana(nod_final)
        elif euristica == 3:
            nod_succesor.h = nod_succesor.determina_euristica_neadmisibila(nod_final)
        succesor = NodParcurgere(nod_succesor, self, self.g + 1, self.g + 1 + nod_succesor.h)
        return succesor

    def face_parte_din_drum(self):
        """
            Verifica daca nod face parte din drumul de la radacina pana la nod
        """
        parinte = self.parinte
        while parinte is not None:
            if parinte.nod.copil == self.nod.copil:
                return True
            parinte = parinte.parinte
        return False


class Problema:
    def __init__(self, nod_inceput, nod_scop):
        """
        Problema este definita de nodul de inceput(din care incepe cautarea)
        si nodul scop, cu ajutorul caruia putem apela functia de testare
        este_nod_scop(nod_scop)
        """
        self.nod_inceput = nod_inceput
        self.nod_scop = nod_scop

    def verifica_existenta_solutie_inceput(self):  # optimizare
        rand_copil_scop, coloana_copil_scop = pozitii_copii[self.nod_scop.copil]

        copil_sus = ""
        copil_jos = ""
        copil_vecin = ""
        if rand_copil_scop - 1 >= 0:
            copil_sus = nume_copii[(rand_copil_scop - 1, coloana_copil_scop)]
        if rand_copil_scop + 1 < coloana:
            copil_jos = nume_copii[(rand_copil_scop + 1, coloana_copil_scop)]
        if coloana_copil_scop % 2 == 1:
            copil_vecin = nume_copii[(rand_copil_scop, coloana_copil_scop - 1)]
        else:
            copil_vecin = nume_copii[(rand_copil_scop, coloana_copil_scop + 1)]

        if copil_sus == "liber" and  copil_jos == "liber" and copil_vecin == "liber":
            return False

        if copil_sus in copii_certati and copil_jos in copii_certati and copil_vecin in copii_certati:
            if copil_sus in copii_certati[self.nod_scop.copil] and copil_jos in copii_certati[self.nod_scop.copil] and copil_vecin in copii_certati[self.nod_scop.copil]:
                return False

        return True

    def a_star(self, euristica):
        if not self.verifica_existenta_solutie_inceput():
            fisier_ouput.write("Nu exista solutie!(Optimizare)")
            return
        open = []
        closed = []
        open.append(NodParcurgere(self.nod_inceput, None, 0, 0))
        are_solutie = False
        while len(open) > 0:
            nod_curent = open.pop(0)
            closed.append(nod_curent)

            if nod_curent.nod.este_nod_scop(self.nod_scop):
                are_solutie = True
                drum = []
                while nod_curent is not None:
                    drum.append(nod_curent)
                    nod_curent = nod_curent.parinte
                drum.reverse()
                for nod_parcurgere in drum:
                    if nod_parcurgere.semn is not None:
                        fisier_ouput.write(nod_parcurgere.semn + " ")
                    fisier_ouput.write(nod_parcurgere.nod.copil + " ")
                break

            lista_succesori = nod_curent.genereaza_succesori(self.nod_scop, euristica)
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
        if not are_solutie:
            fisier_ouput.write("Nu exista solutie")


if __name__ == "__main__":
    nume_fisier_input = input("Fisier de intrare: ")
    fisier_intare = open(nume_fisier_input, "r")

    pozitii_copii = {}
    nume_copii = {}

    rand = 0
    while True:
        copii = fisier_intare.readline().split()
        if copii[0] == "suparati":
            break
        for index in range(len(copii)):
            pozitii_copii[copii[index]] = (rand, index)
            nume_copii[(rand, index)] = copii[index]
        rand += 1

    copii_certati = {}
    while True:
        copii = fisier_intare.readline().split()
        if copii[0] == "mesaj:":
            break

        if copii[0] not in copii_certati:
            copii_certati[copii[0]] = []
        copii_certati[copii[0]].append(copii[1])

        if copii[1] not in copii_certati:
            copii_certati[copii[1]] = []
        copii_certati[copii[1]].append(copii[0])

    copil_inceput = copii[1]
    nod_inceput = Nod(copil_inceput)

    copil_final = copii[3]
    nod_scop = Nod(copil_final)

    nume_fisier_output = "output.txt"
    fisier_ouput = open(nume_fisier_output, "w")

    problema = Problema(nod_inceput, nod_scop)
    # 1 - euristica cu distanta Manhattan, 2 - euristica cu distanta euclidiana, 3 - euristica neadmisibila
    euristica = int(input("Alege euristica: "))
    start = timer()
    problema.a_star(euristica)
    end = timer()
    fisier_ouput.write("\nTimpul de executie: {}".format(end - start))
    fisier_ouput.close()
