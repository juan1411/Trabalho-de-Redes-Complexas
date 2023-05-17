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


def ler_rede(nome:str) -> tuple:
    """Função para ler as redes e pegar o N (quantidade de nós) e <k> (grau médio).

    nome: str
        apelido interno da rede/chave do dicionário `rede_sociais`.

    return: tuple
        É retornado justamente o N e o <k>. (N, k).
    """    
    # carregando em um objeto `nx.Graph`
    G = nx.read_edgelist('./redes/' + redes_sociais[nome], comments='%', nodetype=int)

    # obtendo o N e o <k>:
    grais = np.array(G.degree)
    N = grais.shape[0]
    grau_medio = grais[:, 1].mean()

    del G, grais # economizando memoria
    return N, grau_medio


def main(modelo:str):
    """Função principal para rodar as simulações da redes sociais e medir o tempo de cada parte.

    modelo: str
        nome do modelo que deve ser simulado.
    """
    # aqui ficarao guardados os resultados das metricas
    # para cada simulacao de cada rede social deste modelo:
    resultados = {'Iteracao': [], 'Rede Social':[]}
    for metrica in METRICAS.keys():
        resultados[metrica] = []

    # Agora sim comecam as simulacoes:
    print('\n# Iniciando simulações do Modelo', modelo.capitalize(),'#\n')
    t_inicial = time.time()
    
    # para todas as redes sociais, faca:
    for rede in redes_sociais.keys():

        ######################################
        # lidando com a rede social
        ######################################
        print('Rede Social --', rede)
        t_carregar = time.time()
        N, grau_medio = ler_rede(rede)
        print(f'N: {N}, <k>: {grau_medio:.4f}')
        print(f'Tempo com a rede: {(time.time() - t_carregar):.2f} segs.\n')


        ######################################
        # simulando o modelo para esta rede
        # &
        # calculando as medidas
        ######################################
        print('Començando as simulações para a rede', rede, '\n')
        t_simulacao = time.time()
        t_calculo_medidas = 0

        for i in range(1, VEZES+1):
            # simulando o modelo:
            G_simulado = SIMULE[modelo](N, grau_medio)

            # calculando as metricas:
            t_inicio_calculo = time.time()
            grau_medio_simulado = METRICAS['grau_medio'](G_simulado)
            t_calculo_medidas += time.time() - t_inicio_calculo

            print(f'Simulacao num.{i} --- Grau Médio Simulado: {grau_medio_simulado:.4f}')
            

        print('\nFim das simulações para a rede', rede)
        print(f'Tempo de simulação: {(time.time() - t_simulacao)/60:.2f} mins.\n')

        print('Fim dos cálculos das medidas para as simulações.')
        print(f'Tempo de cálculo: {t_calculo_medidas:.2f} segs.\n')

    ######################################
    # salvando os resultados
    ######################################

    print('Fim de todas as simulações do modelo', modelo.capitalize(), 'para todas as redes sociais.')
    print(f'Tempo necessário para executar tudo: {(time.time() - t_inicial)/60:.2f} mins.\n')



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
    opcoes = list(SIMULE.keys())
    print(opcoes)

    modelo = input('\nModelo escolhido: ')
    while modelo not in opcoes:
        print('Esta opção de modelo não é válida, escolha uma da lista.')
        modelo = input('\nModelo: ')

    del msg, opcoes # economizando memoria

    main(modelo)