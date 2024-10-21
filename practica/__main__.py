import sys
sys.path.append("C:/Users/laura/OneDrive/Documentos/GitHub/IA_Practica1")
#sys.path.append("C:/Users/llums/OneDrive - Universitat de les Illes Balears/3r informatica/1r Quatrimestre/IA/IA_Practica1-main")

from practica import agentDF, agentAE, joc

# Definició de flags per controlar el tipus d'agent que s'emplea
debugnDF = False
debugnAE = True

def main():
    mida = (6, 6)

    # Per la cerca Depth-First
    if debugnDF:
        agents = [
            agentDF.Viatger("Agent 1", mida_taulell=mida)
        ]

    if debugnAE:
        agents = [
            agentAE.Viatger("Agent 1", mida_taulell=mida)
        ]

    lab = joc.Laberint(agents, mida_taulell=mida)
    lab.comencar()


if __name__ == "__main__":
    main()
