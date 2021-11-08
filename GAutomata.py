# -*- coding: utf-8 -*-
"""
*** Universidad Politecnica Metropolitana de Hidalgo ***
***       Maestria en Inteligencia Artificial        ***
***           Automatas y Lenguaje Natural           ***
***               Producto 02 (Cte 02)               ***
"""
__author__ = ["Jorge Alberto Chavez Alderete", "Ruben Ramirez Gomez"]
__contact__ = [
    "213220158@upmh.edu.mx", "rgomez@upmh.edu.mx", "rramirez@rramirez.com",
    "213220145@upmh.edu.mx",
    ]
__copyright__ = "(c) 2021"
__license__ = "CC BY-NC-ND"
__date__ = "2021-10-27"
__version__ = 1.0


import graphviz
from typing import Optional
from collections import Iterable


class GAutomata():
    """
    Representacion Grafica del automata
    """

    __g = None
    __archivo = ""

    def __init__(
            self, titulo: Optional[str] = "",
            archivo: Optional[str] = 'automata',
            direccion: Optional[str] = "LR",
            nodos_final: Optional[Iterable] = None,
            nodos_incial: Optional[Iterable] = None,
            nodos: Optional[Iterable] = None,
            vertices: Optional[Iterable] = None):
        """
        Clase para objetos que representan graficamente un automata

        Parameters
        ----------
        titulo : string, optional
            Default = "". Titulo para el automata
        archivo : string, optional
            Default = 'automata'. Nombre para salvar el archivo png
            correspondiente al grafico
        direccion : string, optional
            Default "LR". Direccion en la cual se genara el automata,
            valores posibles: LR, LR, TB, BT
        nodos_final : array like, optional
            Default = None. Arreglo (tupla/lista) con las etiquetas de los
            nodos finales del automata
        nodos_incial : array like, optional
            Default = None. Arreglo (tupla/lista) con las etiquetas de los
            nodos iniciales del automata
        nodos : array like, optional
            Default = None. Arreglo (tupla/lista) con las etiquetas de los
            nodos no iniciales/finales del automata
        vertices : array like
            Arreglo (tupla/lista) de vertices a agregar, cada elemento es de
            la forma arreglo (tupla/lista) de dos o tres elementos:
            [
                "Etiqueta_nodo_origen",
                "Etiqueta_nodo_destino",
                "Etiqueta_entrada" (opcional)
            ]

        Returns
        -------
        None.

        """
        self.__g = graphviz.Digraph(titulo, format='png')
        self.__g.attr(rankdir=direccion)
        self.__archivo = archivo
        if nodos_final is not None:
            self.agregar_finales(nodos_final)
        if nodos_incial is not None:
            self.agregar_iniciales(nodos_incial)
        if vertices is not None:
            self.agregar_vertices(vertices)
        if nodos is not None:
            self.agregar_nodos(nodos)

    def agregar_finales(self, nodos: Iterable):
        """
        Agregar nodos finales al grafico correspondiente al automata

        Parameters
        ----------
        nodos : array like
            Agreglo de cadenas de texto con las etiquetas de los nodos.

        Returns
        -------
        None.

        """
        self.__g.attr('node', shape='doublecircle')
        for nodo in nodos:
            self.__g.node(nodo)
        self.__g.attr('node', shape='circle')

    def agregar_final(self, nodo: str):
        """
        Agregar un nodo final al grafico correspondiente al automata

        Parameters
        ----------
        nodo : string
            Etiqueta del nodo.

        Returns
        -------
        None.

        """
        self.agregar_finales([nodo])

    def agregar_iniciales(self, nodos: Iterable):
        """
        Agregar nodos iniciales al grafico correspondiente al automata

        Parameters
        ----------
        nodos : array like
            Agreglo de cadenas de texto con las etiquetas de los nodos.

        Returns
        -------
        None.

        """
        for nodo in nodos:
            self.__g.attr('node', shape='circle')
            self.__g.node(nodo)
            self.__g.attr('node', shape='plain')
            self.__g.edge('inicio', nodo)
        self.__g.attr('node', shape='circle')

    def agregar_inicial(self, nodo: str):
        """
        Agregar un nodo inicial al grafico correspondiente al automata

        Parameters
        ----------
        nodo : string
            Etiqueta del nodo.

        Returns
        -------
        None.

        """
        self.agregar_iniciales([nodo])

    def agregar_nodos(self, nodos: Iterable):
        """
        Agregar nodos no inicial/final al grafico correspondiente al automata

        Parameters
        ----------
        nodos : array like
            Agreglo de cadenas de texto con las etiquetas de los nodos.

        Returns
        -------
        None.

        """
        self.__g.attr('node', shape='circle')
        for nodo in nodos:
            self.__g.node(nodo)

    def agregar_nodo(self, nodo: str) -> None:
        """
        Agregar un nodo no inicial/final al grafico correspondiente al automata

        Parameters
        ----------
        nodo : string
            Etiqueta del nodo

        Returns
        -------
        None.

        """
        self.agregar_nodos([nodo])

    def agregar_vertices(self, vertices: Iterable) -> None:
        """
        Agrega vertices al grafico del automata

        Parameters
        ----------
        vertices : array like
            Arreglo (tupla/lista) de vertices a agregar, cada elemento es de
            la forma arreglo (tupla/lista) de dos o tres elementos:
            [
                "Etiqueta_nodo_origen",
                "Etiqueta_nodo_destino",
                "Etiqueta_entrada" (opcional)
            ]

        Returns
        -------
        None.

        """
        self.__g.attr('node', shape='circle')
        for vertice in vertices:
            self.__g.edge(
                vertice[0],
                vertice[1],
                label=(vertice[2] if len(vertice) == 3 else ""))

    def agregar_vertice(self, vertice: Iterable) -> None:
        """
        Agrega un vertice al grafico del automata

        Parameters
        ----------
        vertice : array like
            Arreglo (tupla/lista) de dos o tres elementos:
            [
                "Etiqueta_nodo_origen",
                "Etiqueta_nodo_destino",
                "Etiqueta_entrada" (opcional)
            ]

        Returns
        -------
        None.

        """
        self.agregar_vertices([vertice])

    def ver(self) -> None:
        """
        Visualiza por pantalla el grafico correspondiente al automata

        Returns
        -------
        None.

        """
        self.__g.view(cleanup=True)

    def guardar(self, archivo: Optional[str] = None) -> None:
        """
        Guarda el grafico correspondiente al automata en el archivo
        *.png indicado por archivo

        Parameters
        ----------
        archivo : string, optional
            Default =  None. Nombre del archivo a crear
            para almacenar en grafico

        Returns
        -------
        None.

        """
        self.__g.render(archivo if archivo else self.__archivo, view=False)
