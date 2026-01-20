from math import inf

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self.dict_artists_min = None
        self.percorso = None
        self.peso_max = float(-inf)

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.dict_artists_min = DAO.get_artists_by_min(min_albums)
        for a_id in self.dict_artists_min:
            print(self.dict_artists_min[a_id])


    def build_graph(self, min_albums):
        self._graph.clear()
        self.load_artists_with_min_albums(min_albums)
        connessioni = DAO.get_connessioni(min_albums)
        for a_id in self.dict_artists_min:
            artist = self.dict_artists_min[a_id]
            self._graph.add_node(artist)

        for genre_id in connessioni.keys():
            for artist_id_1 in connessioni[genre_id]:
                artist1 = self.dict_artists_min[artist_id_1]
                for artist_id_2 in connessioni[genre_id]:
                    artist2 = self.dict_artists_min[artist_id_2]
                    if artist1 != artist2:
                        if self._graph.has_edge(artist1, artist2):
                            self._graph[artist1][artist2]['weight'] += 1
                        else:
                            self._graph.add_edge(artist1, artist2, weight = 1)

    def get_num_nodes_edges(self):
        nodes = self._graph.number_of_nodes()
        edges = self._graph.number_of_edges()
        return nodes, edges

    def get_conn_artists(self, artist_id):
        coppie = []
        artist1 = self.dict_artists_min[int(artist_id)]
        for artist2 in self._graph.neighbors(artist1):
            peso = self._graph[artist1][artist2]['weight']
            coppia = [artist2, peso]
            coppie.append(coppia)

        return coppie

    def ricerca_percorso(self, max_artisti, artist_id):
        self.percorso = None
        self.peso_max = float(-inf)
        artist = self.dict_artists_min[artist_id]
        self.ricorsione([artist], 0, max_artisti, artist)


        return self.percorso, self.peso_max

    def ricorsione(self, percorso_parziale, peso_corrente, max_artisti, ultimo_artista):
        if len(percorso_parziale) > max_artisti:
            return

        if peso_corrente > self.peso_max:
            self.peso_max = peso_corrente
            self.percorso = percorso_parziale

        for artista in self._graph.neighbors(ultimo_artista):
            if artista not in percorso_parziale:
                peso = int(self._graph[ultimo_artista][artista]['weight'])
                nuovo_percorso = list(percorso_parziale)
                nuovo_percorso.append(artista)
                self.ricorsione(nuovo_percorso, peso_corrente + peso, max_artisti, artista)




