import flet as ft
from dataclasses import dataclass
from .text_input import TextInput
from .button import Button


class Time(ft.Row):
    def __init__(self):
        super().__init__()
        self.hour = 8
        self.minute = 45
        self.am_pm = "AM"

        # Create the display components
        self.hour_display = ft.Text(value=f"{self.hour:02}")
        self.minute_display = ft.Text(value=f"{self.minute:02}")
        self.am_pm_display = ft.Text(value=self.am_pm)

        # Layout for hours
        self.hours = ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_DROP_UP, on_click=self.increment_hour
                ),
                ft.Container(
                    self.hour_display,
                    padding=ft.padding.symmetric(vertical=8, horizontal=16),
                    border_radius=8,
                    border=ft.border.all(color=ft.colors.GREY, width=1),
                ),
                ft.IconButton(
                    icon=ft.icons.ARROW_DROP_DOWN, on_click=self.decrement_hour
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Layout for minutes
        self.minutes = ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_DROP_UP, on_click=self.increment_minute
                ),
                ft.Container(
                    self.minute_display,
                    padding=ft.padding.symmetric(vertical=8, horizontal=16),
                    border_radius=8,
                    border=ft.border.all(color=ft.colors.GREY, width=1),
                ),
                ft.IconButton(
                    icon=ft.icons.ARROW_DROP_DOWN, on_click=self.decrement_minute
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Layout for AM/PM
        self.am_pm_buttons = ft.Column(
            [
                Button(label="AM", width=60, height=50, on_click=self.toggle_am_pm),
                Button(
                    label="PM",
                    width=60,
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.with_opacity(0, "white"),
                        side=ft.BorderSide(width=1, color=ft.colors.WHITE),
                        shape=ft.ContinuousRectangleBorder(radius=8),
                    ),
                    on_click=self.toggle_am_pm,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Combine hours, minutes, and AM/PM into a single row
        self.controls = [self.hours, ft.Text(":"), self.minutes, self.am_pm_buttons]

    def did_mount(self):
        self.update_time_display()

    # Function to handle hour increment/decrement
    def increment_hour(self, e):
        self.hour = (self.hour % 12) + 1
        self.update_time_display()

    def decrement_hour(self, e):
        self.hour = (self.hour - 2) % 12 + 1
        self.update_time_display()

    # Function to handle minute increment/decrement
    def increment_minute(self, e):
        self.minute = (self.minute + 1) % 60
        self.update_time_display()

    def decrement_minute(self, e):
        self.minute = (self.minute - 1) % 60
        self.update_time_display()

    # Function to handle AM/PM toggle
    def toggle_am_pm(self, e):
        self.am_pm = "PM" if self.am_pm == "AM" else "AM"
        self.update_time_display()

    # Update time display
    def update_time_display(self):
        self.hour_display.value = f"{self.hour:02}"
        self.minute_display.value = f"{self.minute:02}"
        self.am_pm_display.value = self.am_pm

        # Update AM/PM button states
        for btn in self.am_pm_buttons.controls:
            if btn.text == self.am_pm:
                btn.bgcolor = ft.colors.TEAL
                btn.color = ft.colors.WHITE
            else:
                btn.bgcolor = None
                btn.color = None

        self.update()


@dataclass
class DropDownColors:
    container_background_color: str
    container_border_color: str
    selected_control_background_color: str
    selected_control_text_color: str
    unselected_control_text_color: str
    dropdown_starter_icon_color: str

    @staticmethod
    def dark():
        return DropDownColors(
            container_background_color="#323741",
            container_border_color="#3d424d",
            selected_control_background_color="#2a2e35",
            selected_control_text_color=ft.colors.with_opacity(0.9, "white"),
            unselected_control_text_color="#959cae",
            dropdown_starter_icon_color="#ffffff",
        )

    @staticmethod
    def light():
        return DropDownColors(
            container_background_color="#ffffff",
            container_border_color="#d9deec",
            selected_control_background_color="#e9efff",
            selected_control_text_color="#5182ff",
            unselected_control_text_color="#646f8e",
            dropdown_starter_icon_color="#7e879e",
        )


class TimePicker(ft.UserControl):
    def __init__(
        self,
        controls=[],
        drodown_icons=[
            ft.icons.ARROW_DROP_DOWN_ROUNDED,
            ft.icons.ARROW_DROP_UP_ROUNDED,
        ],
        theme=ft.ThemeMode.DARK,
        max_width=300,
        on_select=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.show_splash = False
        self.controls = controls
        self.controls_num = len(controls)
        self.max_width = max_width
        self.dropdown_icons = drodown_icons
        self.colors = (
            DropDownColors.dark()
            if theme == ft.ThemeMode.DARK
            else DropDownColors.light()
        )
        self._on_select = on_select
        self._dropdown_starter_bounds = None

    def did_mount(self):
        self.theme = self.page.theme_mode
        self.colors = (
            DropDownColors.dark()
            if self.theme == ft.ThemeMode.DARK
            else DropDownColors.light()
        )
        self.update()

    def build_control(self):
        return []

    def unfocus_dropdown(self):
        self.dropdown_starter.content.content.controls[0].remove_hover_state(None)
        self.dropdown_starter.content.content.controls[1].content = ft.Icon(
            name=self.dropdown_icons[0],
            color=self.colors.dropdown_starter_icon_color,
            size=25,
        )
        self.dropdown_starter.update()

    def close_dropdown(self):
        self.page.splash = None
        self.show_splash = False
        self.page.update()

    def build_dropdown(self):
        return ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Container(
                            Time(),
                            width=self.max_width,
                            height=150,
                            margin=5,
                            padding=ft.padding.only(top=3, left=15),
                        ),
                        border_radius=8,
                    )
                ],
                spacing=2,
            ),
            padding=10,
            bgcolor=self.colors.container_background_color,
            border=ft.border.all(2, self.colors.container_border_color),
            border_radius=10,
            width=self.max_width,
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=3,
                color=ft.colors.BLACK,
                offset=ft.Offset(0, 1),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

    def toggle_dropdown(self, e):
        if self.show_splash:
            self.unfocus_dropdown()
            self.close_dropdown()
        else:
            self.dropdown_starter.content.content.controls[0].set_hover_state(None)
            self.dropdown_starter.content.content.controls[1].content = ft.Icon(
                name=self.dropdown_icons[1],
                color=self.colors.dropdown_starter_icon_color,
                size=25,
            )
            self._dropdown_starter_bounds = (
                self.calculate_bounds(e)
                if not self._dropdown_starter_bounds
                else self._dropdown_starter_bounds
            )
            self.page.splash = self.update_dropdown_position(
                self._dropdown_starter_bounds["bottom_left"]
            )
            self.show_splash = True

        self.dropdown_starter.update()
        self.page.update()

    def calculate_bounds(self, event, height=50):
        top_left = (event.global_x - event.local_x, event.global_y - event.local_y)
        return {
            "top_left": top_left,
            "top_right": (top_left[0] + self.max_width, top_left[1]),
            "bottom_left": (top_left[0], top_left[1] + float(height)),
            "bottom_right": (top_left[0] + self.max_width, top_left[1] + float(height)),
        }

    def update_dropdown_position(self, bottom_left):
        dropdown = self.dropdown
        dropdown.top = bottom_left[1] + 20
        dropdown.left = bottom_left[0]
        return dropdown

    def build(self):
        self.dropdown = self.build_dropdown()
        self.dropdown_starter = ft.Container(
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.CLICK,
                on_tap_down=self.toggle_dropdown,
                content=ft.Stack(
                    [
                        TextInput(
                            prefix=ft.Icon(
                                name=ft.icons.ACCESS_TIME_ROUNDED,
                                color=ft.colors.GREY_600,
                                size=18,
                            )
                        ),
                        ft.Container(
                            ft.Icon(
                                name=self.dropdown_icons[0],
                                color=self.colors.dropdown_starter_icon_color,
                                size=25,
                            ),
                            right=0,
                            bottom=17,
                            padding=ft.padding.only(right=20),
                        ),
                    ]
                ),
            ),
            width=self.max_width,
        )
        return self.dropdown_starter
