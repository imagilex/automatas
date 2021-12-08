"""
Funciones necesarias para la ejecucion del automata en un entorno web
(utilizando flask) para la implementacion de la UI
"""

from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from Automata import Automata, caracter_vacio
import site_helpers as hp
from werkzeug.utils import secure_filename
from random import randint
import os


UPLOAD_FOLDER = 'data' # /ruta/a/la/carpeta
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/automata-0/')
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

@app.route('/', methods=['POST', 'GET'])
def upload_automata():
    if request.method == 'POST':
        estados = request.form['estados']
        file = request.files['archivo']
        if file and allowed_file(file.filename):
            filename = "matriz_nueva.csv"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('test_automata', estados=estados))
        else:
            mensaje= "Extensión de archivo no valida"
            return render_template("upload_automata.html", mensaje=mensaje)
    else:
        return render_template("upload_automata.html", mensaje="")

@app.route('/test_automata/', methods=['POST', 'GET'])
def test_automata():
    estados = request.args['estados']
    estado_final = 'q'+estados
    automataAFN_test= Automata(['q0'], [estado_final],'data/matriz_nueva.csv')
    automataAFD_test = automataAFN_test.AFN2AFD
    rndnum = randint(1,100000)
    imgAFN = f"img/autom_{rndnum}_AFN"
    imgAFD = f"img/autom_{rndnum}_AFD"
    automataAFN_test.save_png(f"static/{imgAFN}")
    automataAFD_test.save_png(f"static/{imgAFD}")
    return render_template(
        "test_automata.html",
        er_AFN=automataAFN_test.asRE, er_AFD=automataAFD_test.asRE,
        imgAFD=imgAFD + ".png", imgAFN=imgAFN + ".png",
        resultados_pruebas_test=hp.check_words(
            hp.mk_test_lst2(automataAFN_test.alfabeto,len(automataAFN_test.estados), 2**len(automataAFN_test.estados), caracter_vacio),
            {'AFN': automataAFN_test, 'AFD': automataAFD_test}),
        car_vacio=caracter_vacio, car_vacio_code=ord(caracter_vacio))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename,
        as_attachment=True,attachment_filename='matriz.csv')

if "__main__" == __name__:
    app.run()
