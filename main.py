#!/usr/bin/env python3
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


from Automata import Automata
from random import randint
from tabulate import tabulate


automataAFN = Automata(['q0'], ['q5'], 'automata_decimales.csv')
automataAFN.save_png("automata_decimales_AFN")
automataAFD = automataAFN.AFN2AFD
automataAFD.save_png("automata_decimales_AFD")

palabras = [
    '-907.988', '252.865', '269.26', '543.21',
    '+637', '-201.685', '718.84', '+614.204',
    '663324', '+801.776', '323.593', '-.995',
    '-500.378', '-492.55', '675.9', '900.881',
    '+641.591', '-33', '130.211', '437.775',
    '+796271', '366.754', '+944.312', '-468.231',
    '-177.612', ]

test_results = []

for palabra in palabras:
    rAFN = automataAFN.verificar_palabra(palabra)
    rAFD = automataAFD.verificar_palabra(palabra)
    test_results.append([
        palabra,
        rAFN,
        rAFD,
        "Ok" if rAFN == rAFD else "Error"])
for x in range(25):
    palabra = ''
    if randint(1, 3) == 1:
        palabra += '+'
    elif randint(1, 2) == 1:
        palabra += '-'
    if randint(1, 10) <= 9:
        palabra += str(randint(0, 1000))
    if randint(1, 10) <= 9:
        palabra += '.'
    if randint(1, 10) <= 9:
        palabra += str(randint(0, 1000))
    rAFN = automataAFN.verificar_palabra(palabra)
    rAFD = automataAFD.verificar_palabra(palabra)
    test_results.append([
        palabra,
        rAFN,
        rAFD,
        "Ok" if rAFN == rAFD else "Error"])
print(tabulate(
    test_results,
    headers=['Palabra', 'Res AFN', 'Res AFD', "Res ="],
    tablefmt='fancy_grid',
    showindex=True))

print(f"{automataAFN.asRE =}")
print(f"{automataAFD.asRE =}")

automata = Automata(['A'], ['C', 'D'], 'ejemplo_2.csv')
automata.save_png("automata")
print(f"{automata.asRE =}")
print(f"{automata.AFN2AFD.asRE =}")