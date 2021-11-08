"""
Funciones de apoyo para la contextualizacion y uso de la clase Automata para
con la UI
"""
from os.path import isfile
from tabulate import tabulate
from random import randint, choice
from math import ceil, floor
from captcha.image import ImageCaptcha
from hashlib import blake2b
from os import remove, path
from collections import Iterable
from typing import Optional
from Automata import Automata


def check_img_automata(automata: Automata, file: str):
    """
    Verifica si se ha generado el archivo correspondiente a un automata, en
    caso de que no sea asi crea un archivo *.png con la representacion visual
    del automata

    Parameters
    ----------
    automata : Automata
        Automata del cual se verificara la existencia de su represntacion
        visual.
    file : str
        Archivo a validar de existencia o a ejecutar su creacion, no es
        necesario agregar la extension del archivo.

    Returns
    -------
    None.

    """
    if not isfile(f'static/img/{file}.png'):
        automata.save_png(f"static/img/{file}")


def check_words(palabras: Iterable[str], automatas: Iterable[Automata]) -> str:
    """
    Verifica, para cada palabra en la lista de palabras, si pertenecen al
    lenguaje generado por los automatas

    Parameters
    ----------
    palabras : array like
        Lista de palabras a revisar.
    automatas : dict
        Diccionario con los automatas y su nombre para con los cuales se
        realizara la validacion de palabras.

    Returns
    -------
    str
        Cadena HTML que representa una tabla en la cual se incluyen los
        resultados de la validacion de las palabras.

    """
    resultados = []
    for palabra in palabras:
        palabra = palabra.replace('\r', '')
        if "" == palabra:
            continue
        res_eq = True
        current_res = None
        res = [palabra, ]
        for key, automata in automatas.items():
            res_automata = automata.verificar_palabra(palabra)
            res.append(res_automata)
            if current_res is None:
                current_res = res_automata
            res_eq = res_eq and res_automata == current_res
            current_res = res_automata
        res.append("Ok" if res_eq else "Error")
        resultados.append(res)
    headers = ['Palabra'] + list(automatas.keys()) + ["Res Iguales"]
    return tabulate(
        resultados, headers=headers, tablefmt="html", showindex=True)


def mk_test_word() -> str:
    """
    Crea una palabra semialeatoria orientada a pertenecer al lenguaje del
    automata

    Returns
    -------
    str.

    """
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
    return palabra


def mk_test_lst(
        alfabeto: set, largo_palabra: int, vacio: Optional[set] = set(),
        test_size: Optional[int] = 50) -> list:
    """
    Genera una lista de palabras, 75% de ellas son semialeatorias orientadas a
    pertenecer al lenguaje del automata y el 25% de ellas son palabras
    completamente aleatorias generadas usando un alfabeto determinado

    Parameters
    ----------
    alfabeto : set
        Alfabeto sobre el cual se generaran las palabras aleatorias.
    largo_palabra : int
        Longitud de las palabras a generar.
    vacio : set, optional
        Conjunto de caracteres a usar como cadena vacia (epsilon).
        Default set().
    test_size : int, optional
        Total de palabras a generar en la lista. Default 50.

    Returns
    -------
    list.

    """
    return [
               mk_test_word()
               for x in range(ceil(test_size * 0.75))
           ] + [
                "".join([
                    choice(list(alfabeto.difference(vacio)))
                    for x in range(largo_palabra)
                ])
                for x in range(floor(test_size * 0.25))
           ]


def create_captcha() -> str:
    """
    Generador de imagen captcha para impedir que robots web hagan trabajar
    la app

    Returns
    -------
    str
        cadena encriptada del texto en el captcha.

    """
    digitos = [chr(x) for x in range(48, 58)]
    letras = [chr(x) for x in range(97, 123)]
    txt = "".join([choice(digitos + letras) for x in range(5)])
    h = blake2b(digest_size=20)
    h.update(txt.encode('utf-8'))
    txtsha = h.hexdigest()
    img = ImageCaptcha(280, 90)
    img.write(txt, f"static/captcha/{txtsha}.png")
    return txtsha


def check_captcha(captcha: str, captcha_value: str) -> bool:
    """
    Valida el captcha enviado al usuario contra el ingresado por el usuario
    y elimina la imgane png correspondiente a ese captcha

    Parameters
    ----------
    captcha : str
        codigo encriptado del captcha.
    captcha_value : str
        captcha capturado por el usuario.

    Returns
    -------
    bool.

    """
    h = blake2b(digest_size=20)
    h.update(captcha_value.encode('utf-8'))
    txtsha = h.hexdigest()
    if path.exists(f"static/captcha/{captcha}.png"):
        remove(f"static/captcha/{captcha}.png")
    return txtsha == captcha
