# bibliotecas estritamente necessarias para manipular as redes
import numpy as np
import networkx as nx

# biblioteca para gerar o arquivo csv com as medidas
import pandas as pd

# biblioteca para medir tempo de execucao de codigo:
import time

# constantes do projeto
from CONSTANTES import *


# definindo a semente em prol da reprodutibilidade:
np.random.seed = semente


if __name__ == '__main__':
    print('\n# Iniciando simulações do Modelo Érdos-Renyi #\n')

    # para todas as redes sociais, faca:
    for rede in redes_sociais.keys():

        ######################################
        # lidando com a rede social
        ######################################
        print('Rede Social --', rede)
        t_carregar = time.time()
        # carregando em um objeto `nx.Graph`
        G = nx.read_edgelist('redes/' + redes_sociais[rede], comments='%', nodetype=int)

        # obtendo o N e o <k>:
        grais = np.array(G.degree)
        N = grais.shape[0]
        grau_medio = grais[:, 1].mean()

        print(f'N: {N} \t<k>: {grau_medio:.4f}')
        del G, grais # economizando memoria
        print(f'Tempo com a rede: {(time.time() - t_carregar):.2f} segs.')
