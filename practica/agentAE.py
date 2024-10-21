import random
from queue import PriorityQueue

from practica import joc
from practica.estat import Estat
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__cami_exit = None
        
    # cerca per A*
    def cerca(self, estat_inicial):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_heuristica(), estat_inicial))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.genera_fill()

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calc_heuristica(), estat_f))

            self.__tancats.add(actual)

        if actual.es_meta():
            self.__cami_exit = actual.accions_previes

    
    def pinta(self, percepcio: dict):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, (int, int)]:
        if self.__cami_exit is None:
            estat_inicial = Estat(
                self.posicio,
                percepcio["PARETS"], 
                percepcio["DESTI"],
                0
            )

            self.cerca(estat_inicial)

        if self.__cami_exit:
            return self.__cami_exit.pop(0)
        else:
            return Accions.ESPERAR
    
