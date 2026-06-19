from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
import requests
from bs4 import BeautifulSoup
import random
import webbrowser
import urllib.parse

# ======================= GLOBAL HEADERS =======================
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ======================= DATA =======================
to_do_list = []
time_table = {
    "Monday": ["Software Engineering Lecture", "Data Structure Lecture"],
    "Tuesday": ["Data Structure Lecture", "Software Engineering Lecture"],
    "Wednesday": ["Professional Practice Lecture", "Civics Lecture", "Programming for AI"],
    "Thursday": ["CO & AI Lecture"],
    "Friday": ["Professional Practice Lecture", "Civics Lecture", "Programming for AI"],
    "Saturday": [],
    "Sunday": ["Cricket Match"]
}

# ======================= COLOR SCHEME =======================
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#73BA9B',
    'danger': '#DB5461',
    'light': '#F5F5F5',
    'dark': '#2D3047',
    'mood1': '#FF6B6B',
    'mood2': "#CD4E4E",
    'mood3': '#45B7D1',
    'mood4': '#96CEB4',
    'mood5': '#FFEAA7'
}

# ======================= UTILITY FUNCTIONS =======================
class CustomPopup(Popup):
    def __init__(self, title='', content=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True
        
        if content:
            self.add_widget(content)

class FunctionButton(Button):
    def __init__(self, text='', icon='', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = 20
        self.bold = True
        self.size_hint = (1, None)
        self.height = 80
        self.background_normal = ''
        self.background_color = (0.2, 0.6, 0.8, 1)
        self.color = (1, 1, 1, 1)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title
        title_label = Label(
            text='Life Hub Terminal',
            font_size=32,
            bold=True,
            size_hint=(1, 0.15),
            color=(0.1, 0.1, 0.5, 1)
        )
        main_layout.add_widget(title_label)
        
        # Button grid
        grid = GridLayout(cols=2, spacing=15, size_hint=(1, 0.85))
        
        buttons_info = [
            ("Mood & Songs", self.mood_playlist_popup, COLORS['mood1']),
            ("Daily News", self.fetch_news_popup, COLORS['secondary']),
            ("Google Search", self.google_search_popup, COLORS['accent']),
            ("Motivation", self.quote_popup, COLORS['success']),
            ("To-Do List", self.todo_popup, COLORS['primary']),
            ("Calculator", self.calculator_popup, COLORS['danger']),
            ("Time Table", self.timetable_popup, COLORS['mood3']),
            ("YouTube Search", self.youtube_popup, COLORS['mood2']),
            ("Weather", self.weather_popup, COLORS['mood4']),
            ("Exit", self.exit_app, COLORS['dark'])
        ]
        
        for text, callback, color in buttons_info:
            btn = FunctionButton(text=text)
            btn.background_color = self.hex_to_rgb(color)
            btn.bind(on_press=callback)
            grid.add_widget(btn)
        
        main_layout.add_widget(grid)
        self.add_widget(main_layout)
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4)) + (1,)
    
    def mood_playlist_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        label = Label(text='Choose your mood:', font_size=24, color=(0.2, 0.2, 0.2, 1))
        content.add_widget(label)
        
        moods = [
            ("Emotional", "1"),
            ("Sad", "2"),
            ("Lofi", "3"),
            ("Punjabi", "4"),
            ("Romantic", "5")
        ]
        
        playlists = {
            "1": "https://www.youtube.com/watch?v=jIQ0Dx-4peE&list=RDjIQ0Dx-4peE&start_radio=1",
            "2": "https://www.youtube.com/watch?v=i61nN7hcbPA&list=PL115iZFgSUHaEbv9Why0FV7jvAN4qREdJ",
            "3": "https://www.youtube.com/watch?v=IjUYIhQDpRw&list=PLLlb2C74bLzdu9dUe9QiuCMq-cLJtIbDZ",
            "4": "https://www.youtube.com/watch?v=XTp5jaRU3Ws&list=PLO7-VO1D0_6NYoMAN0XncJu4tvibirSmN",
            "5": "https://www.youtube.com/watch?v=atVof3pjT-I&list=PL9bw4S5ePsEGpT9PdWJYN8joMa2eWAxJf"
        }
        
        for mood_text, mood_key in moods:
            btn = Button(text=mood_text, size_hint=(1, None), height=60,
                        background_color=self.hex_to_rgb(COLORS['mood1']))
            btn.bind(on_press=lambda x, key=mood_key: self.open_playlist(playlists[key]))
            content.add_widget(btn)
        
        close_btn = Button(text='Close', size_hint=(1, None), height=50,
                          background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        
        content.add_widget(close_btn)
        self.popup = CustomPopup(title='Mood Playlist', content=content)
        self.popup.open()
    
    def open_playlist(self, url):
        webbrowser.open(url)
        self.popup.dismiss()
    
    def fetch_news_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        label = Label(text='Fetching BBC News...', font_size=20, color=(0.2, 0.2, 0.2, 1))
        content.add_widget(label)
        
        scroll = ScrollView(size_hint=(1, 0.8))
        news_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        news_layout.bind(minimum_height=news_layout.setter('height'))
        
        try:
            r = requests.get("https://www.bbc.com/news", headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            headlines = soup.find_all("h2", limit=10)
            
            label.text = 'BBC Top News:'
            for i, h in enumerate(headlines, 1):
                news_label = Label(
                    text=f"{i}. {h.text.strip()}",
                    font_size=16,
                    size_hint_y=None,
                    height=40,
                    halign='left',
                    valign='middle',
                    text_size=(400, None)
                )
                news_label.bind(texture_size=news_label.setter('size'))
                news_layout.add_widget(news_label)
                
        except Exception as e:
            error_label = Label(text=f"Failed to fetch news: {str(e)}", font_size=16)
            news_layout.add_widget(error_label)
        
        scroll.add_widget(news_layout)
        content.add_widget(scroll)
        
        close_btn = Button(text='Close', size_hint=(1, None), height=50,
                          background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        content.add_widget(close_btn)
        
        self.popup = CustomPopup(title='Daily News', content=content)
        self.popup.open()
    
    def google_search_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        label = Label(text='Google Search', font_size=24, color=(0.2, 0.2, 0.2, 1))
        content.add_widget(label)
        
        self.search_input = TextInput(
            hint_text='Enter your search query...',
            size_hint=(1, None),
            height=50,
            multiline=False,
            font_size=18
        )
        content.add_widget(self.search_input)
        
        btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=60)
        
        search_btn = Button(text='Search', background_color=self.hex_to_rgb(COLORS['accent']))
        search_btn.bind(on_press=self.perform_google_search)
        btn_layout.add_widget(search_btn)
        
        close_btn = Button(text='Close', background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        btn_layout.add_widget(close_btn)
        
        content.add_widget(btn_layout)
        self.popup = CustomPopup(title='Google Search', content=content)
        self.popup.open()
    
    def perform_google_search(self, instance):
        query = self.search_input.text.strip()
        if query:
            search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
            webbrowser.open(search_url)
            self.popup.dismiss()
    
    def quote_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=15, padding=30)
        
        try:
            r = requests.get("https://quotes.toscrape.com/", headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            quotes = soup.find_all("div", class_="quote")
            q = random.choice(quotes)
            text = q.find("span", class_="text").text
            author = q.find("small", class_="author").text
            
            quote_label = Label(
                text=f'"{text}"',
                font_size=20,
                halign='center',
                valign='middle',
                text_size=(400, None)
            )
            quote_label.bind(texture_size=quote_label.setter('size'))
            content.add_widget(quote_label)
            
            author_label = Label(
                text=f"— {author}",
                font_size=18,
                italic=True,
                color=(0.5, 0.5, 0.5, 1)
            )
            content.add_widget(author_label)
            
        except Exception as e:
            error_label = Label(text=f"Could not fetch quote: {str(e)}", font_size=16)
            content.add_widget(error_label)
        
        btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=60)
        
        new_btn = Button(text='New Quote', background_color=self.hex_to_rgb(COLORS['success']))
        new_btn.bind(on_press=lambda x: [self.popup.dismiss(), self.quote_popup(instance)])
        btn_layout.add_widget(new_btn)
        
        close_btn = Button(text='Close', background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        btn_layout.add_widget(close_btn)
        
        content.add_widget(btn_layout)
        self.popup = CustomPopup(title='Motivational Quote', content=content)
        self.popup.open()
    
    def todo_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        label = Label(text='To-Do List Manager', font_size=24, color=(0.2, 0.2, 0.2, 1))
        content.add_widget(label)
        
        # Input and Add button
        input_layout = BoxLayout(spacing=10, size_hint=(1, None), height=60)
        self.todo_input = TextInput(
            hint_text='Enter new task...',
            multiline=False,
            size_hint=(0.7, 1)
        )
        input_layout.add_widget(self.todo_input)
        
        add_btn = Button(text='Add', size_hint=(0.3, 1),
                        background_color=self.hex_to_rgb(COLORS['success']))
        add_btn.bind(on_press=self.add_todo_task)
        input_layout.add_widget(add_btn)
        content.add_widget(input_layout)
        
        # Tasks display
        scroll = ScrollView(size_hint=(1, 0.6))
        self.todo_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.todo_layout.bind(minimum_height=self.todo_layout.setter('height'))
        self.update_todo_display()
        scroll.add_widget(self.todo_layout)
        content.add_widget(scroll)
        
        # Control buttons
        control_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=120)
        
        refresh_btn = Button(text='Refresh', background_color=self.hex_to_rgb(COLORS['accent']))
        refresh_btn.bind(on_press=lambda x: self.update_todo_display())
        control_layout.add_widget(refresh_btn)
        
        clear_btn = Button(text='Clear All', background_color=self.hex_to_rgb(COLORS['danger']))
        clear_btn.bind(on_press=self.clear_all_tasks)
        control_layout.add_widget(clear_btn)
        
        close_btn = Button(text='Close', background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        control_layout.add_widget(close_btn)
        
        help_btn = Button(text='Help', background_color=self.hex_to_rgb(COLORS['primary']))
        help_btn.bind(on_press=lambda x: self.show_todo_help())
        control_layout.add_widget(help_btn)
        
        content.add_widget(control_layout)
        self.popup = CustomPopup(title='To-Do List', content=content)
        self.popup.open()
    
    def add_todo_task(self, instance):
        task = self.todo_input.text.strip()
        if task:
            to_do_list.append(task)
            self.todo_input.text = ''
            self.update_todo_display()
    
    def update_todo_display(self):
        self.todo_layout.clear_widgets()
        
        if not to_do_list:
            empty_label = Label(text='\n\nNo tasks yet. Add your first task above!',
                               font_size=18, color=(0.5, 0.5, 0.5, 1))
            self.todo_layout.add_widget(empty_label)
        else:
            for i, task in enumerate(to_do_list, 1):
                task_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)
                
                task_label = Label(
                    text=f"{i}. {task}",
                    font_size=18,
                    halign='left',
                    valign='middle',
                    size_hint=(0.7, 1)
                )
                task_label.bind(texture_size=task_label.setter('size'))
                task_layout.add_widget(task_label)
                
                remove_btn = Button(
                    text='Remove',
                    size_hint=(0.30, 1),
                    background_color=self.hex_to_rgb(COLORS['danger'])
                )
                remove_btn.bind(on_press=lambda x, idx=i-1: self.remove_todo_task(idx))
                task_layout.add_widget(remove_btn)
                
                edit_btn = Button(
                    text='Edit',
                    size_hint=(0.20, 1),
                    background_color=self.hex_to_rgb(COLORS['accent'])
                )
                edit_btn.bind(on_press=lambda x, idx=i-1: self.edit_todo_task(idx))
                task_layout.add_widget(edit_btn)
                
                self.todo_layout.add_widget(task_layout)
    
    def remove_todo_task(self, index):
        if 0 <= index < len(to_do_list):
            to_do_list.pop(index)
            self.update_todo_display()
    
    def edit_todo_task(self, index):
        if 0 <= index < len(to_do_list):
            edit_popup = Popup(title='Edit Task', size_hint=(0.8, 0.4))
            content = BoxLayout(orientation='vertical', spacing=10, padding=20)
            
            edit_input = TextInput(text=to_do_list[index], multiline=False, size_hint=(1, None), height=50)
            content.add_widget(edit_input)
            
            btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=50)
            
            save_btn = Button(text='Save', background_color=self.hex_to_rgb(COLORS['success']))
            save_btn.bind(on_press=lambda x: [
                self.save_edited_task(index, edit_input.text),
                edit_popup.dismiss(),
                self.update_todo_display()
            ])
            btn_layout.add_widget(save_btn)
            
            cancel_btn = Button(text='Cancel', background_color=self.hex_to_rgb(COLORS['dark']))
            cancel_btn.bind(on_press=lambda x: edit_popup.dismiss())
            btn_layout.add_widget(cancel_btn)
            
            content.add_widget(btn_layout)
            edit_popup.content = content
            edit_popup.open()
    
    def save_edited_task(self, index, new_text):
        if 0 <= index < len(to_do_list) and new_text.strip():
            to_do_list[index] = new_text.strip()
    
    def clear_all_tasks(self, instance):
        to_do_list.clear()
        self.update_todo_display()
    
    def show_todo_help(self):
        help_popup = Popup(title='To-Do List Help', size_hint=(0.8, 0.5))
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        help_text = """
        1. Type task in input field and click 'Add'
        2. Click Remove to remove a task
        3. Click Edit to edit a task
        4. Click Clear All to clear all tasks
        5. Click Refresh to refresh the list
        """
        
        help_label = Label(text=help_text, font_size=16, halign='left', valign='top')
        help_label.bind(texture_size=help_label.setter('size'))
        content.add_widget(help_label)
        
        close_btn = Button(text='Close', size_hint=(1, None), height=50,
                          background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: help_popup.dismiss())
        content.add_widget(close_btn)
        
        help_popup.content = content
        help_popup.open()
    
    def calculator_popup(self, instance):
        content = CalculatorWidget()
        self.popup = CustomPopup(title='Calculator', content=content)
        self.popup.open()
    
    def timetable_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        label = Label(text='Weekly Time Table', font_size=24, color=(0.2, 0.2, 0.2, 1))
        content.add_widget(label)
        
        # Day selector
        day_layout = BoxLayout(spacing=10, size_hint=(1, None), height=50)
        day_spinner = Spinner(
            text='Monday',
            values=list(time_table.keys()),
            size_hint=(0.7, 1)
        )
        day_layout.add_widget(day_spinner)
        
        view_btn = Button(text='View', size_hint=(0.3, 1),
                         background_color=self.hex_to_rgb(COLORS['primary']))
        day_layout.add_widget(view_btn)
        content.add_widget(day_layout)
        
        # Subjects display
        self.subjects_scroll = ScrollView(size_hint=(1, 0.5))
        self.subjects_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.subjects_layout.bind(minimum_height=self.subjects_layout.setter('height'))
        self.subjects_scroll.add_widget(self.subjects_layout)
        content.add_widget(self.subjects_scroll)
        
        # Control buttons
        control_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=120)
        
        add_btn = Button(text='Add Subject', background_color=self.hex_to_rgb(COLORS['success']))
        control_layout.add_widget(add_btn)
        
        remove_btn = Button(text='Remove', background_color=self.hex_to_rgb(COLORS['danger']))
        control_layout.add_widget(remove_btn)
        
        clear_btn = Button(text='Clear Day', background_color=self.hex_to_rgb(COLORS['accent']))
        control_layout.add_widget(clear_btn)
        
        close_btn = Button(text='Close', background_color=self.hex_to_rgb(COLORS['dark']))
        control_layout.add_widget(close_btn)
        
        content.add_widget(control_layout)
        
        # Update function for view button
        def update_subjects(instance):
            day = day_spinner.text
            self.subjects_layout.clear_widgets()
            
            subjects = time_table.get(day, [])
            if not subjects:
                empty_label = Label(text='\n\nNo subjects for this day',
                                   font_size=18, color=(0.5, 0.5, 0.5, 1))
                self.subjects_layout.add_widget(empty_label)
            else:
                for i, subject in enumerate(subjects, 1):
                    sub_label = Label(
                        text=f"{i}. {subject}",
                        font_size=18,
                        size_hint_y=None,
                        height=40
                    )
                    self.subjects_layout.add_widget(sub_label)
        
        view_btn.bind(on_press=update_subjects)
        
        # Bind other buttons
        def add_subject_popup(instance):
            add_content = BoxLayout(orientation='vertical', spacing=10, padding=20)
            
            day_label = Label(text=f'Add subject for {day_spinner.text}:',
                             font_size=20)
            add_content.add_widget(day_label)
            
            subject_input = TextInput(hint_text='Enter subject name...',
                                     multiline=False, size_hint=(1, None), height=50)
            add_content.add_widget(subject_input)
            
            btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=50)
            
            save_btn = Button(text='Save', background_color=self.hex_to_rgb(COLORS['success']))
            save_btn.bind(on_press=lambda x: [
                time_table[day_spinner.text].append(subject_input.text.strip()),
                update_subjects(None),
                add_popup.dismiss()
            ])
            btn_layout.add_widget(save_btn)
            
            cancel_btn = Button(text='Cancel', background_color=self.hex_to_rgb(COLORS['dark']))
            cancel_btn.bind(on_press=lambda x: add_popup.dismiss())
            btn_layout.add_widget(cancel_btn)
            
            add_content.add_widget(btn_layout)
            
            add_popup = Popup(title='Add Subject', content=add_content, size_hint=(0.8, 0.4))
            add_popup.open()
        
        add_btn.bind(on_press=add_subject_popup)
        
        def remove_subject_popup(instance):
            if not time_table[day_spinner.text]:
                return
            
            remove_content = BoxLayout(orientation='vertical', spacing=10, padding=20)
            
            remove_label = Label(text=f'Select subject to remove from {day_spinner.text}:',
                                font_size=20)
            remove_content.add_widget(remove_label)
            
            subject_spinner = Spinner(
                text=time_table[day_spinner.text][0],
                values=time_table[day_spinner.text],
                size_hint=(1, None),
                height=50
            )
            remove_content.add_widget(subject_spinner)
            
            btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=50)
            
            remove_confirm_btn = Button(text='Remove', background_color=self.hex_to_rgb(COLORS['danger']))
            remove_confirm_btn.bind(on_press=lambda x: [
                time_table[day_spinner.text].remove(subject_spinner.text),
                update_subjects(None),
                remove_popup.dismiss()
            ])
            btn_layout.add_widget(remove_confirm_btn)
            
            cancel_btn = Button(text='Cancel', background_color=self.hex_to_rgb(COLORS['dark']))
            cancel_btn.bind(on_press=lambda x: remove_popup.dismiss())
            btn_layout.add_widget(cancel_btn)
            
            remove_content.add_widget(btn_layout)
            
            remove_popup = Popup(title='Remove Subject', content=remove_content, size_hint=(0.8, 0.4))
            remove_popup.open()
        
        remove_btn.bind(on_press=remove_subject_popup)
        
        def clear_day_confirmation(instance):
            clear_content = BoxLayout(orientation='vertical', spacing=10, padding=20)
            
            clear_label = Label(text=f'Clear all subjects for {day_spinner.text}?',
                               font_size=20)
            clear_content.add_widget(clear_label)
            
            btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=50)
            
            yes_btn = Button(text='Yes', background_color=self.hex_to_rgb(COLORS['danger']))
            yes_btn.bind(on_press=lambda x: [
                time_table[day_spinner.text].clear(),
                update_subjects(None),
                clear_popup.dismiss()
            ])
            btn_layout.add_widget(yes_btn)
            
            no_btn = Button(text='No', background_color=self.hex_to_rgb(COLORS['dark']))
            no_btn.bind(on_press=lambda x: clear_popup.dismiss())
            btn_layout.add_widget(no_btn)
            
            clear_content.add_widget(btn_layout)
            
            clear_popup = Popup(title='Clear Day', content=clear_content, size_hint=(0.8, 0.3))
            clear_popup.open()
        
        clear_btn.bind(on_press=clear_day_confirmation)
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        
        # Initial display
        update_subjects(None)
        
        self.popup = CustomPopup(title='Time Table', content=content)
        self.popup.open()
    
    def youtube_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        label = Label(text='YouTube Search', font_size=24, color=(0.2, 0.2, 0.2, 1))
        content.add_widget(label)
        
        self.youtube_input = TextInput(
            hint_text='Search YouTube videos...',
            size_hint=(1, None),
            height=50,
            multiline=False,
            font_size=18
        )
        content.add_widget(self.youtube_input)
        
        btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=60)
        
        search_btn = Button(text='Search', background_color=self.hex_to_rgb(COLORS['mood2']))
        search_btn.bind(on_press=self.perform_youtube_search)
        btn_layout.add_widget(search_btn)
        
        close_btn = Button(text='Close', background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        btn_layout.add_widget(close_btn)
        
        content.add_widget(btn_layout)
        self.popup = CustomPopup(title='YouTube Search', content=content)
        self.popup.open()
    
    def perform_youtube_search(self, instance):
        query = self.youtube_input.text.strip()
        if query:
            search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
            webbrowser.open(search_url)
            self.popup.dismiss()
    
    def weather_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        label = Label(text='Weather Forecast', font_size=24, color=(0.2, 0.2, 0.2, 1))
        content.add_widget(label)
        
        self.city_input = TextInput(
            hint_text='Enter city name...',
            size_hint=(1, None),
            height=50,
            multiline=False,
            font_size=18
        )
        content.add_widget(self.city_input)
        
        self.weather_display = Label(
            text='',
            font_size=20,
            halign='left',
            valign='middle'
        )
        content.add_widget(self.weather_display)
        
        btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=60)
        
        fetch_btn = Button(text='Get Weather', background_color=self.hex_to_rgb(COLORS['mood4']))
        fetch_btn.bind(on_press=self.fetch_weather)
        btn_layout.add_widget(fetch_btn)
        
        close_btn = Button(text='Close', background_color=self.hex_to_rgb(COLORS['dark']))
        close_btn.bind(on_press=lambda x: self.dismiss_popup())
        btn_layout.add_widget(close_btn)
        
        content.add_widget(btn_layout)
        self.popup = CustomPopup(title='Weather', content=content)
        self.popup.open()
    
    def fetch_weather(self, instance):
        city = self.city_input.text.strip()
        if not city:
            self.weather_display.text = 'Please enter a city name.'
            return
        
        url = f"https://wttr.in/{city}?format=j1"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            current = data["current_condition"][0]
            
            weather_text = f"""
            Weather Details for {city}
            
            Temperature: {current['temp_C']}°C
            Feels Like: {current['FeelsLikeC']}°C
            Condition: {current['weatherDesc'][0]['value']}
            Humidity: {current['humidity']}%
            Wind Speed: {current['windspeedKmph']} km/h
            """
            
            self.weather_display.text = weather_text
            
        except Exception as e:
            self.weather_display.text = f"Error getting weather data: {str(e)}"
    
    def dismiss_popup(self):
        if hasattr(self, 'popup'):
            self.popup.dismiss()
    
    def exit_app(self, instance):
        App.get_running_app().stop()

class CalculatorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=5, padding=5, **kwargs)
        
        # Display
        self.display = TextInput(
            text='0',
            font_size=40,
            halign='right',
            readonly=True,
            size_hint=(1, 0.2),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        self.add_widget(self.display)
        
        # Button grid
        grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.8))
        
        buttons = [
            ('7', self.button_press), ('8', self.button_press), ('9', self.button_press), ('÷', self.button_press),
            ('4', self.button_press), ('5', self.button_press), ('6', self.button_press), ('x', self.button_press),
            ('1', self.button_press), ('2', self.button_press), ('3', self.button_press), ('-', self.button_press),
            ('0', self.button_press), ('.', self.button_press), ('=', self.calculate), ('+', self.button_press),
            ('AC', self.clear), ('DEL', self.backspace), ('(', self.button_press), (')', self.button_press)
        ]
        
        button_colors = {
            'AC': COLORS['danger'],
            'DEL': COLORS['accent'],
            '=': COLORS['success'],
            '+': COLORS['primary'],
            '-': COLORS['primary'],
            'x': COLORS['primary'],
            '÷': COLORS['primary'],
            '(': COLORS['secondary'],
            ')': COLORS['secondary']
        }
        
        for text, callback in buttons:
            btn = Button(
                text=text,
                font_size=30,
                background_normal='',
                background_color=self.hex_to_rgb(button_colors.get(text, COLORS['light']))
            )
            if text == '=':
                btn.background_color = self.hex_to_rgb(COLORS['success'])
            elif text in 'ACDEL':
                btn.background_color = self.hex_to_rgb(COLORS['danger'] if text == 'AC' else COLORS['accent'])
            elif text in '+-x÷':
                btn.background_color = self.hex_to_rgb(COLORS['primary'])
            else:
                btn.background_color = (0.9, 0.9, 0.9, 1)
            
            btn.color = (0, 0, 0, 1) if text not in 'ACDEL=+-x÷' else (1, 1, 1, 1)
            btn.bind(on_press=lambda instance, t=text, c=callback: c(t))
            grid.add_widget(btn)
        
        self.add_widget(grid)
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4)) + (1,)
    
    def button_press(self, value):
        current = self.display.text
        if current == '0' or current == 'Error':
            self.display.text = value
        else:
            self.display.text = current + value
    
    def clear(self, value):
        self.display.text = '0'
    
    def backspace(self, value):
        current = self.display.text
        if len(current) > 1:
            self.display.text = current[:-1]
        else:
            self.display.text = '0'
    
    def calculate(self, value):
        try:
            expression = self.display.text.replace('x', '*')
            expression = self.display.text.replace('÷', '/')
            result = eval(expression, {"__builtins__": None}, {})
            self.display.text = str(result)
        except:
            self.display.text = 'Error'

class DailyLifeAssistantApp(App):
    def build(self):
        self.title = 'Life Hub Terminal'
        # self.icon='./logo.png'
        # Icon ke liye absolute path use karo
        import os
        import sys
        if hasattr(sys, '_MEIPASS'):
            # Agar EXE mein hai
            self.icon = os.path.join(sys._MEIPASS, 'logo.png')
        else:
            # Agar normal run kar rahe ho
            self.icon = './logo.png'
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        Window.size = (400, 700)
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    DailyLifeAssistantApp().run()