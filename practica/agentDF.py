import random

from practica import joc
from practica.estat import Estat
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__per_visitar = None
        self.__visitats = None
        self.__cami_exit = None
    
    # cerca per profunditat
    def cerca(self, estat_inicial: Estat) -> bool:
        self.__per_visitar = []
        self.__visitats = set() 
        exit = False

        self.__per_visitar.append(estat_inicial)
        while self.__per_visitar:
            estat_actual = self.__per_visitar.pop(-1)

            if estat_actual in self.__visitats:
                continue

            if estat_actual.es_meta():
                break

            self.__visitats.add(estat_actual)

            for f in estat_actual.genera_fill():
                if f not in self.__visitats and f not in self.__per_visitar:  # Evitar duplicados en per_visitar
                    self.__per_visitar.append(f)

        if estat_actual.es_meta():
            self.__cami_exit = estat_actual.accions_previes
            exit = True
        
        print(f"Camí exit: {self.__visitats}")
        return exit

    
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
            print(f"Estados{estat_inicial.__str__()}")
            print(f"DESTINO: {percepcio["DESTI"]}")

            self.cerca(estat_inicial)

        if self.__cami_exit:
            return self.__cami_exit.pop(0)
        else:
            return Accions.ESPERAR
    
