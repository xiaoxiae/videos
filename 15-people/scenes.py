from manim import *
from random import uniform, seed, choice


#class MoveAlongPath(Animation):
#
#    def __init__(self, mobject: Mobject, path: VMobject, delay_before, delay_after, **kwargs) -> None:
#        self.path = path
#        self.delay_before = delay_before
#        self.delay_after = delay_after
#        super().__init__(mobject, **kwargs)
#
#    def interpolate_mobject(self, alpha: float) -> None:
#        def lerp(a, b, v):
#            return (b - a) * v + a
#
#        alpha = lerp(-self.delay_before, 1 + self.delay_after, alpha)
#        alpha = max(0, min(1, alpha))
#
#        point = self.path.point_from_proportion(self.rate_func(alpha))
#        self.mobject.move_to(point)
#        self.mobject.update()


class Path(VMobject):
    def __init__(self, points, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        """Returns the important points of the curve."""
        # shot explanation: Manim uses quadratic Bézier curves to create paths
        # > each curve is determined by 4 points - 2 anchor and 2 control
        # > VMobject's builtin self.points returns *all* points
        # > we, however, only care about the anchors
        # > see https://en.wikipedia.org/wiki/Bézier_curve for more details
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]

def DashedPath(*args, **kwargs):
    return DashedVMobject(Path(*args), **kwargs)


class Intro(MovingCameraScene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY

        grid_x = 3
        grid_y = 6

        grid = VGroup()

        self.camera.frame.scale(0.54)

        def distance(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (1/2)

        def distance_but_kinda_l(p1, p3):
            p2 = np.asarray([p1[0], p3[1], 0])

            return distance(p1, p2) + distance(p2, p3)

        def create_double_line_nodash(p_start, p_end, direction: bool):
            p1 = p_start

            if direction:
                p2 = np.asarray([p_start[0], p_end[1], 0])
            else:
                p2 = np.asarray([p_end[0], p_start[1], 0])

            p3 = p_end

            if len(p1) == 2:
                p1 = (p1[0], p1[1], 0)
            if len(p3) == 2:
                p3 = (p3[0], p3[1], 0)

            return Path([p1, p2, p3])

        def create_double_line(p_start, p_end, direction: bool):
            p1 = p_start

            if direction:
                p2 = np.asarray([p_start[0], p_end[1], 0])
            else:
                p2 = np.asarray([p_end[0], p_start[1], 0])

            p3 = p_end

            if len(p1) == 2:
                p1 = (p1[0], p1[1], 0)
            if len(p3) == 2:
                p3 = (p3[0], p3[1], 0)

            total_distance = distance(p1, p2) + distance(p2, p3)

            return total_distance, DashedPath([p1, p2, p3], num_dashes=int(total_distance * 10)).set_color(GRAY)

        stupid = [(-2, -2), (-1, -4), (-1, 4)]

        def get_id(obj):
            #if obj in stupid:
            #    return False
            return True

        def update_number(obj, dt, dot, start, goal, people):
            d = distance(start, obj.get_center()) * 2

            opacity = 1 if d > 0.5 else d
            opacity = min(opacity, distance(obj.get_center(), goal) * 2)

            d *= people

            obj.become(Tex(f"{d:.1f}").scale(0.5).set_opacity(opacity))

        def get_steps(places, place):
            total = 0

            x1, y1 = place
            for (x2, y2) in places:
                total += (abs(x1 - x2) + abs(y1 - y2)) * places[(x2, y2)]

            return total

        def find_optimal_meeting_place(places):
            min_steps = float('inf')
            min_pos = None

            for p in [(x, y) for x in range(-100, 100) for y in range(-100, 100)]:
                steps = get_steps(places, p)

                if steps < min_steps:
                    min_steps = steps
                    min_pos = p

            return min_pos

        places = {
            (2, -1): 3,
            (-2, 2): 6,
            (1, -5): 8,
            (2, 5): 9,
            (-2, -2): 1,
            (-1, -4): 3,
            (-1, 4): 5,
            (-0, -0): 10,
        }

        meeting_place = find_optimal_meeting_place(places)

        place_double_lines = {
            p:create_double_line(p, meeting_place, get_id(p))[1]
            for p in places
        }

        place_double_lines_dots = {
            p:Dot().move_to((p[0], p[1], 0))
            for p in places
        }

        place_double_lines_text = {
            p:Tex()
            for p in places
        }

        #for p in place_double_lines_text:
        #    place_double_lines_text[p].add_updater(
        #        lambda obj, dt: update_number(obj, dt, place_double_lines_dots[p], p, meeting_place, places[p]),
        #        call_updater=True
        #    )

        #    self.add(place_double_lines_text[p])

        place_double_lines_nodash = {
            p:create_double_line_nodash(p, meeting_place, get_id(p))
            for p in places
        }

        house_objects = {}

        for y in reversed(range(-grid_y, grid_y + 1)):
            for x in range(-grid_x, grid_x + 1):
                if (x, y) in places:
                    obj = VGroup(
                        SVGMobject("resources/house.svg").scale(0.35),
                        Tex(places[(x, y)], color=self.camera.background_color).set_opacity(0).scale(0.85).shift(DOWN * 0.06),
                    )

                    house_objects[(x, y)] = obj
                else:
                    obj = Dot().scale(0.5)

                obj.shift(RIGHT * x + UP * y)
                obj.set_z_index(10)

                grid.add(obj)

        self.play(FadeIn(grid, lag_ratio=0.01), run_time=1)

        self.play(AnimationGroup(*[AnimationGroup(house_objects[p][1].animate(run_time=0.5).set_opacity(1),
                                                  Flash(house_objects[p][1],
                                                        flash_radius=0.5,
                                                        line_length=0.1,
                                                        color=WHITE))
                                   for p in house_objects], lag_ratio=0.05))

        for p in place_double_lines_dots:
            place_double_lines_dots[p].set_z_index(1)

        def get_uniform(p):
            seed(id(p))
            return uniform(3, 4.5)

        self.play(
            *[
                FadeIn(place_double_lines[p], run_time=get_uniform(p))
                for p in place_double_lines
            ],
            *[
                MoveAlongPath(place_double_lines_dots[p], place_double_lines_nodash[p], run_time=get_uniform(p))
                for p in place_double_lines
            ],
            lag_ratio=1,
            rate_func=linear,
        )
