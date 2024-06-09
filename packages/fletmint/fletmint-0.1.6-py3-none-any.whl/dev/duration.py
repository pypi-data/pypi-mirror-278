import flet as ft
import math


class CircularTimePicker(ft.UserControl):
    def __init__(self, on_change):
        super().__init__()
        self.on_change = on_change
        self.start_time = 0
        self.end_time = 3
        self.duration = self.end_time - self.start_time
        self.canvas = ft.Canvas(
            size=ft.Size(300, 300),
            on_draw=self.draw_canvas,
        )
        self.dragging = None

    def draw_canvas(self, canvas):
        center = ft.Point(self.canvas.width / 2, self.canvas.height / 2)
        radius = min(center.x, center.y) - 20

        # Draw the outer circle
        canvas.draw_circle(center, radius, ft.Paint(color=ft.colors.GREY_300))

        # Draw the start handle
        start_angle = (self.start_time / 12) * 2 * math.pi - math.pi / 2
        start_x = center.x + radius * math.cos(start_angle)
        start_y = center.y + radius * math.sin(start_angle)
        canvas.draw_circle(
            ft.Point(start_x, start_y), 10, ft.Paint(color=ft.colors.BLUE)
        )

        # Draw the end handle
        end_angle = (self.end_time / 12) * 2 * math.pi - math.pi / 2
        end_x = center.x + radius * math.cos(end_angle)
        end_y = center.y + radius * math.sin(end_angle)
        canvas.draw_circle(ft.Point(end_x, end_y), 10, ft.Paint(color=ft.colors.RED))

        # Draw the duration arc
        canvas.draw_arc(
            center,
            radius,
            start_angle,
            end_angle - start_angle,
            ft.Paint(color=ft.colors.GREEN, stroke_width=6, style=ft.PaintStyle.STROKE),
        )

    def on_pan_start(self, e: ft.GestureEvent):
        if self.is_near_handle(e.local_position, self.start_time):
            self.dragging = "start"
        elif self.is_near_handle(e.local_position, self.end_time):
            self.dragging = "end"

    def on_pan_end(self, e: ft.GestureEvent):
        self.dragging = None

    def on_pan_update(self, e: ft.GestureEvent):
        if self.dragging:
            center = ft.Point(self.canvas.width / 2, self.canvas.height / 2)
            pointer_angle = math.atan2(
                e.local_position.y - center.y, e.local_position.x - center.x
            )
            time = ((pointer_angle + math.pi / 2) / (2 * math.pi)) * 12
            if time < 0:
                time += 12
            if self.dragging == "start":
                self.start_time = time
            elif self.dragging == "end":
                self.end_time = time
            self.duration = self.end_time - self.start_time
            if self.duration < 0:
                self.duration += 12
            self.on_change(self.start_time, self.end_time, self.duration)
            self.canvas.update()

    def is_near_handle(self, point, time):
        center = ft.Point(self.canvas.width / 2, self.canvas.height / 2)
        radius = min(center.x, center.y) - 20
        angle = (time / 12) * 2 * math.pi - math.pi / 2
        handle_x = center.x + radius * math.cos(angle)
        handle_y = center.y + radius * math.sin(angle)
        distance = math.sqrt((point.x - handle_x) ** 2 + (point.y - handle_y) ** 2)
        return distance < 20

    def build(self):
        return ft.GestureDetector(
            on_pan_start=self.on_pan_start,
            on_pan_update=self.on_pan_update,
            on_pan_end=self.on_pan_end,
            child=self.canvas,
        )


def main(page: ft.Page):
    def on_time_change(start, end, duration):
        start_label.value = f"Start Time: {int(start)}:00 AM"
        end_label.value = f"End Time: {int(end)}:00 AM"
        duration_label.value = f"Duration: {int(duration)} hr"
        page.update()

    start_label = ft.Text("Start Time: 0:00 AM")
    end_label = ft.Text("End Time: 3:00 AM")
    duration_label = ft.Text("Duration: 3 hr")

    duration_picker = CircularTimePicker(on_change=on_time_change)

    page.add(
        duration_picker,
        start_label,
        end_label,
        duration_label,
        ft.Row([ft.ElevatedButton("Cancel"), ft.ElevatedButton("Done")]),
    )


ft.app(target=main)
