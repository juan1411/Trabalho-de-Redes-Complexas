########################################################################
# Arquivo com as constantes que precisamos usar por todo o trabalho
########################################################################
import networkx as nx
import numpy as np
import math


def degree_distribution(GER):
    vk = dict(GER.degree())
    vk = list(vk.values()) # we get only the degree values
    maxk = np.max(vk)
    mink = np.min(min)
    kvalues= np.arange(0,maxk+1) # possible values of k
    Pk = np.zeros(maxk+1) # P(k)
    for k in vk:
        Pk[k] = Pk[k] + 1
    Pk = Pk/sum(Pk) # the sum of the elements of P(k) must to be equal to one
    return kvalues,Pk


def shannon_entropy(G):
    k,Pk = degree_distribution(G)
    H = 0
    for p in Pk:
        if(p > 0):
            H = H - p*math.log(p, 2)
    return H


corr_grau_vizinhos = lambda G: np.corrcoef(
    list(dict(G.degree()).values()),
    list(nx.average_neighbor_degree(G).values())
    )[0,1]

corr_grau_close = lambda G: np.corrcoef(
    list(dict(G.degree()).values()),
    list(dict(nx.closeness_centrality(G)).values())
    )[0,1]

corr_grau_bet = lambda G: np.corrcoef(
    list(dict(G.degree()).values()),
    list(dict(nx.betweenness_centrality(G)).values())
    )[0,1]


# quantidade de vezes que deve simular os modelos:
VEZES = 10

# dicionario com o caminho ate os dados de cada rede social:
redes_sociais = {
    'twitter-pequeno': 'ego-twitter/out.ego-twitter',
    'facebook': 'ego-facebook/out.ego-facebook',
    'hamster': 'petster-hamster/out.petster-hamster',
    #'bitcoin': 'download.tsv.soc-sign-bitcoinotc/soc-sign-bitcoinotc/out.soc-sign-bitcoinotc'
    # 'twitter-medio': 'munmun_twitter_social/out.munmun_twitter_social'
    # 'youtube': 'com-youtube/out.com-youtube'
}

#######################################################
# vamos padronizar as funcoes para simular os modelos
# de forma que: elas recebam (N, k) e retornem o grafo.
erdos    = lambda N, k: nx.erdos_renyi_graph(N, k/(N-1))
barabasi = lambda N, k: nx.barabasi_albert_graph(N, int(k/2))
wattz =    lambda N, k: nx.watts_strogatz_graph(N, int(k),p = 1) ####Debugar



# dicionario com as funcoes para simular os modelos
SIMULE = {'erdos-renyi': erdos,
          'barabasi-albert': barabasi,
          'watts_strogatz_graph' : wattz
        }

#######################################################
# vamos padronizar as funcoes para calcular a metricas
# de forma que: elas recebam G e retornem a metrica.
grau_medio = lambda G: np.array(G.degree)[:, 1].mean()

# dicionario com as funcoes para calcular as medidas
MEDIDAS = {
    'grau_medio': grau_medio,
    'assortatividade':nx.degree_assortativity_coefficient,
    'coef_clusterizacao': nx.average_clustering,
    'transitivade' : nx.transitivity,
    'entropy' : shannon_entropy,
    # 'cor_grau_e_grau_medio_vizinhos': corr_grau_vizinhos,
    # 'cor_grau_e_proximidade': corr_grau_close,
    # 'cor_grau_e_centralidade': corr_grau_bet,
    # 'average_shortests_path_lenght' : nx.average_shortest_path_length,
   # 'diametro': nx.diameter
    #'menor_caminho':nx.betweenness_centrality
}
