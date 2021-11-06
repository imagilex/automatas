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

"""
Caracter para palabra (caracter) vacio:
    CODIGO ASCII 146
    Entidad HTML: &AElig;
"""


import pandas as pd
import numpy as np
from itertools import chain, combinations
from GAutomata import GAutomata
from copy import deepcopy


caracter_vacio = chr(198)


def conjuntoPotencia(array) -> list:
    """
    Calcula del conjunto potencia de un conjunto de elementos

    Parameters
    ----------
    array : array like
        Conjunto base sobre el cual se determinara el conjunto potencia.

    Returns
    -------
    list
        Conjunto potencia

    """
    s = list(array)
    return [
        set(tupla)
        for tupla in chain.from_iterable(
                combinations(s, r) for r in range(len(s) + 1))]


def set2Str(conjunto) -> str:
    """
    Convierte un conjunto a su representacion como cadena de texto

    Parameters
    ----------
    conjunto : set
        conjunto de elementos a representar como cadena.

    Returns
    -------
    str
        Cadena de texto que representa al conjunto.

    """
    return f"{sorted(conjunto)}".replace(
        "'", "").replace(
            '[', '{').replace(
                ']', '}')


def entradas2ER(entradas) -> str:
    """
    Convierte un conjunto de elementos a su representacion como
    expresion regular simple, p.e.:
        [] => '' (Cadena vacia)
        [0] => '0'
        [0, 1] => '(0+1)'

    Parameters
    ----------
    entradas : array like
        elementos a representar.

    Returns
    -------
    str
        Representacion como er simple del conjunto de elementos.

    """
    if 1 == len(entradas) and isinstance(entradas[0], TerminoER):
        return entradas[0]
    return None if 0 == len(entradas) else TerminoER(terminos=entradas)


class TerminoER:
    """
    Representacion de un termino de una expresion regular
    """

    def __init__(self, siguienteTermino=None, terminos=None, reqKleene=False):
        """
        Representacion de un termino de una expresion regular

        Parameters
        ----------
        siguienteTermino : TerminoER, optional
            Termino para concatenar al Termino que se creará. Default None.
        terminos : array like, optional
            Terminos para unir. Nefault None.
        reqKleene : bool, optional
            Indiqca si este término requiere o no * (clausula de Kleene).
            Default False.

        Returns
        -------
        None.

        """
        # Termino siguiente a concatenar
        self.nextTermino = siguienteTermino
        self.requiereClausulaKleene = reqKleene
        # Terminos a unir
        self.terminos = list()
        for term in terminos:
            self.unirTermino(term)

    def unirTermino(self, termino) -> None:
        """
        Agrega un termino para UNION

        Parameters
        ----------
        termino : str or TemrinoER
            Termino a UNIR.

        Returns
        -------
        None

        """
        if termino and termino not in self.terminos:
            if isinstance(termino, TerminoER):
                new_terms = list()
                aniadido = False
                for term in self.terminos:
                    if isinstance(term, TerminoER):
                        if (termino.terminos == term.terminos and
                                termino.requiereClausulaKleene ==
                                term.requiereClausulaKleene):
                            t1 = TerminoER(
                                terminos=termino.terminos,
                                reqKleene=termino.requiereClausulaKleene)
                            t2 = TerminoER(terminos=[
                                term.nextTermino, termino.nextTermino])
                            t1.concatenarTermino(t2)
                            new_terms.append(t1)
                            aniadido = True
                            continue
                    new_terms.append(term)
                if not aniadido:
                    new_terms.append(termino)
                self.terminos = new_terms
            else:
                self.terminos.append(termino)

    def concatenarTermino(self, termino) -> None:
        """
        Agrega un termino para CONCATENAR

        Parameters
        ----------
        termino : str or TemrinoER
            Termino a concatenar.

        Returns
        -------
        None

        """
        current = self
        while current.nextTermino:
            current = current.nextTermino
        current.nextTermino = termino

    def __str__(self) -> str:
        """
        Conversion a cadena de texto

        Returns
        -------
        str

        """
        cadena = ""
        if 1 == len(self.terminos):
            cadena = str(self.terminos[0])
        elif 1 < len(self.terminos):
            cadena = f"({'+'.join(sorted([str(t) for t in self.terminos]))})"
        if self.requiereClausulaKleene:
            cadena += "*"
        if self.nextTermino:
            cadena += str(self.nextTermino)
        return cadena


