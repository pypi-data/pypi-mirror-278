import flet as ft
import flet.canvas as cv
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fletmint import TabSwitch


def get_fonts_dict(directory):
    fonts_dict = {}
    for file_name in os.listdir(directory):
        if file_name.endswith(".ttf"):
            font_name = os.path.splitext(file_name)[0]
            fonts_dict[font_name] = os.path.join(directory, file_name)
    return fonts_dict


class GridBackgroundCanvas(cv.Canvas):
    def __init__(self, grid_size=20, color=ft.colors.GREY_800):
        super().__init__(shapes=[], expand=True)
        self.grid_size = grid_size
        self.grid_paint = ft.Paint(
            stroke_width=1, style=ft.PaintingStyle.STROKE, color=color
        )

    def did_mount(self):
        self.update_grid(int(self.page.width), int(self.page.height))

    def update_grid(self, width, height):
        shapes = []
        for x in range(0, width + 1, self.grid_size):
            shapes.append(cv.Line(x, 0, x, height, paint=self.grid_paint))
        for y in range(0, height + 1, self.grid_size):
            shapes.append(cv.Line(0, y, width, y, paint=self.grid_paint))

        self.shapes = shapes
        self.width = width
        self.height = height
        self.update()


class FletFowAppbar(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build_bar(self):
        self.app_title = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "FletFlow",
                            style=ft.TextStyle(size=18, font_family="Poppins-SemiBold"),
                        ),
                        ft.Container(
                            ft.Text(
                                "v.0.0 - flet 0.22.1",
                                style=ft.TextStyle(size=9, color=ft.colors.GREY_600),
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Text(
                    "Medical Ai Application",
                    font_family="Poppins-SemiBold",
                    size=10,
                    color=ft.colors.GREY,
                ),
            ],
            spacing=0,
        )

        self.app_bar = ft.Container(
            ft.Row(
                [
                    self.app_title,
                    ft.Container(
                        ft.Row(
                            [
                                ft.TextButton(
                                    content=ft.Icon(
                                        ft.icons.SMARTPHONE_ROUNDED, size=10
                                    ),
                                    style=ft.ButtonStyle(
                                        shape=ft.ContinuousRectangleBorder(radius=20),
                                        side=ft.BorderSide(color="#3d424d", width=2),
                                        bgcolor="#323741",
                                        color="#ffffff",
                                    ),
                                    width=35,
                                    height=35,
                                    on_click=lambda e: print("Button clicked"),
                                ),
                                ft.TextButton(
                                    content=ft.Icon(
                                        ft.icons.DESKTOP_WINDOWS_ROUNDED, size=10
                                    ),
                                    style=ft.ButtonStyle(
                                        shape=ft.ContinuousRectangleBorder(radius=20),
                                        side=ft.BorderSide(color="#3d424d", width=2),
                                        bgcolor="#323741",
                                        color="#ffffff",
                                    ),
                                    width=35,
                                    height=35,
                                    on_click=lambda e: print("Button clicked"),
                                ),
                            ]
                        )
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.TextButton(
                                    content=ft.Icon(ft.icons.CODE, size=10),
                                    style=ft.ButtonStyle(
                                        shape=ft.ContinuousRectangleBorder(radius=20),
                                        side=ft.BorderSide(color="#3d424d", width=2),
                                        bgcolor="#323741",
                                        color="#ffffff",
                                    ),
                                    width=35,
                                    height=35,
                                    on_click=lambda e: print("Button clicked"),
                                ),
                            ]
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#323741",
            border=ft.border.all(1, "#3d424d"),
            padding=ft.padding.all(10),
        )

        return self.app_bar

    def build(self):
        return self.build_bar()


class FletFlowComponentsBar(ft.UserControl):
    def __init__(self):
        super().__init__()

    def did_mount(self):
        self.update_height()

    def update_height(self):
        self.app_bar.height = self.page.window_height
        self.app_bar.update()

    def build(self):
        self.app_bar = ft.Container(
            # ft.Row([self.app_title]),
            bgcolor="#323741",
            border=ft.border.all(1, "#3d424d"),
            padding=ft.padding.all(10),
            width=300,
            # height=800,
        )

        return self.app_bar


class PhoneMockup(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        phone_mockup = ft.Container(
            content=ft.Image(src="iphone14.png"),
            padding=ft.padding.only(top=100),
            alignment=ft.alignment.center,
        )

        return ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        border_radius=8,
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                    phone_mockup,
                ]
            ),
            alignment=ft.alignment.center,
        )


def main(page: ft.Page):
    page.padding = 0
    fonts_directory = (
        r"C:\Users\edoar\Documents\work\fletmint_dev\dev\assets\fonts\poppins"
    )
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = get_fonts_dict(fonts_directory)

    app_bar = FletFowAppbar()
    components_bar = FletFlowComponentsBar()

    mockup = PhoneMockup()

    # Add both components to a Stack
    page.add(
        ft.Stack(
            [
                grid_canvas := GridBackgroundCanvas(),
                ft.Container(mockup, alignment=ft.alignment.center),
                ft.Container(components_bar, alignment=ft.alignment.center_left),
                ft.Container(app_bar, alignment=ft.alignment.top_center),
                # mockup,
            ]
        )
    )

    def on_resize(e):
        grid_canvas.update_grid(int(page.width), int(page.height))
        components_bar.update_height()

    page.on_resize = on_resize


ft.app(target=main, assets_dir=r"C:\Users\edoar\Documents\work\fletmint_dev\dev\assets")
