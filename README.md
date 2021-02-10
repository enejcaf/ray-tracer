# ray-tracer
The idea behind the algorithm is taken step by step from Roman Aflak, who published "Ray Tracing From Scratch in Python" [Published: Jul 26, 2020. Source:  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9], with some additions to the code. Simple "ray tracing" algorithm currently operates with spheres, where we can use a very large distant sphere as a plane. Description of object is with a dictionary for example: {'center': np.array([0, 0, 0]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 }, where parameters represent center of a ball, its radius, and six parameters that are used in the light model: ambient, diffuse, specular, shininess, reflection and n2, where the first five ar from the Blinn-Phong reflection model, and the second one is used as refraction coefficient in Snell's law, where we assume that n outside of object is 1. If you want to add more objects create list of such dictionaries.

Pygame interface

The pygame interface is very simple to use. In main window you have to upload the ".json" file. You can create such file with function print_json(objects, light, camera, screen, file_name). Input parameters are for example:

(objects = [
    { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 },
    { 'center': np.array([0, -9000, 0]), 'radius': 9000 - 0.7, 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.4}
],

light = [{ 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }],
camera = [{'position': np.array([0, 0, 1])}],

screen = [{'width': 900, 'height': 600}]).

Once the file is uploaded you will be able to see the ground plan of the uploaded scene, where very large balls used as planes won't appear. Now you can add some additional balls to your file with clicking on button "Krogla". The coordinates and radius of the ball will be random numbers from 0 to 1, but you can easily edit this manualy in json file and upload the file again. Once you are satisfied with the scene, you can click "Nariši" and the picture will start appearing on the screen in real time. Because main program is generator you can manually change how often is the picture refreshed, because pygame window might stop responding, if you refresh too often. After the picture appears you can choose between buttons "Shrani" meaning save and "X" meaning close. If you perhaps clicked close instead of save, there is will still be a copy of a picture in file "trenutna.png" till you push "Nariši" again.
