# TFG

Explicació:

Amb el codi de Python, envio missatges al PORT COM6, el dispositiu solicitador detecta la comanda amb Arduino i envia un paquet al dispositiu Enviador indicant que ha de fer.

Es generen arxius .csv amb les dades, que serà útil per generar un gràfic.


Bugs per solucionar:

- Al connectar per primera vegada la placa, envia una línía de bytes que no es sempre la mateixa (crec), el programa ha de saltar-la.
- Quan hi ha transmissió i un paquet falla, no incluir-ho al fitxer .csv

Coses per afegir:

- Millorar optimització codi
- Fer millor els gràfics
- Fer pantalla amb més informació sobre els gràfics
- Fer línea amb el model de propagació i veure la variança de la funció.
- Realitzar el codi dels apartats 4 i 5 amb la llibreria Pandas

Actualitzacions

7/2/2023 He descobert la llibreria Pandas, he fet l'apartat 6 del menú utilitzant aquesta llibreria, falta implementar a 4 i 5.

8/2/2023 Actualització codi apartat 5.
