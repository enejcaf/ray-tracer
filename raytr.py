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
    sin_fi1=(1.-x**2.)**0.5
    #odbojni ali lomni kot:
    #fi2 = np.arcsin(np.sin(fi1)*n2/n1)
    sin_fi2 = (sin_fi1*n2/n1)
    #projekcija na normalo:
    Proj_axis = vector - np.dot(vector, axis) * axis
    #kritični kot je pogoj za odboj
    if sin_fi1 >= (n2/n1):
        #return np.sin(fi2)*(axis)+np.cos(fi2)*Proj_axis
        return -sin_fi2*(axis)+(1-sin_fi2**2)*Proj_axis
    else:
        #return np.sin(fi2)*(axis)+np.cos(fi2)*Proj_axis
        return sin_fi2*(axis)+(1-sin_fi2**2)*Proj_axis
    #return vector - 2 * np.dot(vector, axis) * axis

def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None

def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [sphere_intersect(obj['center'], obj['radius'], ray_origin, ray_direction) for obj in objects]
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

    #camera = np.array([0, 0, 1])
    ratio = float(width) / height
    screen = (-1, 1 / ratio, 1, -1 / ratio) # left, top, right, bottom

    #light = { 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }
    '''
    objects = [
        { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 },
        { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52},
        { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 },
        { 'center': np.array([0, -9000, 0]), 'radius': 9000 - 0.7, 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.4}
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
                normal_to_surface = normalize(intersection - nearest_object['center'])
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
    #plt.show(image)
    #plt.imsave('imageOriginal.png', image)

'''
gen=slika(300*1,200*1,3)
i=0
while i<500:
    img=next(gen)
    if i%50==0:
        plt.imshow(img)
        plt.show()
    i+=1
'''
