from manim import *

def get_gray_blob(z=100, opacity=0.75):
    return Square(fill_opacity=1, color=BLACK).set_opacity(opacity).set_z_index(z).scale(10000)
