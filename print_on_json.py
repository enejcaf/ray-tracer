#/usr/bin/env python3
import json
import numpy as np
from numpyencoder import NumpyEncoder

def print_json(objekti, svetila, kamera, zaslon, ime):
    '''
    Zapiše vhodne parametre v obliko datoteke ime.json
    Input:
    objekti: seznam slovarjev za posamezne objekte. Primer:
            objekti = [
              { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
              { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
              { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 }
            ]

    svetila: seznam slovarjev za svetila. Primer:
            svetila = [{ 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }]
    kamera: seznam slovarja za kamero. Podana le lega.
    zaslon: seznam slovarja za kamero. Podana širina in višina zaslona.

    ime: niz (str), ki predstavlja ime datoteke na katero pišemo. Če datoteka
            ne obstaja, jo program ustvari sam.
    '''

    with open(ime, 'w+') as f:
        json.dump({'objekti': objekti, 'svetila': svetila, 'kamera': kamera, 'zaslon': zaslon}, f, indent=4, sort_keys=True, separators=(', ', ': '), ensure_ascii=False, cls=NumpyEncoder)
    f.close()

def read_json(ime):
    '''
    Vrne sezname slovarjev za objekte, svetila, kamero in zaslon.

    Input:
    ime: niz (str) imena datoteke iz katere želimo brati

    return:
        objekti: seznam slovarjev
        svetila: seznam slovarjev
        kamera: seznam slovarjev
        zaslon: seznam slovarjev
    '''

    with open(ime, 'r') as f:
        data = json.load(f)
    f.close()

    objekti=data['objekti']
    svetila=data['svetila']
    kamera=data['kamera']
    zaslon=data['zaslon']
    #print(data['objekti'])
    #print(data['svetila'])

    return objekti, svetila, kamera, zaslon

#read_json('vhod_primer.json')

#Testiranje funkcije:
'''
objekti = [
  { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
  { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
  { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 }
]
svetila = [{ 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }]
kamera = [{'position': np.array([0, 0, 1])}]
zaslon = [{'width': 600, 'height': 400}]
'''
#print_json(objekti, svetila, kamera, zaslon, 'vhod_primer.json')
