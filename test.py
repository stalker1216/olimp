from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
import mysql.connector

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# Screen Definitions
class Task(Screen):
    name = "task"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="Task"))

class CreateTest(Screen):
    name = "create_test"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="Create Test", on_press=self.create_test_popup))

    def create_test_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(TextInput(hint_text="Enter test name"))
        popup_content.add_widget(Button(text="Create Test", on_press=self.create_test))
        popup = Popup(title='Create Test', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def create_test(self, instance):
        # Perform MySQL insertion for the test
        test_name = instance.parent.children[0].text  # Assuming TextInput is the first child
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = "INSERT INTO tests (name) VALUES (%s)"
            cursor.execute(query, (test_name,))
            conn.commit()
            cursor.close()
            conn.close()
            print("Test created successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

# Main App
class TestApp(App):
    def build(self):
        # Screen Manager
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(Task())
        sm.add_widget(CreateTest())
        return sm

if __name__ == "__main__":
    TestApp().run()