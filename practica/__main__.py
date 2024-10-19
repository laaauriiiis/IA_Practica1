import sys
sys.path.append("C:/Users/laura/OneDrive/Documentos/GitHub/IA_Practica1")
#sys.path.append("C:/Users/llums/OneDrive - Universitat de les Illes Balears/3r informatica/1r Quatrimestre/IA/IA_Practica1-main")

from practica import agent, joc

def main():
    mida = (6, 6)

    agents = [
        agent.Viatger("Agent 1", mida_taulell=mida)
         #agent.Viatger("Agent 2", mida_taulell=mida),
    ]
    lab = joc.Laberint(agents, mida_taulell=mida)
    lab.comencar()


if __name__ == "__main__":
    main()
