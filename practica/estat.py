import copy
import itertools

from practica.joc import Accions

class Estat:
    # Costos de cada acción
    COST_MOVIMENT = 1
    COST_BOTAR = 2
    COST_POSAR_PARET = 3
    midaN = 6
    midaM = 6

    # Movimientos posibles: (Dirección, dx, dy)
    MOVIMENTS = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'O': (-1, 0)
    }

    def __init__(self, pos_agent, parets, desti, cami=None):
        if cami is None:
            cami = []
        self.pos_agent = pos_agent  # Posición actual del agente
        self.parets = parets  # Lista de coordenadas con paredes
        self.desti = desti  # Coordenadas de la meta
        self.cami = cami  # Lista de acciones tomadas hasta ahora

    def __hash__(self):
        return hash((self.pos_agent, tuple(self.parets)))

    def __eq__(self, other):
        return self.pos_agent == other.pos_agent and self.parets == other.parets

    def _valid(self, posicio):
        """Verifica si una posición es válida (no está fuera de límites ni tiene una pared)."""
        x, y = posicio
        if not (0 <= x < self.midaN and 0 <= y < self.midaM):
            return False
        if posicio in self.parets:
            return False
        return True

    def es_meta(self):
        """Comprueba si el agente ha llegado al objetivo."""
        return self.pos_agent == self.desti

    def moure(self, direccio):
        """Genera un nuevo estado moviéndose en una dirección (si es posible)."""
        dx, dy = self.MOVIMENTS[direccio]
        nova_pos = (self.pos_agent[0] + dx, self.pos_agent[1] + dy)
        if self._valid(nova_pos):
            nou_estat = copy.deepcopy(self)
            nou_estat.pos_agent = nova_pos
            nou_estat.cami.append((Accions.MOURE, direccio))
            return nou_estat
        return None

    def botar(self, direccio):
        """Genera un nuevo estado saltando dos posiciones en una dirección (si es posible)."""
        dx, dy = self.MOVIMENTS[direccio]
        nova_pos = (self.pos_agent[0] + 2 * dx, self.pos_agent[1] + 2 * dy)
        if self._valid(nova_pos):
            nou_estat = copy.deepcopy(self)
            nou_estat.pos_agent = nova_pos
            nou_estat.cami.append((Accions.BOTAR, direccio))
            return nou_estat
        return None

    def posar_paret(self, direccio):
        """Genera un nuevo estado colocando una pared en una casilla adyacente (si es posible)."""
        dx, dy = self.MOVIMENTS[direccio]
        nova_pos = (self.pos_agent[0] + dx, self.pos_agent[1] + dy)
        if self._valid(nova_pos) and nova_pos not in self.parets:
            nou_estat = copy.deepcopy(self)
            nou_estat.parets.add(nova_pos)
            nou_estat.cami.append((Accions.POSAR_PARET, direccio))
            return nou_estat
        return None

    def genera_fill(self):
        """Genera todos los posibles estados hijos (movimientos posibles)."""
        estats_generats = []
        
        # Intentar moverse en todas las direcciones
        for direccio in self.MOVIMENTS:
            nou_estat_moure = self.moure(direccio)
            if nou_estat_moure:
                estats_generats.append(nou_estat_moure)
            
            nou_estat_botar = self.botar(direccio)
            if nou_estat_botar:
                estats_generats.append(nou_estat_botar)
                
            #nou_estat_paret = self.posar_paret(direccio)
            #if nou_estat_paret:
                #estats_generats.append(nou_estat_paret)
                
        return estats_generats

    def __str__(self):
        return (f"Posició agent: {self.pos_agent} | Paredes: {self.parets} | "
                f"Camí: {self.cami}")

