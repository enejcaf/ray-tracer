import numpy as np
import matplotlib.pyplot as plt
from progress.bar import ChargingBar

def normalize(vector):
    return vector / np.linalg.norm(vector)

def reflected(vector, axis, n1, n2):
    #n1=1. za zrak
    #n2=1.52 za steklo
    #vpadni kot:
    #fi1 = np.arccos(np.dot(normalize(vector), normalize(axis)))
    #sin(arccos(x))=(1-x^2)^0.5
    x=np.dot(normalize(vector), normalize(axis))
    sin_fi1=(1. - x**2.)**0.5
    #odbojni ali lomni kot:
    #fi2 = np.arcsin(np.sin(fi1)*n2/n1)
    sin_fi2 = (sin_fi1 * n2 / n1)
    #projekcija na normalo:
    Proj_axis = vector - np.dot(vector, axis) * axis
    #kritični kot je pogoj za odboj
    if sin_fi1 >= (n2/n1):
        #return np.sin(fi2)*(axis)+np.cos(fi2)*Proj_axis
        return -sin_fi2*(axis) + (1-sin_fi2**2) * Proj_axis
    else:
        #return np.sin(fi2)*(axis)+np.cos(fi2)*Proj_axis
        return sin_fi2 * (axis) + (1-sin_fi2**2) * Proj_axis
    #return vector - 2 * np.dot(vector, axis) * axis

def sphere_intersect(center, radius, ray_origin, ray_direction):
    '''
    Iskanje presečišč na krogli v izhodišču, zato odštevamo vektor središča (center).
    '''
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None

def rot(axis, sin_theta, cos_theta):
    """
    Rodriguezova formula predelana na vhodna podatka cos in sin kota.
    """
    axis = np.asarray(axis)
    axis = axis / (np.dot(axis, axis))**0.5
    a = ((cos_theta+1.)/2.)**0.5  #math.cos(theta / 2.0)
    b, c, d = -axis * sin_theta/(2*a) #-axis*math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def cylinder_intersect(center, radius, height, axis, ray_origin, ray_direction):
    '''
    Kot pri krogli problem rešujemo v izhodišču poleg tega pa še zarotiramo vektorje, tako da je valj pokončen.
    Množenje matrik prispeva k časovni zahtevnosti reševanja.
    '''
    #cos_fi=np.dot(normalize(axis), normalize(0,0,1))
    if normalize(axis)[2]==1:
        R = np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
    else:
        cos_fi = normalize(axis)[2]
        rot_axis = np.array([normalize(axis)[1], -normalize(axis)[0], 0])
        sin_fi = np.linalg.norm(rot_axis)
        R = rot(rot_axis, sin_fi, cos_fi)
    ray_direction2=np.matmul(R, (ray_direction))
    ray_origin2=np.matmul(R, (ray_origin - center))
    a = np.linalg.norm(ray_direction2)**2 - np.fabs(ray_direction2[2])**2
    b = 2 * np.dot(ray_direction2, ray_origin2) - 2*ray_direction2[2] * ray_origin2[2]
    c = np.linalg.norm(ray_origin2)**2 - np.fabs(ray_origin2[2])**2 - radius ** 2
    delta = b ** 2 - 4 *a*c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / (2*a)
        t2 = (-b - np.sqrt(delta)) / (2*a)
        #če si želimo zaprt cilinder imamo še enačbi za kapice:
        #t3 = (z_min-(ray_origin[2]-center[2]))/ray_direction[2]
        #t4 = (z_max-(ray_origin[2]-center[2]))/ray_direction[2]
        #potem dodamo še pogoja za kapice, kjer upoštevamo, da se lahko zgodi da imamo
        #hkrati sekanje čez obe kapici, ali pa imamo sekanje dvakrat
        #čez plašč, ali pa imamo sekanje enkrat čez plašč in enkrat čez kapico.

        z1 = ray_origin2[2]+t1*ray_direction2[2]
        z2 = ray_origin2[2]+t2*ray_direction2[2]

        if (z1 > -height/2 and z1 < height/2) and (z2 > -height/2 and z2 < height/2):
            if t1 > 0 and t2 > 0:
                return min(t1, t2)

        elif z1>-height/2 and z1<height/2:
            if t1>0:
                return t1
        elif z2>-height/2 and z2<height/2:
            if t2>0:
                return t2

    return None

def cone_intersect(center, height, axis, ray_origin, ray_direction):
    if normalize(axis)[2]==1:
        R=np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
    else:
        cos_fi = normalize(axis)[2]
        rot_axis = np.array([normalize(axis)[1], -normalize(axis)[0], 0])
        sin_fi = np.linalg.norm(rot_axis)
        R = rot(rot_axis, sin_fi, cos_fi)

    ray_direction2 = np.matmul(R,(ray_direction))
    ray_origin2 = np.matmul(R ,(ray_origin - center))
    a = ray_direction2[0]**2+ray_direction2[1]**2-ray_direction2[2]**2
    b = 2 * np.dot(ray_direction2, ray_origin2) - 4*ray_direction2[2]*(ray_origin2)[2]
    c = np.linalg.norm(ray_origin2) ** 2 - 2*(ray_origin2)[2] ** 2
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / (2 * a)
        t2 = (-b - np.sqrt(delta)) / (2 * a)
        z1=(ray_origin2[2] + t1 * ray_direction2[2])
        z2=(ray_origin2[2] + t2 * ray_direction2[2])
        if (z1 > 0 and z1 < height) and (z2 > 0 and z2 < height):
            if t1 > 0 and t2 > 0:
                return min(t1, t2)

        elif z1 > 0 and z1 < height:
            if t1>0:
                return t1
        elif z2 > 0 and z2 < height:
            if t2 > 0:
                return t2
    return None


