# bibliotecas estritamente necessarias para manipular as redes
import numpy as np
import networkx as nx

# biblioteca para gerar o arquivo csv com as medidas
import pandas as pd

# biblioteca para medir o tempo de execucao do codigo:
import time

# para executar as simulacoes em paralelo:
from concurrent.futures import ProcessPoolExecutor, as_completed

# constantes do projeto
from CONSTANTES import *


# definindo a semente em prol da reprodutibilidade:
np.random.seed = SEMENTE


def ler_rede(nome:str) -> tuple:
    """Função para ler as redes e pegar o N (quantidade de nós) e <k> (grau médio).

    `nome`: str
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
    return int(N), grau_medio


def calcula_medidas(G: nx.Graph, iteracao:int, nome_rede:str):
    """Função para calcular as medidas especificadas
     em `MEDIDAS` e atualizar os resultados.
    Atenção!! Os resultados que serão atualizados
     estão em uma variável global.
    
    # Parâmetros
    `G`: networkx.Graph
        grafo para o qual serão calculadas as medidas

    `iteracao`: int
        número da iteração correspondente ao grafo `G`

    `nome_rede`: str
        justamente o nome da rede social da qual `G` foi simulado
    """
    # variavel global
    global resultados

    # calculando todas as medidas:
    for med in MEDIDAS.keys():
        medida = np.nan # inicializa a medida como NaN caso de algum erro

        try: # tentando calcular a medida
            medida = MEDIDAS[med](G)

        except Exception as e: # log de erro
            print('Tentando calcular a medida', med, 'ocorreu o erro:', e)

        finally: # em todo caso, sempre atualize os resultados
            resultados.loc[(resultados['Iteracao']==iteracao) &
                           (resultados['Rede Social']==nome_rede),
                           med] = medida


def simula_modelo(modelo:str, N:int, grau_medio:float) -> nx.Graph:
    """Função para simular o modelo uma única vez.

    # Parâmetros

    `modelo`: str
        nome do modelo que deve ser simulado; deve ser uma chave de `SIMULE`

    `N`: int
        número de vértices desejados para o grafo

    `grau_medio`: float
        grau médio (ou número médio de conexões por nó) desejado para o grafo

    # Retorno
    É retornado o grafo simulado, sendo ele um objeto `networkx.Graph`.
    """
    G_simulado = SIMULE[modelo](N, grau_medio)
    return G_simulado


def main(modelo:str):
    """Função principal para rodar as simulações da redes sociais e medir o tempo de cada parte.

    `modelo`: str
        nome do modelo que deve ser simulado.
    """
    # variaveis globais:
    global resultados

    # os nomes das redes sociais:
    chaves = [ch for ch in redes_sociais.keys()]

    # variaveis auxiliares para inicializar o dataframe dos resultados
    # shape dos resultados: ('qtd de simulacoes'x'qtd de redes', 'qtd de medidas')
    shape_res = ( VEZES*len(chaves), len(MEDIDAS.keys()) )
    aux = np.full(shape_res, fill_value=np.nan)

    # aqui ficarao guardados os resultados das metricas
    # para cada simulacao de cada rede social deste modelo:
    resultados = pd.DataFrame(aux, columns=MEDIDAS.keys())
    resultados['Rede Social'] = np.repeat(chaves, VEZES)
    resultados['Iteracao'] = list(range(1, VEZES+1))*len(chaves)

    # por curiosidade, vamos guardar o tempo total de simulcao
    t_total_simulacao = 0

    # Agora sim comecam as simulacoes:
    print('\n# Iniciando simulações do Modelo', modelo.capitalize(),'#\n')
    t_inicial = time.time()
    
    # para todas as redes sociais, faca:
    for rede in chaves:

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

        # faremos a contagem de tempo
        t_simulacao = time.time()

        # executando as simulacoes em paralelo, 5 por vez:
        with ProcessPoolExecutor(5) as executor:

            # basicamente, esse dicionario contem uma `resposta` do executor.submit
            # essas `respostas` chegam assim que a funcao `simula_modelo` retorna algo
            futuros_retornos = {
                executor.submit(simula_modelo, modelo, N, grau_medio):
                    (i, rede) for i in range(1, VEZES+1)
                }

            # assim que `executor.submit` retornar uma resposta,
            # já é possível entrar neste for-loop
            for simulacao in as_completed(futuros_retornos):
                ite, nome_rede = futuros_retornos[simulacao]
                print(f'{nome_rede.capitalize()} \tSimulação #{ite} \tOK')
                G_simulado = simulacao.result()

                # calculando todas as medidas para o grafo simulado
                calcula_medidas(G_simulado, ite, nome_rede)
                print(f'{rede.capitalize()} \tMedidas #{ite} \tOK')


        # atualizando os tempos
        t_simulacao = time.time() - t_simulacao

        # logs de registro
        print('\nFim das simulações para a rede', rede)
        print(f'Tempo de simulação: {t_simulacao//60:.0f} mins e {t_simulacao%60:.2f} segs.\n')
        t_total_simulacao += t_simulacao


    ######################################
    # log extra dos tempo totais:
    print('Fim de todas as simulações.',
          f'Tempo total: {t_total_simulacao//60:.0f} mins e {t_total_simulacao%60:.2f} segs.')
    

    ######################################
    # salvando os resultados
    ######################################
    nome_arq = 'Modelo_'+str(modelo)+'.csv'
    print(f'\nComeçando agora a compilar o arquivo [{nome_arq}] com os resultados.')
    t_resultados = time.time()
    resultados.to_csv(nome_arq, index=False)

    print('Fim da compilação dos resultados.')
    print(f'Tempo de compilação: {(time.time() - t_resultados):.2f} segs.\n')

    print('Fim de todas as simulações do modelo', modelo.capitalize(), 'para todas as redes sociais.')
    t_final = time.time() - t_inicial
    print(f'Tempo necessário para executar tudo: {t_final//60:.0f} mins e {t_final%60:.2f} segs.\n')



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