
import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model


    def handle_create_graph(self, e):
        try:
            minimo = int(self._view.txtNumAlbumMin.value)
            if minimo < 0:
                self._view.show_alert("Inserire un numero intero maggiore o uguale a 0")
            else:
                self._model.build_graph(minimo)
                for artist_id in self._model.dict_artists_min:
                    artist = self._model.dict_artists_min[artist_id]
                    self._view.ddArtist.options.append(ft.DropdownOption(key = artist_id, text = artist))
                self._view.btnArtistsConnected.disabled = False
                self._view.ddArtist.disabled = False
                self._view.btnSearchArtists.disabled = False
                self._view.txtMaxArtists.disabled = False
                self.handle_info_graph()
                self._view.update_page()

        except Exception as e:
            self._view.show_alert("Inserire un numero intero")

    def handle_info_graph(self):
        self._view.txt_result.controls.clear()
        nodes, edges = self._model.get_num_nodes_edges()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {nodes} nodi (artisti), e {edges} archi "))
        self._view.update_page()

    def handle_connected_artists(self, e):
        self._view.txt_result.controls.clear()
        artist_id = int(self._view.ddArtist.value)
        coppie = self._model.get_conn_artists(artist_id)
        artist1 = self._model.dict_artists_min[artist_id]
        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista {artist1}"))
        for coppia in coppie:
            artist2 = coppia[0]
            peso = coppia[1]
            self._view.txt_result.controls.append(ft.Text(f"{artist2} - Numero di generi in comune: {peso}"))
        self._view.update_page()

    def handle_ricerca_percorso(self, e):
        self._view.txt_result.controls.clear()
        artist_id = int(self._view.ddArtist.value)
        artist = self._model.dict_artists_min[artist_id]
        try:
            max_artisti = int(self._view.txtMaxArtists.value)
            if max_artisti < 0:
                self._view.show_alert("Inserire un numero intero maggiore o uguale a 0")
            else:
                percorso, peso = self._model.ricerca_percorso(max_artisti, artist_id)
                self._view.txt_result.controls.append(ft.Text(f"Cammino di peso massimo dall'artista {artist}"))
                self._view.txt_result.controls.append(ft.Text(f"Lunghezza {len(percorso)}"))
                for artist in percorso:
                    self._view.txt_result.controls.append(ft.Text(f"{artist}"))
                self._view.txt_result.controls.append(ft.Text(f"Peso massimo {len(peso)}"))
                self._view.update_page()

        except Exception:
            self._view.show_alert("Inserire un numero intero")






