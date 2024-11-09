from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.label import Label

# Import your use cases and controllers
from project.services.use_cases.siafi.mapeando_pi_siafi import MapeandoPiSiafi
from project.adapters.controllers.mapeando_pi_siafi_controller import MapeandoPiSiafiController
from project.services.use_cases.compare.compare_pi_seof import ComparePiSeof 
from project.services.use_cases.compare.compare_pi_siafi import ComparePiSiafi

class MainApp(App):
    def build(self):
        self.pi_file = None
        self.pi_seof_file = None
        self.pi_siafi_file = None

        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # File chooser
        self.filechooser = FileChooserIconView()
        self.filechooser.bind(on_selection=self.selected_file)
        main_layout.add_widget(self.filechooser)

        # Buttons for selecting files
        file_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='48dp', spacing=10)
        select_pi_button = Button(text='Select PI PDF', on_release=self.select_pi)
        select_pi_seof_button = Button(text='Select PI SEOF PDF', on_release=self.select_pi_seof)
        select_pi_siafi_button = Button(text='Select PI SIAFI PDF', on_release=self.select_pi_siafi)
        file_buttons_layout.add_widget(select_pi_button)
        file_buttons_layout.add_widget(select_pi_seof_button)
        file_buttons_layout.add_widget(select_pi_siafi_button)
        main_layout.add_widget(file_buttons_layout)

        # Buttons for operations
        operation_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='48dp', spacing=10)
        mapeando_pis_button = Button(text='Mapeando PIs', on_release=self.mapeando_pis)
        compare_pis_button = Button(text='Compare PI seof', on_release=self.compare_pi_seof)
        operation_buttons_layout.add_widget(mapeando_pis_button)
        operation_buttons_layout.add_widget(compare_pis_button)
        main_layout.add_widget(operation_buttons_layout)

        return main_layout

    def selected_file(self, filechooser, selection):
        if selection:
            self.selected = selection[0]

    def select_pi(self, instance):
        self.pi_file = self.selected
        print(f"Selected PI file: {self.pi_file}")

    def select_pi_seof(self, instance):
        self.pi_seof_file = self.selected
        print(f"Selected PI SEOF file: {self.pi_seof_file}")

    def select_pi_siafi(self, instance):
        self.pi_siafi_file = self.selected
        print(f"Selected PI SIAFI file: {self.pi_siafi_file}")

    def mapeando_pis(self, instance):
        if self.pi_file and self.pi_seof_file and self.pi_siafi_file:
            mapeando_pi_siafi_use_case = MapeandoPiSiafi()
            mapeando_pi_siafi_controller = MapeandoPiSiafiController(mapeando_pi_siafi_use_case)
            mapeando_pi_siafi_controller.handle(self.pi_file, self.pi_seof_file, self.pi_siafi_file)
            print("Mapeando PIs completed")
        else:
            print("Please select all PI files")

    def compare_pi_seof(self, instance):
        if self.pi_file and self.pi_seof_file:
            compare_pi_seof_use_case = ComparePiSeof()
            compare_pi_seof_use_case.pi_seof(self.pi_file, self.pi_siafi_file)
            print("Compare PIs completed")
        else:
            print("Please select all PI files")

    def compare_pi_siafi(self, instance):
        if self.pi_file and self.pi_siafi_file:
            compare_pi_siafi_use_case = ComparePiSiafi()
            compare_pi_siafi_use_case.pi_siafi(self.pi_file, self.pi_siafi_file)
            print("Compare PIs completed")
        else:
            print("Please select all PI files")

if __name__ == '__main__':
    MainApp().run()