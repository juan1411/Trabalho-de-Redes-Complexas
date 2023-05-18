# bibliotecas estritamente necessarias para manipular as redes
import numpy as np
import networkx as nx

# biblioteca para gerar o arquivo csv com as medidas
import pandas as pd

# biblioteca para medir tempo de execucao de codigo:
import time

# para executar as simulacoes em paralelo:
from multiprocessing import Pool

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


def calcula_medidas(G: nx.Graph, iteracao:int, nome_rede:str,
                    resultados_anteriores:pd.DataFrame
                   ) -> pd.DataFrame:
    """Função para calcular as medidas especificadas
     em `MEDIDAS` e atualizar os resultados.
    
    # Parâmetros
    `G`: networkx.Graph
        grafo para o qual serão calculadas as medidas

    `iteracao`: int
        número da iteração correspondente ao grafo `G`

    `nome_rede`: str
        justamente o nome da rede social da qual `G` foi simulado
    
    `resultados_anteriores`: pandas.DataFrame
        dicionário com os resultados anteriores

    # Retorno
    É retornado o dataframe `resltados_anteriores`, porém
     atualizado, agora incluindo as medidas do grafo `G`.
    """
    # por seguranca, tomando uma copia dos resultados_anteriores:
    resultados_novos = resultados_anteriores.copy()

    # calculando todas as medidas:
    for med in MEDIDAS.keys():
        medida = np.nan # inicializa a medida como NaN caso de algum erro

        try: # tentando calcular a medida
            medida = MEDIDAS[med](G)

        except Exception as e: # log de erro
            print('Tentando calcular a medida', med, 'ocorreu o erro', e)

        finally: # em todo caso, sempre atualize os resultados
            resultados_novos.loc[(resultados_novos['Iteracao']==iteracao) &
                                 (resultados_novos['Rede Social']==nome_rede),
                                med] = medida

    return resultados_novos


def main(modelo:str):
    """Função principal para rodar as simulações da redes sociais e medir o tempo de cada parte.

    `modelo`: str
        nome do modelo que deve ser simulado.
    """
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

    print(resultados.head())

    # a criterio de curiosidade, vamos guardar o tempo total
    # de simulcao e de calculo das medidas
    t_total_simulcao = 0
    t_total_calculo = 0

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
        t_simulacao = 0
        t_calculo_medidas = 0

        for i in range(1, VEZES+1):
            # simulando o modelo:
            t_inicio_simulacao = time.time()
            G_simulado = SIMULE[modelo](N, grau_medio)
            t_simulacao += time.time() - t_inicio_simulacao

            # calculando as medidas e atualizando os resultados:
            t_inicio_calculo = time.time()
            resultados = calcula_medidas(G_simulado, i, rede, resultados)
            t_calculo_medidas += time.time() - t_inicio_calculo

            print(f'{rede.capitalize()} \tSimulação #{i} \tOK')
            

        print('\nFim das simulações para a rede', rede)
        print(f'Tempo de simulação: {t_simulacao/60:.2f} mins.\n')
        t_total_simulcao += t_simulacao

        print('Fim dos cálculos das medidas para as simulações da rede', rede)
        print(f'Tempo de cálculo: {t_calculo_medidas:.2f} segs.\n')
        t_total_calculo += t_calculo_medidas

    ######################################
    # log extra dos tempo totais:
    print(f'Fim de todas as simulações. Tempo total: {t_total_simulcao/60:.2f} mins.')
    print(f'Fim do cálculo de todas as medidas. Tempo total: {t_total_calculo:.2f} segs.')

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