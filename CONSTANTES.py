########################################################################
# Arquivo com as constantes que precisamos usar por todo o trabalho
########################################################################
import networkx as nx

# definicao da semente, em prol da reprodutibilidade:
SEMENTE = 42

# quantidade de vezes que deve simular os modelos:
VEZES = 10

# dicionario com o caminho ate os dados de cada rede social:
redes_sociais = {'youtube': 'com-youtube/out.com-youtube',
                 }

#######################################################
# vamos padronizar as funcoes para simular os modelos
# de forma que: elas recebam (N, k) e retornem o grafo.
erdos    = lambda N, k: nx.erdos_renyi_graph(N, k/(N-1), seed=SEMENTE)
barabasi = lambda N, k: nx.barabasi_albert_graph(N, int(k/2), seed=SEMENTE)

# dicionario com as funcoes para simular os modelos
simule = {'erdos-renyi': erdos,
          'barabasi-albert': barabasi
        }