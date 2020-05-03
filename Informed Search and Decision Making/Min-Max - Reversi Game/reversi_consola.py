import copy
import time

di = [0, 0, 1, -1, 1, 1, -1, -1]
dj = [1, -1, 0, 0, 1, -1, 1, -1]

ADANCIME_MAX = 0

weights =[[100, -20, 10, 5, 5, 10, -20, 100],
          [-20, -50, -2, -2, -2, -2, -50, -20],
          [10, -2, -1, -1, -1, -1, -2, 10],
          [5, -2, -1, -1, -1, -1, -2, 5],
          [5, -2, -1, -1, -1, -1, -2, 5],
          [10, -2, -1, -1, -1, -1, -2, 10],
          [-20, -50, -2, -2, -2, -2, -50, -20],
          [100, -20, 10, 5, 5, 10, -20, 100]]

class Joc:
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    GOL = "#"

    def __init__(self, tabla=None):
        if tabla is None:
            self.tabla = [["#" for _ in range(self.__class__.NR_COLOANE)] for _ in range(self.__class__.NR_COLOANE)]
            self.tabla[3][3] = self.tabla[4][4] = 'a'
            self.tabla[3][4] = self.tabla[4][3] = 'n'
        else:
            self.tabla = tabla

    def final(self):
        """Verific daca niciun jucator nu mai poate face vreo mutare(astfel este pass pentru ambii),
        daca tabla este formata doar din goluri sau piese de ale unui singur jucator sau daca tabla nu mai contine
        niciun gol. Daca tabla se afla intr-unul dintre aceste cazuri, inseamna ca s-a terminat jocul. Altfel, nu este
        finalul jocului."""
        if len(self.mutari_indici(self.__class__.JMIN)) == 0 and len(self.mutari_indici(self.__class__.JMAX)) == 0:
            return "Pass"

        seen_gol = 0
        seen_jmin = 0
        seen_jmax = 0
        for rand in self.tabla:
            for simbol in rand:
                if simbol == self.__class__.GOL:
                    seen_gol = 1
                elif simbol == self.__class__.JMIN:
                    seen_jmin = 1
                elif simbol == self.__class__.JMAX:
                    seen_jmax = 1

        if seen_gol + seen_jmin <= 2 and seen_jmax == 0:
            return self.__class__.JMIN

        if seen_gol + seen_jmax <= 2 and seen_jmin == 0:
            return self.__class__.JMAX

        for rand in self.tabla:
            if self.__class__.GOL in rand:
                return False

        contor_jmin = 0
        contor_jmax = 0
        for rand in self.tabla:
            for simbol in rand:
                if simbol == self.__class__.JMIN:
                    contor_jmin += 1
                if simbol == self.__class__.JMAX:
                    contor_jmax += 1

        if contor_jmin > contor_jmax:
            return self.__class__.JMIN
        elif contor_jmax > contor_jmin:
            return self.__class__.JMAX
        else:
            return "remiza"

    def __eq__(self, other):
        return self.tabla == other.tabla

    def mutari(self, jucator):
        """Genereaza toate mutarile posibile ale jucatorului curent avand configuratia tablei data"""
        lista_mutari = []
        for rand in range(self.__class__.NR_COLOANE):
            for coloana in range(self.__class__.NR_COLOANE):
                for i in range(self.__class__.NR_COLOANE):
                    mutare_valida = self.este_mutare_valida(self.tabla, rand, coloana, jucator, i)
                    if mutare_valida:
                        tabla_temp = copy.deepcopy(self.tabla)
                        tabla_succesor = self.modifica_tabla(tabla_temp, rand, coloana, jucator)
                        este_in_lista = False
                        for mutare in lista_mutari:
                            if mutare == Joc(tabla_succesor):
                                este_in_lista = True

                        if not este_in_lista:
                            lista_mutari.append(Joc(tabla_succesor))

        return lista_mutari

    def mutari_indici(self, jucator):
        """Genereaza pozitiile pe care poate jucatorul curent sa puna piesa"""
        lista_indici = []
        for rand in range(self.__class__.NR_COLOANE):
            for coloana in range(self.__class__.NR_COLOANE):
                for i in range(self.__class__.NR_COLOANE):
                    mutare_valida = self.este_mutare_valida(self.tabla, rand, coloana, jucator, i)
                    if mutare_valida:
                        lista_indici.append((rand, coloana))
        return lista_indici

    def scor(self):
        """Calculeaza scorul(numarul de piese) pentru ambii jucatori"""
        contor_jmax = 0
        contor_jmin = 0
        for rand in range(self.__class__.NR_COLOANE):
            for coloana in range(self.__class__.NR_COLOANE):
                if self.tabla[rand][coloana] == self.__class__.JMIN:
                    contor_jmin += 1
                if self.tabla[rand][coloana] == self.__class__.JMAX:
                    contor_jmax += 1
        return contor_jmin, contor_jmax

    def modifica_tabla(self, tabla, rand, coloana, jucator):
        """Adaugam pe tabla piesa jucatorului curent pe (rand, coloana) si adaugam piese pt jucatorul curent/eliminam
        piesele adversarului daca este necesar verificand pe toate directiile"""
        for i in range(self.__class__.NR_COLOANE):
            mutare_valida = self.este_mutare_valida(tabla, rand, coloana, jucator, i)
            if mutare_valida:
                rand_temp = rand - di[i]
                coloana_temp = coloana - dj[i]
                jucator_opus = "a" if jucator == "n" else "n"
                while 0 <= rand_temp < self.__class__.NR_COLOANE and 0 <= coloana_temp < self.__class__.NR_COLOANE:
                    if tabla[rand_temp][coloana_temp] == jucator:
                        break
                    if tabla[rand_temp][coloana_temp] == jucator_opus:
                        tabla[rand_temp][coloana_temp] = jucator
                    rand_temp -= di[i]
                    coloana_temp -= dj[i]
        tabla[rand][coloana] = jucator
        return tabla

    def este_mutare_valida(self, tabla, rand, coloana, jucator, i):
        """Verificam daca pe pozitia rand, coloana putem sa punem piesa pentru jucator avand in vedere directia i"""
        if tabla[rand][coloana] != self.__class__.GOL:
            return False
        if rand - di[i] < 0 or rand - di[i] >= self.__class__.NR_COLOANE or coloana - dj[i] < 0 or coloana - dj[
            i] >= self.__class__.NR_COLOANE:
            return False
        rand_temp = rand - di[i]
        coloana_temp = coloana - dj[i]
        jucator_opus = "a" if jucator == "n" else "n"
        seen_jucator = False
        seen_jucator_opus = False

        while 0 <= rand_temp < self.__class__.NR_COLOANE and 0 <= coloana_temp < self.__class__.NR_COLOANE:
            if tabla[rand_temp][coloana_temp] == self.__class__.GOL:
                break
            if tabla[rand_temp][coloana_temp] == jucator_opus:
                seen_jucator_opus = True
            if tabla[rand_temp][coloana_temp] == jucator and seen_jucator_opus:
                seen_jucator = True
            if tabla[rand_temp][coloana_temp] == jucator and not seen_jucator_opus:
                break

            if seen_jucator and seen_jucator_opus:
                return True
            rand_temp -= di[i]
            coloana_temp -= dj[i]

        return False

    def functie_evaluare1(self):
        """Aceasta functie de evaluare se bazeaza pe pozitiile pieselor jucatorilor puse pe tabla,
        calculand o suma de produse dintre weight-ul pozitiei pe care se afla piesa si 1 daca se afla
        o piesa pe tabla cu care calculatorul joaca sau -1 daca este a jucatorului. Astfel, aplicand aceasta
        functie de evaluare in algoritmii min max si alpha beta, la nivelul "max" calculatorul o sa-si aleaga
        configuratia care-i maximizeaza pozitiile importante(precum colturile), iar la nivelul "min" o sa se
        aleaga configuratia care-i minimizeaza pozitiile importante ale calculatorului."""
        sum = 0
        for i in range(self.__class__.NR_COLOANE):
            for j in range(self.__class__.NR_COLOANE):
                if self.tabla[i][j] == self.__class__.JMIN:
                    sum -= weights[i][j]
                elif self.tabla[i][j] == self.__class__.JMAX:
                    sum += weights[i][j]

        return sum

    def functie_evaluare2(self):
        """Aceasta functie de evaluare se bazeaza pe mobilitatea jucatorilor si importanta colturilor.
        Astfel, aceasta va calcula mobilitatea jucatorului reprezentat de calculator impotriva player-ului.
        Asadar, aplicand aceasta functie de evaluare in algoritmii min max si alpha beta, la nivelul "max"
        calculatorul o sa-si aleaga configuratia care-i maximizeaza mobilititatea si accesul la colturi, iar
        la nivelul "min" o sa se aleaga configuratia care-i minimizeaza jucatorului reprezentat de calculator
         mobilitatea si accesul la colturi."""
        cornerJmax = 0
        cornerJmin = 0
        if self.tabla[0][self.__class__.NR_COLOANE - 1] == self.__class__.JMAX:
            cornerJmax += 1
        elif self.tabla[0][self.__class__.NR_COLOANE - 1] == self.__class__.JMIN:
            cornerJmin += 1

        if self.tabla[0][0] == self.__class__.JMAX:
            cornerJmax += 1
        elif self.tabla[0][0] == self.__class__.JMIN:
            cornerJmin += 1

        if self.tabla[self.__class__.NR_COLOANE - 1][0] == self.__class__.JMAX:
            cornerJmax += 1
        elif self.tabla[self.__class__.NR_COLOANE - 1][0] == self.__class__.JMIN:
            cornerJmin += 1

        if self.tabla[self.__class__.NR_COLOANE - 1][self.__class__.NR_COLOANE - 1] == self.__class__.JMAX:
            cornerJmax += 1
        elif self.tabla[self.__class__.NR_COLOANE - 1][self.__class__.NR_COLOANE - 1] == self.__class__.JMIN:
            cornerJmin += 1

        mpc = len(self.mutari_indici(self.__class__.JMAX))
        mplayer = len(self.mutari_indici(self.__class__.JMIN))
        return 10 * (cornerJmax - cornerJmin) + (mpc - mplayer) / (mpc + mplayer)

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif t_final == "remiza":
            return 0
        else:
            return self.functie_evaluare1()

    def __str__(self):
        output_str = ""
        for rand in self.tabla:
            for simbol in rand:
                output_str += simbol + " "
            output_str += "\n"
        return output_str

    def __repr__(self):
        output_str = ""
        for rand in self.tabla:
            for simbol in rand:
                output_str += simbol + " "
            output_str += "\n"
        return output_str


