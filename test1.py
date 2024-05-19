from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.input = TextInput(
            hint_text='Введите текст сюда',
            size_hint=(1, 0.2),
            multiline=False
        )

        self.button = Button(
            text='Показать текст',
            size_hint=(1, 0.2)
        )
        self.button.bind(on_press=self.on_button_press)

        self.layout.add_widget(self.input)
        self.layout.add_widget(self.button)

        self.label = Label(size_hint=(1, 0.6))
        self.layout.add_widget(self.label)

        return self.layout

    def on_button_press(self, instance):
        input_text = self.input.text
        print(f'Введенный текст: {input_text}')
        self.label.text = f'Вы ввели: {input_text}'

if __name__ == '__main__':
    MyApp().run()