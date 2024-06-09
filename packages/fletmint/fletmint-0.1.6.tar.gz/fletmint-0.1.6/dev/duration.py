import flet as ft
import math
from enum import Enum


class AutoGridDelegate:
    def get_cross_axis_count(self, width, cross_axis_spacing):
        return max(1, math.floor(width / (100 + cross_axis_spacing)))


class GridDelegate(Enum):
    AUTO = AutoGridDelegate()


class MasonryGridView(ft.UserControl):
    def __init__(
        self,
        grid_delegate: GridDelegate = GridDelegate.AUTO,
        cross_axis_count=1,
        height=800,
        width=800,
        main_axis_spacing=0.0,
        cross_axis_spacing=0.0,
        controls=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.height = height
        self.width = width
        self.grid_delegate = (
            grid_delegate.value if isinstance(grid_delegate, Enum) else grid_delegate
        )
        self.cross_axis_count = cross_axis_count
        self.main_axis_spacing = main_axis_spacing
        self.cross_axis_spacing = cross_axis_spacing
        self.children = controls if controls is not None else []
        self.previous_positions = {}

    def did_mount(self):
        self.page.on_resize = self.on_resize
        self.update()

    def on_resize(self, event):
        self.width = self.page.window_width
        self.update_columns()

    def __sanitize_into_containers(self, children):
        for child in children:
            if not isinstance(child, ft.Container):
                child = ft.Container(content=child)
            yield child

    def build_stack(self):
        if self.grid_delegate:
            columns = self.grid_delegate.get_cross_axis_count(
                self.width, self.cross_axis_spacing
            )
        else:
            columns = self.cross_axis_count

        column_width = (self.width - (columns - 1) * self.cross_axis_spacing) / columns
        column_heights = [0] * columns
        self.masonry_stack = ft.Stack(width=self.width, height=self.height)

        for idx, child in enumerate(self.__sanitize_into_containers(self.children)):
            column = column_heights.index(min(column_heights))
            left_position = column * (column_width + self.cross_axis_spacing)
            top_position = column_heights[column]
            column_heights[column] += child.height + self.main_axis_spacing

            animated_child = ft.Container(
                content=child.content,
                width=child.width,
                height=child.height,
                bgcolor=child.bgcolor,
                left=self.previous_positions.get(idx, (left_position, top_position))[0],
                top=self.previous_positions.get(idx, (left_position, top_position))[1],
                animate_position=ft.animation.Animation(1000, "ease"),
            )
            self.masonry_stack.controls.append(animated_child)
            self.previous_positions[idx] = (left_position, top_position)

        self.masonry_stack.height = max(column_heights)

    def update_columns(self):
        if self.grid_delegate:
            columns = self.grid_delegate.get_cross_axis_count(
                self.width, self.cross_axis_spacing
            )
        else:
            columns = self.cross_axis_count
        column_width = (self.width - (columns - 1) * self.cross_axis_spacing) / columns
        column_heights = [0] * columns

        for idx, child in enumerate(self.masonry_stack.controls):
            column = column_heights.index(min(column_heights))
            left_position = column * (column_width + self.cross_axis_spacing)
            top_position = column_heights[column]
            column_heights[column] += child.height + self.main_axis_spacing

            # Actualizar la posición del contenedor y almacenar la nueva posición
            child.left = left_position
            child.top = top_position
            self.previous_positions[idx] = (left_position, top_position)

        self.update()

    def build(self):
        self.build_stack()
        return self.masonry_stack


import random


def main(page: ft.Page):
    page.scroll = "always"
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_visibility=False,
            thumb_visibility=False,
        )
    )

    heights = [300, 150, 400, 250, 100, 350, 200]
    colors = [
        ft.colors.RED,
        ft.colors.GREEN,
        ft.colors.BLUE,
        ft.colors.YELLOW,
        ft.colors.PURPLE,
        ft.colors.ORANGE,
        ft.colors.PINK,
    ]

    controls = [
        ft.Container(
            ft.Image(
                src=f"https://picsum.photos/300/{random.choice(heights)}?random={i}",
                fit=ft.ImageFit.FILL,
            ),
            width=300,
            height=random.choice(heights),
            bgcolor=random.choice(colors),
            border_radius=ft.border_radius.all(5),
        )
        for i in range(50)  # Example range of 20
    ]

    items = [
        ft.Container(
            ft.Text(f"Item {i}", size=20, color=ft.colors.WHITE),
            alignment=ft.alignment.center,
            width=100,
            height=random.randint(100, 300),
            bgcolor=random.choice([ft.colors.RED, ft.colors.GREEN, ft.colors.BLUE]),
            border_radius=5,
        )
        for i in range(20)
    ]

    masonry_grid = MasonryGridView(
        # grid_delegate=AutoGridDelegate(),
        # cross_axis_count=5,
        controls=controls,
        width=page.window_width,
        main_axis_spacing=10,
        cross_axis_spacing=5,
    )

    page.add(ft.Container(masonry_grid, padding=20))
    page.update()


ft.app(target=main)
