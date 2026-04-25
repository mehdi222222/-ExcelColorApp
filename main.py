import kivy
kivy.require("2.1.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView

import openpyxl


def excel_color_to_hex(cell):
    """Extract cell RGB color properly."""
    fill = cell.fill

    if fill is None or fill.fgColor is None:
        return "#FFFFFF"

    fg = fill.fgColor

    if fg.type == "rgb":
        value = fg.rgb
        if value and len(value) == 8:
            return "#" + value[2:]
        else:
            return "#FFFFFF"

    return "#FFFFFF"


class SelectFileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")
        self.fc = FileChooserIconView(filters=["*.xlsx", "*.xlsm"])
        layout.add_widget(self.fc)

        btn = Button(text="باز کردن فایل", size_hint=(1, 0.15))
        btn.bind(on_release=self.open_file)

        layout.add_widget(btn)
        self.add_widget(layout)

    def open_file(self, instance):
        if len(self.fc.selection) == 0:
            return

        path = self.fc.selection[0]

        try:
            app = App.get_running_app()
            app.excel_path = path
            self.manager.current = "viewer"

        except Exception as e:
            print("Error:", e)


class ViewerScreen(Screen):
    def on_enter(self):
        self.show_colors()

    def show_colors(self):
        layout = BoxLayout(orientation="vertical")

        try:
            wb = openpyxl.load_workbook(App.get_running_app().excel_path)
            ws = wb.active

            result = []

            for row in ws.iter_rows():
                for cell in row:
                    color = excel_color_to_hex(cell)
                    if color != "#FFFFFF":
                        result.append(f"{cell.coordinate} : {color}")

            if not result:
                layout.add_widget(Label(text="هیچ رنگی پیدا نشد"))
            else:
                for item in result[:50]:
                    layout.add_widget(Label(text=item))

        except Exception as e:
            layout.add_widget(Label(text="خطا در خواندن فایل"))
            layout.add_widget(Label(text=str(e)))

        back_btn = Button(text="بازگشت", size_hint=(1, 0.15))
        back_btn.bind(on_release=lambda i: setattr(self.manager, "current", "select"))
        layout.add_widget(back_btn)

        self.clear_widgets()
        self.add_widget(layout)


class MyApp(App):
    excel_path = None

    def build(self):
        sm = ScreenManager()
        sm.add_widget(SelectFileScreen(name="select"))
        sm.add_widget(ViewerScreen(name="viewer"))
        return sm


if __name__ == "__main__":
    MyApp().run()
