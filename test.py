import animation as ani
import body
import math
import copy

# Earth
earth_set = {
    "pos": [6.744778068264060E+07, 1.302994293719669E+08],
    "label": "earth"
}
earth = body.Body(pos=earth_set["pos"], label=earth_set["label"])
#-----------------------------------------------------------------------
# Mars
mars_set = {
    "pos": [-2.938171357055589E+07, -2.190407176449395E+08],
    "label": "mars"
}
mars = body.Body(pos=mars_set["pos"], label=mars_set["label"])
#-----------------------------------------------------------------------
# Mercury
mercury_set = {
    "pos": [1.954828063374393E+06, 4.508317558219616E+07],
    "label": "mercury"
}
mercury = body.Body(pos=mercury_set["pos"], label=mercury_set["label"])
#-----------------------------------------------------------------------
# Venus
venus_set = {
    "pos": [-8.548957050643057E+07, -6.760761371329141E+07],
    "label": "venus"
}
venus = body.Body(pos=venus_set["pos"], label=venus_set["label"])
#-----------------------------------------------------------------------
# Neptune
neptune_set = {
    "pos": [4.468725763116714E+09, 5.932802468104235E+07],
    "label": "neptune"
}
neptune = body.Body(pos=neptune_set["pos"], label=neptune_set["label"])
#-----------------------------------------------------------------------
# Saturn
saturn_set = {
    "pos": [1.424009164827680E+09, 6.920852658702333E+06],
    "label": "saturn"
}
saturn = body.Body(pos=saturn_set["pos"], label=saturn_set["label"])
#-----------------------------------------------------------------------
# Jupiter
jupiter_set = {
    "pos": [-2.135512992034739E+08, 7.470909244637821E+08],
    "label": "jupiter"
}
jupiter = body.Body(pos=jupiter_set["pos"], label=jupiter_set["label"])
#-----------------------------------------------------------------------
# Uranus
uranus_set = {
    "pos": [1.496499774886272E+09, 2.502327876676484E+09],
    "label": "uranus"
}
uranus = body.Body(pos=uranus_set["pos"], label=uranus_set["label"])
#-----------------------------------------------------------------------

planet_set = [mercury, mars, earth, venus, jupiter, saturn, uranus, neptune]

def animation_test():
    time_steps_set = []
    time_steps_set.append(planet_set)

    for _ in range(100):
        set_copy = copy.deepcopy(time_steps_set[-1])
        for body in set_copy:
            pos_arr = []
            pos_arr.append(body.position[0] * 1.01)
            pos_arr.append(body.position[1] * 1.01)
            body.set_pos(pos_arr)
        time_steps_set.append(set_copy)

    animation = ani.Animation(time_steps_set)
    animation.animate(center="susn")
    

animation_test()
