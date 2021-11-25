# Autómatas y Lenguaje Natural

***

Ejecución local con flask:

Ubuntu
~~~
export FLASK_ENV=development
export FLASK_APP=app.py
python -m flask run
~~~

Windows
~~~
set FLASK_ENV=development
set FLASK_APP=app.py
python -m flask run
~~~

***

A partir de la clase Automata es posible:

- Generar el automata gráficamente y guarda el *.png
- Obtener del alfabeto en automatico
- Ejecutar la funcion de transición
- Ejecular la transición extendida
- Realizar verificación de palabras
- Transformación de AFN a AFD
- Obtención de Expresión Regular

***

Implementado en: https://mia.imagilex.com.mx/automata-decimales

El automata puede o no tener transiciones de palabra vacía.

Se transformaba de AFN a AFD con el método planteado en Hopcroft, J. et. al. (2007). *Introduccion a la Teoria de Automatas, Lenguajes y Computacion*. Y la obtención de la expresión regular, por el método planteado en el mismo libro, el cual es eliminación de estados, se realiza una mejora a la generación de la expresión regular que consiste en verificar un poco la complejidad de cada nodo a eliminar en el método. Para esta mejora se implemento una complejidad de cada nodo, basado en cuantos nodos te dirigen al nodo del cual quieres calcular su complejidad y a cuantos nodos puedes moverte desde dicho nodo, además de la implementación de Dijkstra para determinar que tán lejos se encuentra un nodo del nodo de aceptación, siendo más complejos aquellos que estan más alejados.