class Automata():
    """
    Representacion del automata
    """
    __estados = set()
    __iniciales = set()
    __finales = set()
    __vertices = list()
    __alfabeto = set()
    __grafo = None
    __spliter_entradas = ","

    def __init__(
            self, iniciales=[], finales=[], archivo_matriz="",
            spliter_entradas=",", just_struct=False):
        """
        Representacion de un automata, el cual puede ser o no determinista

        Parameters
        ----------
        iniciales : list, optional
            Lista de estados iniciales. Default [].
        finales : list, optional
            Lista de estados finales. Default [].
        archivo_matriz : str, optional
            Ruta al archivo csv con la matriz de adyacencia que representa al
            automata. Default "".
        spliter_entradas : str, optional
            Divisor de elementos de entrada en la matriz de adyacencia.
            Default ",".
        just_struct : Boolean, optional
            Indica si unicamente se generara la estructura del objeto.
            Default False.

        Raises
        ------
        ValueError
            Al no aniadir los nodos iniciales
            Al no aniadir los nodos finales
            Al encontrar inconsistencias en la matriz de adyacencia

        Returns
        -------
        Automata

        """
        self.__vertices = list()
        self.__alfabeto = set()
        self.__grafo = None
        if just_struct:
            self.__iniciales = set()
            self.__finales = set()
            self.__estados = set()
            self.__spliter_entradas = ","
            return
        if 0 == len(iniciales):
            raise ValueError("La cantidad de nodos iniciales no puede ser 0")
        if 0 == len(finales):
            raise ValueError("La cantidad de nodos finales no puede ser 0")
        self.__iniciales = set(iniciales)
        self.__finales = set(finales)
        dfTmp = pd.read_csv(archivo_matriz, index_col=0)
        if len(dfTmp.columns) != len(dfTmp.index):
            raise ValueError(
                f"El archivo {archivo_matriz} de contener una matriz de "
                "adyacencia cuadrada")
        for col in dfTmp.columns:
            if col not in dfTmp.index:
                raise ValueError(
                    f"La columna {col} no se encuentra en las filas")
        for nodo in self.__iniciales.union(self.__finales):
            if nodo not in dfTmp.columns:
                raise ValueError(
                    f"El nodo {nodo} no se encuentra en la matriz")
        self.__spliter_entradas = spliter_entradas
        self.__estados = set(dfTmp.columns)
        for idx in dfTmp.columns:
            for col in dfTmp.columns:
                if not pd.isnull(dfTmp.loc[idx][col]):
                    label = dfTmp.loc[idx][col]
                    label = str(
                        int(label)
                        if isinstance(label, np.float64)
                        else label)
                    entradas = [
                        entrada.strip()
                        for entrada in label.split(self.__spliter_entradas)]
                    self.__vertices.append({
                        'from': idx,
                        'to': col,
                        'entradas': entradas
                        })
                    self.__alfabeto = self.__alfabeto.union(set(entradas))

    def __create_graph(self) -> None:
        """
        (De uso interno). Genera la represtacion grafica del automata
        utlizando GAutomata

        Returns
        -------
        None.

        """
        self.__grafo = GAutomata(
            nodos_final=self.estados_finales,
            nodos_incial=self.estados_iniciales,
            vertices=[
                (
                    vertice['from'],
                    vertice['to'],
                    self.__spliter_entradas.join(sorted([
                        str(e) for e in vertice['entradas']]))
                ) for vertice in self.vertices])

    @property
    def estados_iniciales(self) -> set:
        """
        Conjunto de estados iniciales del automata

        Returns
        -------
        set.

        """
        return set(self.__iniciales)

    @property
    def estados_finales(self) -> set:
        """
        Conjunto de estados finales del automata

        Returns
        -------
        set.

        """
        return set(self.__finales)

    @property
    def estados(self) -> set:
        """
        Conjunto de estados del automata

        Returns
        -------
        set.

        """
        return set(self.__estados)

    @property
    def vertices(self) -> list:
        """
        Lista de vertices del automata donde cada elemento es un diccionario
        con la forma:
            {
                'from': str estado de inicio del vertice
                'to': str estado del final del vertice
                'entradas': list con elementos del alfabeto que transfieren de
                    from a to
            }

        Returns
        -------
        list.

        """
        return list(self.__vertices)

    @property
    def alfabeto(self) -> set:
        """
        Conjunto con los elementos que forman parte del alfabeto

        Returns
        -------
        set.

        """
        return set(self.__alfabeto)

    def save_png(self, filename) -> None:
        """
        Almacena la representacion grafica del automata en un archivo *.png

        Parameters
        ----------
        filename : str
            Ruta y nombre del archivo sin extension.

        Returns
        -------
        None.

        """
        self.__create_graph()
        if self.__grafo:
            self.__grafo.guardar(filename)

    def transicion(self, estado, entrada) -> set:
        """
        Funcion de transicion.

        Parameters
        ----------
        estado : str
            Estado inicial.
        entrada : str
            Entrada con la cual se tranfiere desde el estado a otro u otros
            estados.

        Raises
        ------
        ValueError
            Si el estado no pertenece al automata o la entrada no pertenece al
            alfabeto del automata.

        Returns
        -------
        set
            Conjunto de estados a los cuales se transfiere desde el estado
            utlizando la entrada, en caso de no haber estados a transferir
            el conjunto sera vacio sde estados resultado sera vacio.
        """
        if estado not in self.estados:
            raise ValueError(f"El estado {estado} no se encuentra")
        if entrada not in self.alfabeto:
            raise ValueError(f"La entrada {entrada} no se encuentra")
        vertices = filter(
            lambda edo: edo['from'] == estado and entrada in edo['entradas'],
            self.vertices)
        return set([vertice['to'] for vertice in vertices])

    def transicion_extendida(self, palabra, inicio=None) -> set:
        """
        Funcion de transicion extendida

        Parameters
        ----------
        palabra : str
            DESCRIPTION.
        inicio : str, array like, optional
            Estado o estados desde los cuales comenzara a calcularse la
            transicion extendida, en caso de no recibirse el parametro se
            comienza a tranferir desde los estados iniciales del automata.
            Default None.

        Raises
        ------
        ValueError
            Si la palabra esta vacia.

        Returns
        -------
        set
            Conjunto de estados a los que se ha transferido luego de
            verificar la palabra completa. Puede estar vacio en caso de que
            alguna palabra contenga un caracter no propio del alfabeto o bien
            si al final de las transiciones o en un "estado intermedio" no hay
            estados de salida para con el caracter siguiente a verificar.

        """
        """TODO: trabaja bien solo cuando los caracteres del alfabeto son de
        un solo caracter"""
        if 0 == len(palabra):
            raise ValueError("La palabra esta vacia")
        inicio = set(inicio) if inicio else self.estados_iniciales
        continuar = True
        while continuar:
            inicio = inicio.union(self.__estado_paso_vacio(inicio))
            edos_paso = set()
            try:
                for edo in inicio:
                    edos_paso = edos_paso.union(
                        self.transicion(edo, palabra[0]))
            except ValueError:
                return {}
            continuar = 0 < len(edos_paso) and 1 < len(palabra)
            palabra = palabra[1:]
            inicio = set(edos_paso)
        if 0 == len(edos_paso):
            return {}
        return edos_paso.union(self.__estado_paso_vacio(edos_paso))

    def __estado_paso_vacio(self, estados) -> set:
        """
        Devuelve los nodos adyacentes correspondientes a estados a donde se
        puede transferir con entradas de cadena vacia
        Parameters
        ----------
        estados : set
            Estados de cuales se verifican entradas de cadena vacia que
            transfieren a otros estados.
        Returns
        -------
        set.
        """
        if not self.acepta_caracter_vacio:
            return set()
        edos = set()
        for edo in estados:
            edos = edos.union(set([
                vt['to']
                for vt in self.vertices
                if vt['from'] == edo and caracter_vacio in vt['entradas']]))
        return edos

    def verificar_palabra(self, palabra) -> bool:
        """
        Verifica si una palabra pertenece o no al lenguaje generado por
        el automata

        Parameters
        ----------
        palabra : str
            Palabra a verificar.

        Returns
        -------
        bool.
        """
        return 0 < len(self.estados_finales.intersection(
            self.transicion_extendida(palabra)))

    @property
    def AFN2AFD(self):
        """
        Forma del automata como automata finito determinista.

        La transaformacion se realiza utilizando el metodo planteado en
        Hopcroft, J. et. al. (2007). Introduccion a la Teoria de Automatas,
        Lenguajes y Computacion.

        Returns
        -------
        resultado : Automata.

        """
        resultado = Automata(just_struct=True)
        resultado.__alfabeto = self.alfabeto
        resultado.__iniciales = set([set2Str(self.estados_iniciales)])
        resultado.__finales = set()
        resultado.__spliter_entradas = self.__spliter_entradas
        resultado.__estados = set(resultado.estados_iniciales)
        resultado.__vertices = list()
        resultado.__grafo = None
        conj_pot = conjuntoPotencia(self.estados)
        for conj in conj_pot:
            lbl_edo = set2Str(conj)
            resultado.__estados.add(lbl_edo)
            if 0 < len(conj.intersection(self.estados_finales)):
                resultado.__finales.add(lbl_edo)
            for simb in resultado.alfabeto:
                edos_paso = set()
                for edo in conj:
                    edos_paso = edos_paso.union(self.transicion(edo, simb))
                lbl2 = set2Str(edos_paso)
                vert = [vt
                        for vt in resultado.__vertices
                        if vt['from'] == lbl_edo and vt['to'] == lbl2]
                if 0 < len(vert):
                    vert[0]['entradas'].append(simb)
                else:
                    resultado.__vertices.append({
                        'from': lbl_edo,
                        'to': set2Str(edos_paso),
                        'entradas': [simb]
                        })
        resultado.__remover_inecesarios()
        return resultado

    def __remover_inecesarios(self) -> None:
        """
        (De uso interno). Remueve nodos inecerarios en al automata, estos
        pueden ser los resultantes de automata.candidates2remove o bien estados
        que no son finales y que tampoco transfieren a ningun otro estado.

        Returns
        -------
        None.

        """
        vert2remove = self.candidates2remove
        while len(vert2remove):
            self.__estados = self.estados.difference(vert2remove)
            self.__finales = self.estados_finales.difference(
                vert2remove)
            self.__vertices = [
                vt
                for vt in self.vertices
                if vt['from'] in self.estados]
            vert2remove = self.candidates2remove
        nodos2 = set([
            vt['to'] for vt in self.vertices
            if vt['to'] not in self.estados_iniciales.union(
                    self.estados_finales) and vt["to"] != vt['from']])
        nodosFrom = set([
            vt['from'] for vt in self.vertices
            if vt['from'] not in self.estados_iniciales.union(
                    self.estados_finales) and vt["to"] != vt['from']])
        nodosSinSalida = nodos2.difference(nodosFrom)
        self.__estados = self.estados.difference(nodosSinSalida)
        self.__vertices = [
            vt
            for vt in self.vertices
            if vt['to'] not in nodosSinSalida]

    @property
    def candidates2remove(self) -> set:
        """
        Nodos candidatos a ser removidos del automata sin alterar el lenguaje
        generado, tipicamente estos estados seran los nodos que no son
        iniciales pero que ademas tampoco son resultado de alguna transicion
        desde otros nodos

        Returns
        -------
        set.

        """
        vert_in = set([
            vt['to'] for vt in self.__vertices
            ]).union(self.estados_iniciales)
        vert2remove = self.estados.difference(vert_in)
        vert_ciclo = set([
            vt['to'] for vt in self.vertices if vt['from'] == vt['to']])
        vert_in_cicle = set([
            vt['to']
            for vt in self.vertices
            if vt['from'] != vt['to'] and vt['to'] in vert_ciclo])
        return vert2remove.union(
            vert_ciclo.difference(vert_in_cicle)
            ).difference(
                self.estados_iniciales)

    @property
    def isAFN(self) -> bool:
        """
        Indica si es automata es o no un automata finito no determinista

        Returns
        -------
        bool.

        """
        verts = set([vt['from'] for vt in self.vertices])
        for vert in verts:
            entradas = list()
            for vt in self.vertices:
                if vt['from'] == vert:
                    for entrada in vt['entradas']:
                        if entrada in entradas:
                            return True
                        else:
                            entradas.append(entrada)
        return False

    @property
    def acepta_caracter_vacio(self) -> bool:
        """
        Indica si se acepta o no el caracter como palabra vacia (epsilon),
        se realiza con base en el alfabeto del automata.

        Returns
        -------
        bool.

        """
        return caracter_vacio in self.alfabeto

    def __get_entradas(self, nodo_from, nodo_to) -> list:
        """
        (De uso interno). Obtiene las diferentes entradas de un nodo a otro,
        las simplifica en caso de que existan multiples vertices

        Parameters
        ----------
        nodo_from : str
            Nodo incial.
        nodo_to : str
            Nodo final.

        Returns
        -------
        list.

        """
        aux = []
        for vt in self.vertices:
            if vt['from'] == nodo_from and vt['to'] == nodo_to:
                aux += vt['entradas']
        return aux

    def __reduce_no_finales(self) -> None:
        """
        (De uso interno). Empleado en el calculo de expresiones regulares
        para con el automata, simplifica el automata utilizando eliminacion
        de estados hasta dejar solo estados iniciales y finales, como se
        indica en Hopcroft, J. et. al. (2007). Introduccion a la Teoria de
        Automatas, Lenguajes y Computacion.

        Returns
        -------
        None.

        """
        edos2reduce = self.estados.difference(
            self.estados_iniciales.union(self.estados_finales))
        for edo in edos2reduce:
            nodos_ant = set([
                vt['from']
                for vt in self.vertices
                if vt['to'] == edo and vt['from'] != vt['to']])
            nodos_suc = set([
                vt['to']
                for vt in self.vertices
                if vt['from'] == edo and vt['from'] != vt['to']])
            S = entradas2ER(self.__get_entradas(edo, edo))
            if S:
                S.requiereClausulaKleene = True
            for nin in nodos_ant:
                Q = entradas2ER(self.__get_entradas(nin, edo))
                for nout in nodos_suc:
                    R = entradas2ER(self.__get_entradas(nin, nout))
                    P = entradas2ER(self.__get_entradas(edo, nout))
                    if R:
                        self.__vertices = [
                            vt
                            for vt in self.vertices
                            if vt['from'] != nin or vt['to'] != nout]
                    new_vertice = deepcopy(Q)
                    if S:
                        new_vertice.concatenarTermino(deepcopy(S))
                    new_vertice.concatenarTermino(P)
                    if R:
                        new_vertice = TerminoER(terminos=[R, new_vertice])
                        self.__vertices.append({
                            'from': nin,
                            'to': nout,
                            'entradas': new_vertice.terminos})
                    else:
                        self.__vertices.append({
                            'from': nin,
                            'to': nout,
                            'entradas': [new_vertice]})
            self.__estados.remove(edo)
            self.__vertices = [
                vt
                for vt in self.vertices
                if vt['from'] != edo and vt['to'] != edo]

    @property
    def asRE(self) -> str:
        """
        Expresion regular equivalente al automata. Se calcula de forma "tonta"
        utilizando el metodo planteado en Hopcroft, J. et. al. (2007).
        Introduccion a la Teoria de Automatas, Lenguajes y Computacion.

        Raises
        ------
        TypeError
            En caso de que el automata no tenga estados inciales o bien si
            tiene mas de un estado inicial.

        Returns
        -------
        str.

        """
        if 1 != len(self.estados_iniciales):
            raise TypeError("El automata debe tener solo un estado inicial")
        autom = deepcopy(self)
        autom.__reduce_no_finales()
        nInicial = list(autom.estados_iniciales)[0]
        expresiones = []
        for edo in autom.estados_finales:
            autom_tmp = deepcopy(autom)
            autom_tmp.__finales = {edo}
            autom_tmp.__remover_inecesarios()
            autom_tmp.__reduce_no_finales()
            if edo == nInicial:
                er = entradas2ER(autom_tmp.__get_entradas(edo, edo))
                er.requiereClausulaKleene = True
            else:
                R = entradas2ER(autom_tmp.__get_entradas(nInicial, nInicial))
                S = entradas2ER(autom_tmp.__get_entradas(nInicial, edo))
                U = entradas2ER(autom_tmp.__get_entradas(edo, edo))
                T = entradas2ER(autom_tmp.__get_entradas(edo, nInicial))
                if U:
                    U.requiereClausulaKleene = True
                SU = None
                SUT = None
                if S:
                    SU = deepcopy(S)
                    SU.concatenarTermino(U)
                    if T:
                        SUT = deepcopy(SU)
                        SUT.concatenarTermino(T)
                er = TerminoER(terminos=[R, SUT], reqKleene=True)
                if 0 < len(er.terminos):
                    er.concatenarTermino(SU)
                else:
                    er = SU
            expresiones.append(er)
        return str(TerminoER(terminos=expresiones))
