import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def ball(center, r):
    n = 200
    #Pripravimo 100 točk:
    theta = np.linspace(0,2*np.pi, n)
    phi = np.linspace(0,np.pi, n)

    #koordinate krogle
    x = center[0] * np.ones((n,n)) + r * np.outer(np.cos(theta),np.sin(phi))
    y = center[1] * np.ones((n,n)) + r * np.outer(np.sin(theta),np.sin(phi))
    z = center[2] * np.ones((n,n)) + r * np.outer(np.ones(n),np.cos(phi))

    #krogle ni treba rotirati

    return x, y, z


def normalize(vector):
    return vector / np.linalg.norm(vector)

def rot(axis, sin_theta, cos_theta):
    """
    Rodriguezova formula predelana na vhodna podatka cos in sin kota.
    """
    axis = np.asarray(axis)
    axis = axis / (np.dot(axis, axis))**0.5
    a = ((cos_theta+1.) / 2.)**0.5   #np.cos(theta / 2.0)
    b, c, d = -axis * sin_theta / (2 * a) #-axis*np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])



def cylinder(center, axis, r, hmax):
    """
    paramterizacija valja s središčem (vektor center), usmerjenostjo (vektor axis), radijem (r), maksimalno višino (hmax).
    """
    #cos_fi=np.dot(normalize(axis), normalize(0,0,1))
    if normalize(axis)[2]==1:
        R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    else:
        cos_fi = normalize(axis)[2]
        rot_axis = np.array([normalize(axis)[1], -normalize(axis)[0], 0])
        sin_fi = np.linalg.norm(rot_axis)
        R = rot(rot_axis, sin_fi, cos_fi)


    fi = np.linspace(0,2*np.pi, 50) #točke kroga
    h = np.linspace(0,hmax, 20) #toče za višino
    x = r*np.outer(np.sin(fi), np.ones(len(h))) # x value repeated 20 times
    y = r*np.outer(np.cos(fi), np.ones(len(h))) # y value repeated 20 times
    z = -hmax / 2 * np.ones((len(fi), len(h)))+np.outer(np.ones(len(fi)), h) # x,y corresponding height

    #mnozimo v Einsteinovi notaciji tako, kot da so x, y, z števila in seštejemo po celem stolpcu
    vec_R=np.einsum('ij,jkl', R, np.stack((x, y, z)))
    return vec_R[0]+center[0],vec_R[1]+center[1],vec_R[2]+center[2]

def cone(center, axis, h):
    #cos_fi=np.dot(normalize(axis), normalize(0,0,1))
    if normalize(axis)[2] == 1:
        R=np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
    else:
        cos_fi = normalize(axis)[2]
        rot_axis = np.array([normalize(axis)[1], -normalize(axis)[0], 0])
        sin_fi = np.linalg.norm(rot_axis)
        R = rot(rot_axis, sin_fi, cos_fi)

    #center je pozicija vrha
    radi = h
    height = h

    #Polarne koordinate
    phi = np.linspace(0, 2*np.pi, 50)
    r = np.linspace(0, h, 50)

    #Poračunamo kartezične
    x = np.outer(r,np.cos(phi))
    y = np.outer(r,np.sin(phi))
    z = ((np.sqrt((x)**2 + (y)**2)/(radi/height)))

    #mnozimo v Einsteinovi notaciji tako, kot da so x, y, z števila in seštejemo po celem stolpcu
    vec_R = np.einsum('ij,jkl', R, np.stack((x, y, z)))
    return vec_R[0] + center[0], vec_R[1] + center[1], vec_R[2] + center[2]

