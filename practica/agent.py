import random

from practica import joc
from practica import estat
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__proves = [
            (Accions.MOURE, "E"),
            (Accions.MOURE, "S"),
            (Accions.MOURE, "N"),
            (Accions.MOURE, "O"),
            (Accions.BOTAR, "S"),
            (Accions.BOTAR, "N"),
            (Accions.BOTAR, "E"),
            (Accions.BOTAR, "O"),
            (Accions.POSAR_PARET, "S"),
            (Accions.POSAR_PARET, "N"),
            (Accions.POSAR_PARET, "E"),
            (Accions.POSAR_PARET, "O"),

        ]
#######################################################
        self.__per_visitar = None
        self.__visitats = None
        self.__cami_exit = None
    
    # cerca per profunditat
    def cerca(self, estat_inicial: estat) -> bool:
        self.__per_visitar = []
        self.__visitats = set() #No queremos que se repian los estados
        exit = False

        self.__per_visitar.append(estat_inicial)
        while self.__per_visitar: #Mientras haya estados por visitar
            estat_actual = self.__per_visitar.pop(-1)

            if estat_actual in self.__visitats or not estat_actual._valid(estat_actual.pos_agent): #Es segur mira si es un estado válido
                continue

            if estat_actual.es_meta():
                break

            for f in estat_actual.genera_fill():
                self.__per_visitar.append(f)

            self.__visitats.add(estat_actual)

        if estat_actual.es_meta():
            self.__cami_exit = estat_actual.cami
            exit = True

        return exit
    
    def pinta(self, percepcio: dict):
        # Obtener dimensiones del tablero a partir de la matriz "TAULELL"
        taulell = percepcio["TAULELL"]
        N = len(taulell)
        M = len(taulell[0]) if N > 0 else 0

        # Crear un array unidimensional con N * M elementos, inicialmente vacíos (" ")
        display_taulell = [" " for _ in range(N * M)]

        # Función para convertir coordenadas 2D (x, y) a índice 1D
        def convertir_a_indice(x, y):
            return y * M + x

        # Colocar las paredes (representadas por "#")
        for (x, y) in percepcio["PARETS"]:
            display_taulell[convertir_a_indice(x, y)] = "#"

        # Colocar el objetivo (representado por "X")
        desti_x, desti_y = percepcio["DESTI"]
        display_taulell[convertir_a_indice(desti_x, desti_y)] = "X"

        # Colocar los agentes (representados por "A" y un índice si hay varios)
        for agent_name, (agent_x) in percepcio["AGENTS"].items():
            display_taulell[convertir_a_indice(agent_x)] = "A"  # Personalizable si hay varios agentes

        # Imprimir el tablero como N filas
        print("Tauler de joc:")
        for i in range(N):
            fila = display_taulell[i * M:(i + 1) * M]  # Extraer una fila del array unidimensional
            print(" ".join(fila))
        print("\n")  # Separar por claridad


    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        # Si no se ha encontrado un camino aún, inicializa el estado y busca el camino.
        if self.__cami_exit is None:
            # Obtener la posición del agente desde "AGENTS"
            pos_agent = percepcio["AGENTS"].get("Agent 1")
            
            # Verificar que la posición del agente exista en "AGENTS"
            if pos_agent is None:
                raise ValueError("Posición del agente no encontrada en percepcio['AGENTS']")
            
            estat_inicial = estat.Estat(
                pos_agent=pos_agent,  # Usar la posición obtenida del diccionario "AGENTS"
                parets=percepcio["PARETS"],
                desti=percepcio["DESTI"]
            )
            
            # Llamar al método cerca para buscar el camino desde el estado inicial
            if not self.cerca(estat_inicial):
                # Si no encuentra una solución, no hace nada y espera
                return Accions.ESPERAR
        
        # Si hay un camino, ejecuta el siguiente paso del camino.
        if self.__cami_exit:
            # Tomar la siguiente acción del camino.
            accio, direccio = self.__cami_exit.pop(0)  # Desencolar la siguiente acción
            return accio, direccio
        else:
            # Si no hay más acciones en el camino, espera
            return Accions.ESPERAR

