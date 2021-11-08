"""
Funciones necesarias para la ejecucion del automata en un entorno web
(utilizando flask) para la implementacion de la UI
"""

from flask import Flask, render_template, request
from Automata import Automata, caracter_vacio
import site_helpers as hp

app = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Renderizado de la pagina a mostrar en la url root ("/", index) sel sitio

    Crea los automatas y valida una serie de palabras aleatorias.

    Returns
    -------
    str.

    """
    automataAFN = Automata(['q0'], ['q5'], 'data/automata_decimales.csv')
    automataAFD = automataAFN.AFN2AFD
    hp.check_img_automata(automataAFN, 'automata_decimales_AFN')
    hp.check_img_automata(automataAFD, 'automata_decimales_AFD')
    return render_template(
        "index.html",
        er_AFN=automataAFN.asRE, er_AFD=automataAFD.asRE,
        resultados_pruebas=hp.check_words(
            hp.mk_test_lst(automataAFN.alfabeto, 10, caracter_vacio),
            {'AFN': automataAFN, 'AFD': automataAFD}),
        car_vacio=caracter_vacio, car_vacio_code=ord(caracter_vacio))


@app.route('/test-word/', methods=["GET", "POST"])
def test_word() -> str:
    """
    Renderizado de la pagina que permite al usuario validad sus propias
    palabras para con el automata

    Crea los automatas, valida las palabras ingresadas por el usuario en caso
    de que existan

    Returns
    -------
    str
    """
    palabras = None
    resultados_pruebas = ""
    right_captcha = True
    automataAFN = Automata(['q0'], ['q5'], 'data/automata_decimales.csv')
    automataAFD = automataAFN.AFN2AFD
    if request.method == 'POST':
        if hp.check_captcha(
                request.form['captcha'], request.form['captcha_value']):
            palabras = request.form['words2test']
            resultados_pruebas = hp.check_words(
                palabras.split('\n'),
                {'AFN': automataAFN, 'AFD': automataAFD})
        else:
            right_captcha = False
    hp.check_img_automata(automataAFN, 'automata_decimales_AFN')
    hp.check_img_automata(automataAFD, 'automata_decimales_AFD')
    return render_template(
        "test.html",
        er_AFN=automataAFN.asRE, er_AFD=automataAFD.asRE,
        palabras=palabras, resultados_pruebas=resultados_pruebas,
        car_vacio=caracter_vacio, car_vacio_code=ord(caracter_vacio),
        captcha=hp.create_captcha(), right_captcha=right_captcha)


if "__main__" == __name__:
    app.run()