def plane(normal, r0):
    n=3 #velikost ravnine
    if normal[2] > 0:
        x, y = np.meshgrid(range(n), range(n))
        x, y = x - n / 3 * np.ones(n), y - n / 3 * np.ones(n)
        z = (np.dot(r0, normal) - x * normal[0] - y * normal[1]) / normal[2]
        return x, y, z
    elif normal[1] > 0:
        x, z = np.meshgrid(range(n), range(n))
        x, z = x - n / 3 * np.ones(n), z - n / 3 * np.ones(n)
        y = (np.dot(r0, normal) - x * normal[0] - z * normal[2]) / normal[1]
        return x, y, z
    elif normal[0] > 0:
        y, z = np.meshgrid(range(n), range(n))
        y, z = y - n / 3 * np.ones(n), z - n / 3 * np.ones(n)
        x = (np.dot(r0, normal) - y * normal[1] - z * normal[2]) / normal[0]
        return x, y, z

def plot_objects(objekti, camera, pokazi):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection ='3d')

    for obj in objekti:
        if obj['type'] == 'ball':
            clr=np.floor(2550*obj['ambient'])
            c=rgb_to_hex((int(clr[0]), int(clr[1]), int(clr[2])))
            x,y,z=(ball(obj['center'], obj['radius']))

            ax.plot_surface(x, y, z, color='#'+c)


        elif obj['type'] == 'cylinder':

            clr=np.floor(2550*obj['ambient'])
            c=rgb_to_hex((int(clr[0]), int(clr[1]), int(clr[2])))

            x,y,z=(cylinder(obj['center'], obj['direction'], obj['radius'], obj['height']))

            ax.plot_surface(x, y, z, color='#'+c)

        elif obj['type'] == 'plane':
            clr=np.floor(2550*obj['ambient'])
            c=rgb_to_hex((int(clr[0]), int(clr[1]), int(clr[2])))

            x,y,z=(plane(obj['normal'], obj['point']))

            ax.plot_surface(x, y, z, color='#'+c)
        elif obj['type'] == 'cone':
            clr = np.floor(2550*obj['ambient'])
            c = rgb_to_hex((int(clr[0]), int(clr[1]), int(clr[2])))

            x, y, z=(cone(obj['center'], obj['direction'], obj['height']))

            ax.plot_surface(x, y, z, color='#'+c)


    ax.set_xlabel('x', linespacing=3.2)
    ax.set_ylabel('y', linespacing=3.2)
    ax.set_zlabel('z', linespacing=3.2)
    #plt.title('Shema postavitve')

    #izračun azimuta
    #projekcija v ravnino:
    e1 = np.array([1,0,0])
    e2 = np.array([0,1,0])
    e3 = np.array([0,0,1])

    if np.dot(e1, camera) == 0 and np.dot(e2, camera) == 0:
        alpha = 90
        A = -90

    else:
        proj_xy=np.dot(e1, camera)*e1+np.dot(e2, camera)*e2
        cos_alpha=np.dot(normalize(proj_xy),e1)
        alpha=np.arccos(cos_alpha)

        cos_A=np.dot(normalize(camera), e3)
        A=np.arccos(cos_A)

    ax.view_init(A, alpha)
    plt.tight_layout(pad = 0)
    plt.savefig('predogled.png', bbox_inches='tight', pad_inches=0)
    if pokazi ==1 :
        plt.show()

'''
objects = [
        { 'type': 'ball', 'center': np.array([-0.2, 0, -1]), 'radius': 0.4, 'ambient': np.array([0.1, 0.1, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 },
        { 'type': 'ball', 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52},
        {'type': 'cylinder', 'center': np.array([-0.2, 0.2, -0.4]), 'radius': 0.5, 'height': 0.6, 'direction': np.array([1, 0.1, 0]), 'ambient': np.array([0.1, 0.0, 0.0]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52},
        { 'type': 'ball', 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 },
        { 'type': 'plane', 'normal': np.array([0, 0, 1]), 'point': np.array([0, -1, 0]), 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1},
        { 'type': 'cone', 'center': np.array([-0.3, 0.2, -0.8]), 'height': 0.5, 'direction': np.array([0,-2,1]), 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 }
    ]
camera = np.array([0, 0, 1])
plot_objects(objects, camera, 1)
'''
