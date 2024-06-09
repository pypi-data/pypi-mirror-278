import time
import flet as ft
import random


class folder(ft.UserControl):
    _instances = []

    def __init__(self, left_=0, top_=0, on_update=None):
        super().__init__()
        self.left_ = left_
        self.top_ = top_
        self.grid_size = 110
        self.snapped_left = left_
        self.snapped_top = top_
        self.on_snap_updated = on_update
        self.snapped_now = False
        self.mode = False

    @classmethod
    def set_params(cls, mode=False):
        for instance in cls._instances:
            instance.hovering_toggle(mode)

    def update_snapped(self):
        self.snapped_left = self.full_container.left
        self.snapped_top = self.full_container.top

    def on_hover(self, e):
        self.container.bgcolor = (
            "white,0.1" if self.container.bgcolor == "white,0.0" else "white,0.0"
        )
        self.container.border = (
            ft.border.all(width=1, color="white,0.1")
            if self.container.border == ft.border.all(width=1, color="white,0.0")
            else ft.border.all(width=1, color="white,0.0")
        )
        self.container.update()

    def hovering_toggle(self, toggle=False):
        self.container.on_hover = None if toggle == False else self.on_hover
        self.container.border = ft.border.all(width=1, color="white,0.0")
        self.container.update()
        if toggle == True:
            self.container.bgcolor = "white,0.0"
            self.container.border == ft.border.all(width=1, color="white,0.0")
            self.container.update()

    def change_pos(self, pos):
        x, y = pos
        self.full_container.top = y
        self.full_container.left = x
        self.full_container.update()
        self.update_snapped()

    def on_start_tap(self, e: ft.DragStartEvent):
        self.set_params(mode=False)
        self.snapped_now = True
        self.start_x = e.global_x
        self.start_y = e.global_y
        self.initial_top = (
            self.full_container.top
            if self.full_container.top is not None
            else self.full_container.top
        )
        self.initial_left = (
            self.full_container.left
            if self.full_container.left is not None
            else self.full_container.left
        )
        print(self.snapped_now)

    def on_update_tap(self, e: ft.DragUpdateEvent):
        delta_x = e.global_x - self.start_x
        delta_y = e.global_y - self.start_y
        new_left = self.initial_left + delta_x
        new_top = self.initial_top + delta_y
        snapped_left = round(self.full_container.left / self.grid_size) * self.grid_size
        snapped_top = round(self.full_container.top / self.grid_size) * self.grid_size
        self.change_pos((new_left, new_top))

        if self.on_snap_updated != None:
            self.on_snap_updated((snapped_left, snapped_top))

    def on_end_tap(self, e: ft.DragEndEvent):
        self.set_params(mode=True)
        self.snapped_now = False
        print(self.snapped_now)
        snapped_left = round(self.full_container.left / self.grid_size) * self.grid_size
        snapped_top = round(self.full_container.top / self.grid_size) * self.grid_size

        snapped_left = max(0, snapped_left)
        snapped_top = max(0, snapped_top)
        if self.on_snap_updated != None:
            self.on_snap_updated((snapped_left, snapped_top))
        self.change_pos((snapped_left, snapped_top))
        self.snapped_left = snapped_left
        self.snapped_top = snapped_top

        print(f"End dragging and snapped")

    def on_click_folder(self, e: ft.TapEvent):
        top = e.global_y - self.snapped_top
        top = e.global_y - top + 10
        left = e.global_x - self.snapped_left
        left = e.global_x - left + 10
        print("doing some shot")

    def animate_test(self, toggle=False):
        self.text.opacity = 1 if toggle == True else 0
        self.text.update()

    def build(self):
        colors = [
            "red",
            "blue",
            "green",
            "yellow",
            "purple",
            "orange",
            "pink",
            "brown",
            "black",
            "white",
        ]
        size_folder = 60
        self.icon_ = ft.Container(
            ft.Icon(ft.icons.FOLDER, color=random.choice(colors), size=60),
            alignment=ft.alignment.center,
        )
        self.text = ft.Container(
            ft.Text(
                "Folder", size=12, color="white,0.5", text_align=ft.TextAlign.CENTER
            ),
            alignment=ft.alignment.center,
            opacity=1,
            offset=[0, -0.5],
            animate_opacity=ft.animation.Animation(
                300, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT
            ),
        )
        icon_n_text = ft.Column(
            [self.icon_, self.text], ft.alignment.center, spacing=5, offset=[0, 0.2]
        )

        self.container = ft.Container(
            width=100,
            height=100,
            border_radius=5,
            alignment=ft.alignment.center,
            content=icon_n_text,
            bgcolor="white,0.0",
            border=ft.border.all(width=1, color="white,0.0"),
            on_hover=self.on_hover,
            animate=ft.animation.Animation(
                100, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT
            ),
        )

        self.full_container = ft.GestureDetector(
            content=self.container,
            drag_interval=50,
            mouse_cursor=ft.MouseCursor.CLICK,
            on_vertical_drag_start=self.on_start_tap,
            on_vertical_drag_end=self.on_end_tap,
            on_vertical_drag_update=self.on_update_tap,
            on_tap_up=self.on_click_folder,
            top=self.top_,
            left=self.left_,
            animate_position=ft.animation.Animation(
                500, curve=ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN
            ),
        )
        self._instances.append(self)
        return self.full_container


class start(ft.UserControl):
    def __init__(self):
        super().__init__()

    def change_position(self, e):
        left, top = e

        for i in self.list_folders:
            i: folder = i
            if i.snapped_now == False:
                if i.snapped_left == left and i.snapped_top == top:
                    new_pos = i.snapped_left + i.grid_size, i.snapped_top
                    new_pos = self.find_free_position()
                    i.change_pos(new_pos)
                    i.snapped_left, i.snapped_top = new_pos

    def find_free_position(self):
        occupied_positions = set()
        for folder_ in self.list_folders:
            folder_: folder = folder_
            occupied_positions.add((folder_.snapped_left, folder_.snapped_top))
        for row in range(6):
            for col in range(6):
                pos = (col * folder().grid_size, row * folder().grid_size)
                if pos not in occupied_positions:
                    return pos
        return (0, 0)

    def create(self):
        width_ = self.page.window_width
        height_ = self.page.window_height
        self.list_folders = []
        i_ = 0
        for i in range(6):
            if i != 0:
                i_ = i_ + folder().grid_size
            self.list_folders.append(folder(left_=i_, on_update=self.change_position))
        i_ = 0
        for i in range(6):
            if i != 0:
                i_ = i_ + folder().grid_size
            self.list_folders.append(
                folder(
                    left_=i_, top_=folder().grid_size, on_update=self.change_position
                )
            )
        self.stak = ft.Stack([*self.list_folders], width=width_, height=height_)

    def build(self):
        self.create()
        return self.stak


def main(page: ft.Page):
    page.title = "no"
    page.update()
    page.add(start())


ft.app(main)
