########################################################################
# Arquivo com as constantes que precisamos usar por todo o trabalho
########################################################################
import networkx as nx
import numpy as np


# quantidade de vezes que deve simular os modelos:
VEZES = 30

# dicionario com o caminho ate os dados de cada rede social:
redes_sociais = {
    'adolescente': 'moreno_health/out.moreno_health_health',
    'facebook': 'ego-facebook/out.ego-facebook',
    'hamster': 'petster-hamster/out.petster-hamster'
}

def ler_rede(nome:str, grafo:bool=False) -> tuple:
    """Função para ler as redes e pegar o N (quantidade de nós) e <k> (grau médio).

    # Parâmetros
    `nome`: str
        apelido interno da rede/chave do dicionário `rede_sociais`.

    `grafo`: bool, padrão `False`
        indicação se a função deve ou não retornar o grafo carregado.

    # Retorno
    É retornado justamente o N e o <k>: (N, k).

    No caso em que `grafo = True`, é retornado apenas o Grafo: (G).
    """    
    # carregando em um objeto `nx.Graph`
    if (nome == 'adolescente'):
        G = nx.read_edgelist(
            './redes/' + redes_sociais[nome], comments='%',
            nodetype=int, data=(('weight', float),)
        )
    else:
        G = nx.read_edgelist('./redes/' + redes_sociais[nome], comments='%', nodetype=int)

    if grafo: return G
    else:
        # obtendo o N e o <k>:
        grais = np.array(G.degree)
        N = grais.shape[0]
        grau_medio = grais[:, 1].mean()

        del G, grais # economizando memoria
        return int(N), grau_medio


#######################################################
# vamos padronizar as funcoes para simular os modelos
# de forma que: elas recebam (N, k) e retornem o grafo.
erdos     = lambda N, k: nx.erdos_renyi_graph(N, k/(N-1))
barabasi  = lambda N, k: nx.barabasi_albert_graph(N, int(k/2))
wattz_p1  = lambda N, k: nx.watts_strogatz_graph(N, int(k), p=1)
wattz_p05 = lambda N, k: nx.watts_strogatz_graph(N, int(k), p=0.5)
wattz_p01  = lambda N, k: nx.watts_strogatz_graph(N, int(k), p=0.01)


# dicionario com as funcoes para simular os modelos
SIMULE = {
    'ER': erdos,
    'BA': barabasi,
    'WS_P10' : wattz_p1,
    'WS_P05' : wattz_p05,
    'WS_P01' : wattz_p01
}

#######################################################
# vamos padronizar as funcoes para calcular a metricas
# de forma que: elas recebam G e retornem a metrica.
grau_medio = lambda G: np.array(G.degree)[:, 1].mean()

bc_mean = lambda G: np.mean(
    list(dict(nx.betweenness_centrality(G, k=int(len(G)))).values()))

len_bari = lambda G: len(nx.barycenter(G))

excent_mean = lambda G: np.mean(list(dict(nx.eccentricity(G)).values()))

s_metric = lambda G: nx.s_metric(G, False)

def degree_distribution(GER):
    vk = dict(GER.degree())
    vk = list(vk.values())
    maxk = np.max(vk)
    kvalues= np.arange(0, maxk+1)
    Pk = np.zeros(maxk+1)
    for k in vk: Pk[k] += 1
    Pk = Pk/sum(Pk)
    return kvalues, Pk


def shannon_entropy(G):
    _, Pk = degree_distribution(G)
    H = 0
    for p in Pk:
        if(p > 0): H -= p*np.log2(p)
    return H


def cd(G):
    vals = list(dict(nx.betweenness_centrality(G, k=int(len(G)))).values())
    b_max = max(vals)
    n = len(vals)
    return (n*b_max - sum(vals))/(n - 1) 


def corr_grau_cliques(G):
    cliques = [sum([1 for _ in nx.find_cliques(G, [n])]) for n in G]
    corr = np.corrcoef(
        list(dict(G.degree()).values()), cliques
    )
    return corr[0, 1]

corr_grau_vizinhos = lambda G: np.corrcoef(
    list(dict(G.degree()).values()),
    list(nx.average_neighbor_degree(G).values())
    )[0,1]

corr_grau_close = lambda G: np.corrcoef(
    list(dict(G.degree()).values()),
    list(dict(nx.closeness_centrality(G)).values())
    )[0,1]


# dicionario com as funcoes para calcular as medidas
MEDIDAS = {
    'grau_medio': grau_medio,
    'assortatividade':nx.degree_assortativity_coefficient,
    'coef_clusterizacao': nx.average_clustering,
    'transitividade' : nx.transitivity,
    'entropia' : shannon_entropy,
    'media_dos_menores_caminhos' : nx.average_shortest_path_length,
    'intermediacao_media': bc_mean,
    'ponto_central_de_dominancia': cd,
    'diametro': nx.diameter,
    'metrica_s': s_metric,
    'qtd_baricentros': len_bari,
    'excentricidade_media': excent_mean,
    'cor_grau_e_grau_medio_vizinhos': corr_grau_vizinhos,
    'cor_grau_e_proximidade': corr_grau_close,
    'cor_grau_e_cliques': corr_grau_cliques
}


def calcula_medidas(G: nx.Graph, debug:bool=False) -> dict:
    """Função para calcular todas as medidas especificadas em `MEDIDAS`.
    
    # Parâmetros
    `G`: networkx.Graph
        grafo para o qual serão calculadas as medidas

    `debug`: bool, padrão `False`
        indicação se a função deve ser executada no "modo" debug, i.e. com os prints ativados.
    
    # Retorno
    É retornado um dicionario com os pares (`nome: str:`, `valor: [numpy.nan|numpy.float32]`). 
    """
    calculos = {}
    for med in MEDIDAS.keys():
        valor = np.nan # inicializa o valor como NaN caso de algum erro

        try: # tentando calcular a medida
            valor = np.float32(MEDIDAS[med](G))
            if debug: print('Medida:', med, '- valor:', round(valor, 4))

        except Exception as e: # log de erro
            if debug: print('Tentando calcular a medida', med, '\nocorreu o erro:', e)

        finally:
            calculos[str(med)] = valor

    return calculos
