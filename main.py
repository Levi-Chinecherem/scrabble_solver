from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.popup import Popup
from backend import Board
import time

'''
Never lose Scrabble again

Variables: 
hand_columns = list of letters 
board_columns = list of list of letters 
test
'''

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')

class Boxes(GridLayout):
    def __init__(self, **kwargs):
        super(Boxes, self).__init__(**kwargs)
        self.cols = 15
        self.board = []
        self.hand = []
        self.hand_columns = []
        self.board_columns = []
        self.on = -1

        #list of text input objects
        def add_top_gui():
            for i in range(15):
                rows = []
                for k in range(15):
                    rows.append(TextInput(multiline = False, write_tab = False, font_size=25,))
                self.board_columns.append(rows)
            #add text object widgets
            for i in self.board_columns:
                for k in i:
                    self.add_widget(k)
        add_top_gui()

        #test change every other color
        def paint_top_gui():
            count = 0
            for i in self.board_columns:
                for k in i:
                    if count in [0,7,14,105,119,210,217,224]:
                        k.background_color = (1, 0.302, 0.302, 0.8)
                        k.word_multiplier = 3
                        k.letter_multiplier = 1
                        k.padding = [15,6,6,6]
                    elif count in ([3, 11,36,38,45,52,59,92,96,98,102,108,116,122,
                    126,128,132,165,172,179,186, 188,212,220]):
                        k.background_color = (0.1,1 ,0.3,1)
                        k.word_multiplier = 1
                        k.letter_multiplier = 2
                        k.padding = [15,6,6,6]
                    elif count in [16,28,32,42,48,56,64,70,154,160,168,176,182,192,196,208]:
                        k.background_color = (0.969, 0.776, 0.706,1)
                        k.word_multiplier = 2
                        k.letter_multiplier = 1
                        k.padding = [15,6,6,6]
                    elif count in [20,24,76,80,84,88,136,140,144,148,200,204]:
                        k.background_color = (0.1,1 ,0.4,0.6)
                        k.word_multiplier = 1
                        k.letter_multiplier = 3
                        k.padding = [15,6,6,6]
                    elif count == 112:
                        k.background_color = (0.886, 0.6, 0.498,1)
                        k.word_multiplier = 1
                        k.letter_multiplier = 1
                        k.padding = [15,6,6,6]
                    else:
                        k.word_multiplier = 1
                        k.letter_multiplier = 1
                        k.padding = [15,6,6,6]

                    count += 1
        paint_top_gui()

        def add_bottom_gui():
            #filler
            for i in range(self.cols-6):
                self.add_widget(Label(text = '',line_height = 10,))

            # on number
            self.on_label = Label(text = '')
            self.add_widget(self.on_label)
            # out of number
            self.out_of_label = Label(text = '')
            self.add_widget(self.out_of_label)

            #filler
            for i in range(4):
                self.add_widget(Label(text = '',line_height = 10,))

            enter_btn = Button(text = 'Enter')
            enter_btn.bind(on_press=self.new_enter)
            self.add_widget(enter_btn)

            clear_btn = Button(text = 'Clear')
            clear_btn.bind(on_press = self.clear)
            self.add_widget(clear_btn)


            #list of hand input objects
            for i in range(7):
                self.hand_columns.append(TextInput(multiline = False, write_tab = False, font_size=20))

            for i in self.hand_columns:
                self.add_widget(i)

            self.prev_btn = Button(text = '<', font_size = 20)
            self.prev_btn.bind(on_press = self.prev_func)
            self.add_widget(self.prev_btn)

            self.next_btn = Button(text = '>', font_size = 20)
            self.next_btn.bind(on_press = self.next_func)
            self.add_widget(self.next_btn)

            self.score_label = Label(text = '', font_size = 20)
            self.add_widget(self.score_label)

        add_bottom_gui()

    def prev_func(self, btn):
        if self.on == -1 or self.on == 0:
            pass
        elif self.on == 1:
            self.on -= 1
            self.clean_board()
            self.on_label.text = str(self.on)
            self.score_label.text = ''
        else:
            self.on -= 1
            self.paint_words()
            self.on_label.text = str(self.on)

    def next_func(self,btn):
        if self.on == -1 or self.on == len(self.lst_sorted):
            pass
        else:
            self.on += 1
            self.paint_words()
            self.on_label.text = str(self.on)

    def clean_board(self):
        outer_count = 0
        for i in self.board_columns:
            inner_count = 0
            for k in i:
                k.text = self.board[outer_count][inner_count]
                k.foreground_color = (0,0,0,1)
                inner_count +=1
            outer_count += 1

    def paint_words(self):
        self.clean_board()
        word_info = self.lst_sorted[self.on-1]
        count = 0
        word = word_info[0]
        point = word_info[1]
        coordinates = word_info[3],word_info[4]
        orientation = word_info[2]
        if orientation == 0:
            for w in word:
                grid_location = self.board_columns[coordinates[0]][coordinates[1] + count]
                grid_location.text = w
                count += 1
        else:
            for w in word:
                grid_location = self.board_columns[coordinates[1] + count][coordinates[0]]
                grid_location.text = w
                count += 1
        self.score_label.text = str(point)

    def new_enter(self,btn):
        for i in self.board_columns:
            for k in i:
                string = k.text
                if len(string) > 0:
                    k.text = string[0]
                    k.scroll_x = 0
        return self.enter()

    def enter(self):

        def quick_sort(word_lst):
            '''
            sorts a list of words by points formatted by:
            [word, point, orientation, rows, column]
            '''
            if not word_lst:
                return []
            center = word_lst[0]
            less_than = [x for x in word_lst if x[1] < center[1]]
            greater_than = [x for x in word_lst if x[1] > center[1]]
            center = [x for x in word_lst if x[1] == center[1]]
            return quick_sort(greater_than) + center + quick_sort(less_than)

        self.board,self.hand, self.on = [],[], 1
        for i in self.board_columns:
            rows = []
            for k in i:
                rows.append(k.text.lower())
            self.board.append(rows)
        for i in self.hand_columns:
            self.hand.append(i.text.lower())
        board_object = Board(self.board,''.join(self.hand), self.board_columns)
        self.lst_sorted = quick_sort(board_object.words)
        self.out_of_label.text = str(len(self.lst_sorted))
        self.on = 0
        self.on_label.text = str(self.on)
        
    def clear(self,btn):
        for i in self.board_columns:
            for k in i:
                k.text = ''
        for i in self.hand_columns:
            i.text = ''
        self.on = -1
        self.on_label.text = ''
        self.out_of_label.text = ''
        self.score_label.text = ''

class MyApp(App):
    def build(self):
        return Boxes()

if __name__ == '__main__':
    MyApp().run()