def plane_intersect(n, r_0, ray_origin, ray_direction):
    '''
    Poišče presečišče z ravnino. Ravnina je definirana kot n \cdot (r - r_0)=0, kjer je n normala in r_0 poljubna točka ravnine.
    Pri objektih je normala definirana s ključem 'normal', točka pa s 'center', zaradi ujemanja z drugimi telesi.
    '''
    t = np.dot(n, r_0 - ray_origin) / np.dot(n, ray_direction)
    if t>=0:
        return t
    else:
        return None


def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = []
    for obj in objects:
        if obj['type'] == 'ball':
            distances.append(sphere_intersect(obj['center'], obj['radius'], ray_origin, ray_direction))
        elif obj['type'] == 'cylinder':
            distances.append(cylinder_intersect(obj['center'], obj['radius'], obj['height'], obj['direction'], ray_origin, ray_direction))
        elif obj['type'] == 'plane':
            distances.append(plane_intersect(obj['normal'], obj['point'], ray_origin, ray_direction))
        elif obj['type'] == 'cone':
            distances.append(cone_intersect(obj['center'], obj['height'], obj['direction'], ray_origin, ray_direction))


    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance

def slika(width, height, max_depth, camera, light, objects):
    #width = 300*2
    #height = 200*2

    #max_depth = 3
    '''
    camera = np.array([0, 0, 1])
    '''
    ratio = float(width) / height
    screen = (-1, 1 / ratio, 1, -1 / ratio) # left, top, right, bottom
    '''
    light = { 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }

    objects = [
        #{ 'type': 'ball', 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 },
        #{ 'type': 'ball', 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52},
        {'type': 'cylinder', 'center': np.array([-0.2, 0.2, -0.4]), 'radius': 0.5, 'height': 0.6, 'direction': np.array([0.2, 1, 0.2]), 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52},
        #{ 'type': 'ball', 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 },
        { 'type': 'plane', 'normal': np.array([0, 1, 0]), 'point': np.array([0, -1, 0]), 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1},
        { 'type': 'cone', 'center': np.array([-0.3, 0.2, -0.8]), 'height': 0.5, 'direction': np.array([0,-2,1]), 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 }
    ]
    '''

    image = np.zeros((height, width, 3))

    bar = ChargingBar('Processing', max=height)
    for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            # screen is on origin
            pixel = np.array([x, y, 0])
            origin = camera
            direction = normalize(pixel - origin)

            color = np.zeros((3))
            reflection = 1

            for k in range(max_depth):
                # check for intersections
                nearest_object, min_distance = nearest_intersected_object(objects, origin, direction)
                if nearest_object is None:
                    break

                intersection = origin + min_distance * direction
                if nearest_object['type'] == 'ball':
                    normal_to_surface = normalize(intersection - nearest_object['center'])
                elif nearest_object['type'] == 'cylinder':
                    #normal_to_surface = normalize(intersection - nearest_object['center'])
                    v1 = intersection - nearest_object['center']
                    normal_to_surface = normalize(v1 - (np.dot(v1, normalize(nearest_object['direction']))) * normalize(nearest_object['direction']))
                elif nearest_object['type'] == 'plane':
                    normal_to_surface = normalize(nearest_object['normal'])
                elif nearest_object['type'] == 'cone':
                    #ker gre za stožec z enako višino kot maksimalnim radijem, se zadeve poenostavijo, saj je normala pod kotom 45 stopinj
                    h1 = normalize(nearest_object['direction'])
                    v1 = normalize(intersection-nearest_object['center'])
                    x1 = normalize(np.sqrt(2)*nearest_object['height']*v1-nearest_object['height']*h1)
                    normal_to_surface = (np.sqrt(2) / 2) * x1 - (np.sqrt(2) / 2) * h1

                shifted_point = intersection + 1e-5 * normal_to_surface
                intersection_to_light = normalize(light['position'] - shifted_point)

                _, min_distance = nearest_intersected_object(objects, shifted_point, intersection_to_light)
                intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
                is_shadowed = min_distance < intersection_to_light_distance

                if is_shadowed:
                    break

                illumination = np.zeros((3))

                # ambient
                illumination += nearest_object['ambient'] * light['ambient']

                # diffuse
                illumination += nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)

                # specular
                intersection_to_camera = normalize(camera - intersection)
                H = normalize(intersection_to_light + intersection_to_camera)
                illumination += nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (nearest_object['shininess'] / 4)

                # reflection
                color += reflection * illumination
                reflection *= nearest_object['reflection']

                origin = shifted_point
                direction = reflected(direction, normal_to_surface, 1., nearest_object['n2'])

            image[i, j] = np.clip(color, 0, 1)
        yield image
        #v programu: trenutna_slika = slika().next()
        bar.next()
    bar.finish()
    #plt.imshow(image)
    #plt.show()
    plt.imsave('imageOriginal.png', image)

'''
slika(300*1,200*1,3)

'''