class Stare:
    def __init__(self, tabla_joc, j_curent, adancime=0, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent
        self.adancime = adancime
        self.scor = scor
        self.mutari_posibile = []
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")"
        return sir

    def __repr__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")"
        return sir


def min_max(stare): # verifica daca mai are succesori -> pas calculator
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare

def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        elif final == "Pass":
            print("Ambii jucatori au luat pass.\n")
            jmin_scor, jmax_scor = stare_curenta.tabla_joc.scor()
            if jmin_scor > jmax_scor:
                print("A castigat jucatorul")
            elif jmin_scor < jmax_scor:
                print("A castigat calculatorul")
            else:
                print("Remiza")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    timp_inceput_joc = int(round(time.time() * 1000))
    raspuns_valid = False
    tip_algoritm = ""
    while not raspuns_valid:
        tip_algoritm = input("Algoritm folosit? (ranspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu a sau cu n?\n").lower()
        if Joc.JMIN in ['a', 'n']:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie a sau n.")
    Joc.JMAX = 'a' if Joc.JMIN == 'n' else 'n'

    raspuns_valid = False
    while not raspuns_valid:
        dificultate = input("Dificultatea jocului: incepator, mediu, avansat\n").lower()
        if dificultate in ['incepator', 'mediu', 'avansat']:
            raspuns_valid = True
            if dificultate == 'mediu':
                ADANCIME_MAX = 4
            elif dificultate == 'avansat':
                ADANCIME_MAX = 5
            elif dificultate == 'incepator':
                ADANCIME_MAX = 2
        else:
            print("Nu exista aceasta optiune.")

    tabla_curenta = Joc()
    print("Tabla initiala")
    stare_curenta = Stare(tabla_curenta, 'n', ADANCIME_MAX)

    pass_jucator = 0
    pass_calculator = 0

    numar_mutari_jucator = 0
    numar_mutari_calculator = 0
    while True:
        print(str(stare_curenta))
        scor_jmin, scor_jmax = stare_curenta.tabla_joc.scor()
        print("\nScor jucator: %d\nScor calculator: %d" % (scor_jmin, scor_jmax))
        if stare_curenta.j_curent == Joc.JMAX:
            print("Este randul calculatorului")
        else:
            print("Este randul jucatorului")

        if afis_daca_final(stare_curenta):
            break

        if stare_curenta.j_curent == Joc.JMIN:
            if len(stare_curenta.tabla_joc.mutari_indici(stare_curenta.j_curent)) == 0:
                print("Pass pentru jucator!")
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                continue

            print("Daca vrei sa iesi din joc, scrie exit")
            t_inainte = int(round(time.time() * 1000))
            linie = input("Baga linie: ")
            coloana = input("Baga coloana: ")
            t_dupa = int(round(time.time() * 1000))
            if linie == 'exit' or coloana == 'exit':
                scor_jmin, scor_jmax = stare_curenta.tabla_joc.scor()
                print("Jucatorul a ales sa opreasca jocul")
                print("\nScor jucator: %d\nScor calculator: %d" % (scor_jmin, scor_jmax))
                break

            if linie in ['0', '1', '2', '3', '4', '5', '6', '7'] and coloana in ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                                                                                 'h']:
                linie = int(linie)
                coloana = int(ord(coloana) - ord('a'))
                if (linie, coloana) in stare_curenta.tabla_joc.mutari_indici(stare_curenta.j_curent):
                    tabla_joc_temp = copy.deepcopy(stare_curenta.tabla_joc.tabla)
                    tabla_joc_noua = Joc(tabla_joc_temp).modifica_tabla(tabla_joc_temp, linie, coloana,
                                                                        stare_curenta.j_curent)
                    stare_curenta.tabla_joc.tabla = tabla_joc_noua
                    numar_mutari_jucator += 1
                    print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                    stare_curenta.j_curent = stare_curenta.jucator_opus()
                    print("\nTabla dupa mutarea jocului")

                else:
                    if len(stare_curenta.tabla_joc.mutari_indici(stare_curenta.j_curent)) > 0:
                        print("Nu se poate pune piesa acolo.")
            else:
                print("Nu se poate pune piesa acolo")
        else:
            if len(stare_curenta.tabla_joc.mutari_indici(stare_curenta.j_curent)) == 0:
                print("Pass pentru calculator!")
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                continue

            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            numar_mutari_calculator += 1
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            stare_curenta.j_curent = stare_curenta.jucator_opus()
            print("Tabla dupa mutarea calculatorului")

    print("Numar mutari jucator %d" % numar_mutari_jucator)
    print("Numar mutari calculator %d" % numar_mutari_calculator)
    timp_sfarsit_joc = int(round(time.time() * 1000))
    print("Jocul a durat " + str(timp_sfarsit_joc - timp_inceput_joc) + " milisecunde.")


if __name__ == "__main__":
    main()
