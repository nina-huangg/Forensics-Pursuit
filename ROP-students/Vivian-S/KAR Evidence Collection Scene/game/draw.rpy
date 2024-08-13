init -10 python in draw_logic:

    import os
    import io
    import math
    import hashlib
    import store
    import enum
    import pygame_sdl2 as pygame
    from os import path

    SAVE_FOLDER = path.abspath(renpy.config.basedir)
    GALLERY_REL_FOLDER = "_draw"
    COLOR_CIRCLE = "colors.png"
    DRAW_SAVE_NAME = "Draw"
    DRAW_EXT = ".png"

    VERSION = (1, 1, 3)


    class _DrawGallery(store.Gallery):

        __author__ = "Vladya"

        BACKGROUND = None

        def __init__(self):

            super(_DrawGallery, self).__init__()
            self.update_pictures()

        def update_pictures(self):

            for pic in self._get_pictures():

                name = pic.replace('/', '_')
                name = name.replace(' ', '_')
                name = name.replace('.', '_')

                if name in self.buttons:
                    continue

                images = []
                if self.BACKGROUND:
                    images.append(self.BACKGROUND)
                images.append(pic)

                self.button(name)
                self.image(*images)

        @staticmethod
        def _get_pictures(update=True):

            if update:
                renpy.loader.cleardirfiles()

            _fold = path.normpath(GALLERY_REL_FOLDER)

            for renpy_fn in renpy.list_files():

                fn = path.normpath(renpy_fn)
                _fn, ext = path.splitext(fn)
                ext = ext.strip().lower()

                if ext not in (".jpg", ".jpeg", ".png", ".webp"):
                    continue

                _dir = path.dirname(fn)
                while True:
                    if _dir == _fold:
                        yield renpy_fn
                        break
                    if not _dir:
                        break
                    _dir = path.dirname(_dir)

        def get_buttons(self):

            zoom_size = float(renpy.config.screen_width) * .15
            for name, button in self.buttons.items():

                disp = button.images[0].displayables[-1]

                w, _h = map(float, Draw._get_size(disp))
                zoom = zoom_size / w

                disp = store.Transform(disp, zoom=zoom)

                yield self.make_button(name, disp)

    draw_gallery = _DrawGallery()

    class Point(object):

        __author__ = "Vladya"

        def __init__(self, x, y, st, color, width):

            self.__x, self.__y = map(int, (x, y))
            self.__st = abs(float(st))

            self.__color = renpy.color.Color(color)
            self.__width = abs(int(width))

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        @property
        def st(self):
            return self.__st

        @property
        def color(self):
            return self.__color

        @property
        def width(self):
            return self.__width

    class ActionRequest(enum.Flag):

        NOTIFY = enum.auto()
        SAVE = enum.auto()
        ADD_TO_GALLERY = enum.auto()


    class Draw(renpy.Displayable):

        __author__ = "Vladya"

        DRAW_BUTTON = 1

        def __init__(self, background, reference=None, **properties):

            super(Draw, self).__init__(**properties)

            self.__background = self._get_displayable(background)
            self.__is_pressed = False

            self.__curves = []
            self.__active_curve = None
            self.__delete_log = []

            self.__color = renpy.color.Color("#000")
            self.__width = 20

            if reference is not None:
                self.__reference = self._get_displayable(reference)
            else:
                self.__reference = None
            self.__show_reference = False

            self.__size = None
            self.__action_request = False
            self.__end_interact_request = False

            self.__picker = ColorPicker(self.set_color)

        @classmethod
        def main(
            cls,
            background=None,
            reference=None,
            start_width=None,
            start_color=None,
            **transform_prop
        ):

            # preset background
            if background is None:
                background = "#888"

            if transform_prop:
                background = store.Transform(background, **transform_prop)

            draw_object = cls(background, reference)
            if start_width:
                draw_object.set_width(start_width)
            if start_color:
                draw_object.set_color(start_color)

            _screen_name = "_draw_screen"

            renpy.mode("screen")
            renpy.show_screen(_screen_name, draw_object, _transient=True)
            roll_forward = renpy.roll_forward_info()

            try:
                rv = renpy.ui.interact(
                    mouse="screen",
                    type="screen",
                    suppress_overlay=True,
                    suppress_window=True,
                    roll_forward=roll_forward
                )
            except (renpy.game.JumpException, renpy.game.CallException) as ex:
                rv = ex

            renpy.checkpoint(rv)

            _special_ex = (renpy.game.JumpException, renpy.game.CallException)
            if isinstance(rv, _special_ex):
                raise rv

            return rv

        def _disable(self):
            self.__end_interact_request = True
            renpy.redraw(self, .0)

        @staticmethod
        def _get_displayable(data):
            result = renpy.displayable(data)
            if not isinstance(result, renpy.display.core.Displayable):
                raise ValueError("{0} isn't a displayable.".format(data))
            return result

        @classmethod
        def _get_size(cls, data):
            disp = cls._get_displayable(data)
            rend = renpy.display.render.render_for_size(
                disp,
                renpy.config.screen_width,
                renpy.config.screen_height,
                .0,
                .0
            )
            return tuple(map(int, rend.get_size()))

        @staticmethod
        def _save_canvas(canvas, folder=None):

            if folder is None:
                folder = SAVE_FOLDER

            canvas_surf = canvas.get_surface()
            _counter = 1
            while True:
                fn = path.abspath(
                    path.join(
                        folder,
                        "{0} {1}{2}".format(DRAW_SAVE_NAME, _counter, DRAW_EXT)
                    )
                )
                if not path.isfile(fn):
                    break
                _counter += 1

            _directory = path.dirname(fn)
            if not path.isdir(_directory):
                os.makedirs(_directory)

            pygame.image.save(canvas_surf, renpy.fsencode(fn))
            return fn

        @classmethod
        def add_canvas_in_gallery(cls, canvas):
            fold = path.abspath(
                path.join(renpy.config.gamedir, GALLERY_REL_FOLDER)
            )
            fn = cls._save_canvas(canvas, fold)
            draw_gallery.update_pictures()
            return fn

        @classmethod
        def get_canvas_as_disp(cls, canvas):

            fn = cls._save_canvas(canvas)
            with open(fn, "rb") as _file:
                _data = _file.read()
            os.remove(fn)

            _hash = hashlib.sha512(_data)
            return renpy.display.im.Data(
                _data,
                "{0}{1}".format(_hash.hexdigest(), DRAW_EXT)
            )

        @property
        def reference(self):
            return self.__reference

        @property
        def reference_switcher(self):
            return self.__show_reference

        @reference_switcher.setter
        def reference_switcher(self, new_value):
            self.__show_reference = bool(new_value)
            renpy.redraw(self, .0)

        @property
        def picker(self):
            return self.__picker

        @property
        def width(self):
            return self.__width

        @width.setter
        def width(self, new_width):
            self.__width = int(new_width)

        def draw_all(self, canvas):

            for curve in self.__curves:

                if not curve:
                    continue

                elif len(curve) == 1:
                    point = curve[0]
                    canvas.circle(
                        point.color,
                        (point.x, point.y),
                        (point.width // 2)
                    )

                else:
                    prev = None
                    for point in curve:
                        if prev:
                            canvas.line(
                                prev.color,
                                (prev.x, prev.y),
                                (point.x, point.y),
                                prev.width
                            )
                        prev = point

        def add_point(self, x, y, st):
            point = Point(x, y, st, self.__color, self.__width)
            if self.__active_curve is None:
                self.__active_curve = []
                self.__curves.append(self.__active_curve)
                self.__delete_log.clear()
            self.__active_curve.append(point)
            renpy.redraw(self, .0)

        def add_in_gallery(self, notify=False):

            rq = ActionRequest.ADD_TO_GALLERY
            if notify:
                rq |= ActionRequest.NOTIFY

            self.__action_request = rq
            renpy.redraw(self, .0)

        def save(self, notify=False):

            rq = ActionRequest.SAVE
            if notify:
                rq |= ActionRequest.NOTIFY

            self.__action_request = rq
            renpy.redraw(self, .0)

        def back(self):
            self.__is_pressed = False
            self.__active_curve = None
            if self.__curves:
                curve = self.__curves.pop(-1)
                self.__delete_log.append(curve)
            renpy.redraw(self, .0)

        def forward(self):
            self.__is_pressed = False
            self.__active_curve = None
            if self.__delete_log:
                curve = self.__delete_log.pop(-1)
                self.__curves.append(curve)
            renpy.redraw(self, .0)

        def clear_all(self):
            self.__is_pressed = False
            self.__active_curve = None
            self.__curves.clear()
            self.__delete_log.clear()
            renpy.redraw(self, .0)

        def set_color(self, color):
            self.__color = renpy.color.Color(color)

        def set_width(self, width):
            self.width = width

        def visit(self):
            return [self.__background]

        def event(self, ev, x, y, st):

            if not self.__size:
                return

            w, h = self.__size
            in_area = False
            if (0 <= x < w) and (0 <= y < h):
                in_area = True

            if in_area and (ev.type == pygame.MOUSEMOTION):
                if self.__is_pressed:
                    self.add_point(x, y, st)

            elif in_area and (ev.type == pygame.MOUSEBUTTONDOWN):
                if ev.button == self.DRAW_BUTTON:
                    self.__is_pressed = True
                    self.add_point(x, y, st)
                    raise renpy.IgnoreEvent()

            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == self.DRAW_BUTTON:
                    self.__is_pressed = False
                    self.__active_curve = None

        def per_interact(self):
            self.__is_pressed = False
            self.__active_curve = None
            renpy.redraw(self, .0)

        def render(self, *rend_args):

            back = renpy.render(self.__background, *rend_args)
            w, h = self.__size = tuple(map(int, back.get_size()))

            result = renpy.Render(w, h)
            result.blit(back, (0, 0))

            if self.reference and self.reference_switcher:
                rend = renpy.render(self.reference, *rend_args)
                x = (float(result.width) * .5) - (float(rend.width) * .5)
                y = (float(result.height) * .5) - (float(rend.height) * .5)
                x, y = map(int, (x, y))
                result.blit(rend, (x, y))

            canvas = result.canvas()
            self.draw_all(canvas)

            if self.__end_interact_request:
                self.__end_interact_request = False
                disp = self.get_canvas_as_disp(canvas)
                renpy.end_interaction(disp)

            if self.__action_request:

                if self.__action_request & ActionRequest.SAVE:
                    fn = self._save_canvas(canvas)
                    if self.__action_request & ActionRequest.NOTIFY:
                        renpy.notify(_("Saved draw as \"{0}\"").format(fn))

                if self.__action_request & ActionRequest.ADD_TO_GALLERY:
                    self.add_canvas_in_gallery(canvas)
                    if self.__action_request & ActionRequest.NOTIFY:
                        renpy.notify(_("A draw added in gallery."))

                self.__action_request = None

            return result


    class ColorPicker(renpy.Displayable):

        __author__ = "Vladya"

        nosave = ["_callback"]

        def __init__(self, pick_color_callback=None, **properties):

            super(ColorPicker, self).__init__(**properties)

            self.__current_coor = None
            self.__current_color = None
            self.__is_pressed = False

            self.__size = None
            self.__brightness = .0

            self._callback = None
            if pick_color_callback:
                self.set_callback(pick_color_callback)

        def __setstate__(self, data):
            data["_callback"] = None
            return data

        def _redraw(self):
            if self.__current_coor:
                prev = self.__current_color
                self.__current_color = self._get_pixel(*self.__current_coor)
                if self._callback and (prev != self.__current_color):
                    self._callback(self.__current_color)
            renpy.redraw(self, .0)

        @property
        def color_circle(self):
            return renpy.display.im.MatrixColor(
                COLOR_CIRCLE,
                renpy.display.im.matrix.brightness(self.brightness)
            )

        @property
        def current_color(self):
            if self.__current_color is None:
                return renpy.color.Color((0, 0, 0, 0))
            return self.__current_color

        @property
        def brightness(self):
            return self.__brightness

        @brightness.setter
        def brightness(self, level):
            self.__brightness = float(level)
            self._redraw()

        def set_callback(self, pick_color_callback):
            self._callback = pick_color_callback

        def _get_pixel(self, x, y):

            x, y = map(int, (x, y))

            surf = renpy.load_surface(self.color_circle)
            try:
                result = surf.get_at((x, y))
            except IndexError:
                return renpy.color.Color((0, 0, 0, 0))
            else:
                r, g, b, a = result

            return renpy.color.Color((r, g, b, a))

        def set_coor(self, x, y):

            x, y = map(float, (x, y))
            surf = renpy.load_surface(self.color_circle)

            width, height = map(float, surf.get_size())

            xcenter, ycenter = (width / 2.), (height / 2.)
            xcenter_dist = xcenter - x
            ycenter_dist = ycenter - y

            dist = math.hypot(*map(abs, (xcenter_dist, ycenter_dist)))
            if dist:
                xstep = xcenter_dist / dist
                ystep = ycenter_dist / dist
            else:
                xstep = ystep = .0

            while True:

                variant = tuple(map(int, map(round,  (x, y))))
                try:
                    r, g, b, _alpha = surf.get_at(variant)
                except IndexError:
                    pass
                else:
                    if _alpha:
                        self.__current_coor = variant
                        return

                x += xstep
                y += ystep

        def event(self, ev, x, y, st):

            if not self.__size:
                return

            w, h = self.__size
            in_area = False
            if (0 <= x < w) and (0 <= y < h):
                in_area = True

            r, g, b, _alpha = self._get_pixel(x, y)

            if ev.type == pygame.MOUSEMOTION:
                if self.__is_pressed:
                    self.set_coor(x, y)
                    self._redraw()

            elif in_area and (ev.type == pygame.MOUSEBUTTONDOWN):
                if ev.button == 1:
                    if _alpha:
                        self.__is_pressed = True
                        self.set_coor(x, y)
                        self._redraw()
                        raise renpy.IgnoreEvent()

            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    self.__is_pressed = False
                    self._redraw()

        def visit(self):
            return [self.color_circle]

        def per_interact(self):
            self.__is_pressed = False
            self._redraw()

        def render(self, *rend_args):

            back = renpy.render(self.color_circle, *rend_args)
            w, h = self.__size = tuple(map(int, back.get_size()))

            result = renpy.Render(w, h)
            result.blit(back, (0, 0))

            if self.__current_coor:
                x, y = self.__current_coor
                canvas = result.canvas()
                canvas.circle("#000", (x, y), 15)
                canvas.circle(self.current_color, (x, y), 3)

            return result

    renpy.config.allow_underfull_grids = True  # Для пополняемой галереи.

init 150 python in draw_logic:

    try:
        _circle = Draw._get_displayable(COLOR_CIRCLE)
        _circle.load()
    except Exception:
        COLOR_CIRCLE = "_placeholder/girl.png"
    else:
        del(_circle)


screen _draw_screen(draw_object):

    modal True

    default circle_size = draw_logic.Draw._get_size(draw_object.picker)

    frame:
        # has hbox
        frame:
            has vbox
            spacing 10
            

            # frame:
            #     has vbox
            #     first_spacing 10
            #     spacing 5
            #     add draw_object.picker:
            #         align (.5, .5)

            #     # frame:
                #     has vbox
                #     label _("Brightness")
                #     bar:
                #         xmaximum circle_size[0]
                #         value FieldValue(
                #             draw_object.picker,
                #             "brightness",
                #             range=2.,
                #             offset=(-1.),
                #             step=.001
                #         )

                # frame:
                #     has vbox
                #     label _("Width")
                #     bar:
                #         xmaximum circle_size[0]
                #         value FieldValue(
                #             draw_object,
                #             "width",
                #             range=100,
                #             offset=1,
                #             step=.001
                #         )

            # frame:
            #     has vbox
            #     xminimum circle_size[0]
            #     textbutton _("Done"):
            #         action Function(draw_object._disable)
            #     textbutton _("Save as .png"):
            #         action Function(draw_object.save, True)
            #     textbutton _("Add in gallery"):
            #         action Function(draw_object.add_in_gallery, True)
            #     if draw_object.reference:
            #         textbutton (_("Hide reference") if draw_object.reference_switcher else _("Show reference")):
            #             action ToggleField(draw_object, "reference_switcher", True, False)

            # frame:
            #     has vbox
            #     xminimum circle_size[0]
            #     textbutton _("Back"):
            #         action Function(draw_object.back)
            #     textbutton _("Forward"):
            #         action Function(draw_object.forward)

            # frame:
            #     has vbox
            #     xminimum circle_size[0]
            #     textbutton _("Clear all"):
            #         action Function(draw_object.clear_all)

        frame:
            xfill True
            yfill True
            add draw_object:
                align (.5, .5)

    imagebutton:
        xalign 0.8
        yalign 0.8
        idle "done_idle"
        hover "done_hover"
        action Jump("timer")

