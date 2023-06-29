########################################################################
# Arquivo com as constantes que precisamos usar por todo o trabalho
########################################################################
import networkx as nx
import numpy as np

# definicao da semente, em prol da reprodutibilidade:

# quantidade de vezes que deve simular os modelos:
VEZES = 10

# dicionario com o caminho ate os dados de cada rede social:
redes_sociais = {'twitter-pequeno': 'ego-twitter/out.ego-twitter'
                 # 'twitter-medio': 'munmun_twitter_social/out.munmun_twitter_social'
                 # 'youtube': 'com-youtube/out.com-youtube'
                }

#######################################################
# vamos padronizar as funcoes para simular os modelos
# de forma que: elas recebam (N, k) e retornem o grafo.
erdos    = lambda N, k: nx.erdos_renyi_graph(N, k/(N-1))
barabasi = lambda N, k: nx.barabasi_albert_graph(N, int(k/2))
wattz =    lambda N, k: nx.watts_strogatz_graph(N, int(k/2),1)


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
MEDIDAS = {'grau_medio': grau_medio,
           'assortatividade':nx.degree_assortativity_coefficient,
           'coef_clusterizacao': nx.average_clustering
           #'diametro': nx.diameter
           #'menor_caminho':nx.betweenness_centrality
        }
