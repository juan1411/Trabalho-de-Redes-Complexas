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
np.random.seed = SEMENTE


if __name__ == '__main__':
    msg = '\nOlá, este é o arquivo para simular os modelos e calcular as métricas!!!'
    msg += '\nEle segue o seguinte pipeline:'
    msg += '\n\t 1. definição o modelo; \n\t 2. carregamento uma rede social;'
    msg += '\n\t 3. obtenção do N e do <k> da rede; \n\t 4. descarregamento a rede;'
    msg += '\n\t 5. simulação `i` vezes do modelo para a rede;'
    msg += '\n\t 6. cálculo das métricas para cada simulação;'
    msg += '\n\t 7. repetição de 2. a 6. para todas as redes sociais;'
    msg += '\n\t 8. salvamento dos resultados em um arquivo .csv.\n'
    msg += '\nEntão, por favor, defina o modelo. As opções disponíveis são:'
    print(msg)
    opcoes = list(simule.keys())
    print(opcoes)

    modelo = input('\nModelo escolhido: ')
    while modelo not in opcoes:
        print('Esta opção de modelo não é válida, escolha um da lista.')
        modelo = input('\nModelos: ')

    del msg, opcoes # economizando memoria

    print('\n# Iniciando simulações do Modelo', modelo.capitalize(),'#\n')

    t_inicial = time.time()
    # para todas as redes sociais, faca:
    for rede in redes_sociais.keys():

        ######################################
        # lidando com a rede social
        ######################################
        print('Rede Social --', rede)
        t_carregar = time.time()
        # carregando em um objeto `nx.Graph`
        G = nx.read_edgelist('./redes/' + redes_sociais[rede], comments='%', nodetype=int)

        # obtendo o N e o <k>:
        grais = np.array(G.degree)
        N = grais.shape[0]
        grau_medio = grais[:, 1].mean()

        print(f'N: {N}, <k>: {grau_medio:.4f}')
        del G, grais # economizando memoria
        print(f'Tempo com a rede: {(time.time() - t_carregar):.2f} segs.\n')


        ######################################
        # simulando o modelo para esta rede
        ######################################
        t_simulacao = time.time()
        print('Començando as simulações para a rede', rede, '\n')
        for i in range(1, VEZES+1):
            print(i, '- ésima vez simulando o modelo', modelo)

        print('\nFim das simulações para a rede', rede)
        print(f'Tempo de simulação: {(time.time() - t_simulacao):.2f} segs.\n')

        ######################################
        # calculando as medidas
        ######################################


        ######################################
        # salvando os resultados
        ######################################

    print('Fim de todas as simulações do modelo', modelo.capitalize(), 'para todas as redes sociais.')
    print(f'Tempo necessário para executar tudo: {(time.time() - t_inicial)/60:.2f} mins.\n')