'''
Backend for scrabble 

variables
board: list of lists representative of the gui board
hand: list of letters representative of the gui hand

Classes
Words: grabs words from engmix.text, puts them into a set 
Scrabble: 

'''

class Words:
    words_dict = {}
    x = open('dictionaryOfWords.txt','rt', encoding='latin1') #replace dictionaryOfWords.txt if using another txt file
    for line in x:
        line = line.strip()
        length = len(line)
        if length in words_dict:
            words_dict[length].add(line)
        else:
            words_dict[length] = set(line)

class Scrabble(Words):

    def __init__(self, board, hand, row_num, row, board_columns, orientation):
        self.board,self.board_columns = board, board_columns
        self.row_num = row_num
        self.row = row
        self.orientation = orientation #0 for horizontal, 1 for vertical
        self.row_concat = ''.join(row)
        self.max, self.min = len(self.row)+1, 2
        self.hand = hand + self.row_concat
        self.words = self.unscrabble()


    def unscrabble(self):
        '''
        returns a list of words that can be generated from board letters and
        hand letters
        '''
        lst = []
        for i in range(self.min, self.max):
            #runs through all english words
            for b in self.words_dict[i]:
                #check if has letter on board
                for k in self.row_concat:
                    if k in b:
                        flag, count = True, 0
                        for w in b:
                            if b.count(w) > self.hand.count(w):
                                flag = False
                                break 
                        if flag:
                            lst.append(b)
        return self.form_check(self.row, lst)

    def form_check(self, form, word_list):
        '''
        checks to see if a word matches the form
        >>> form = ['','u','c','','']
        >>> word_list = ['fuck','truck','tuck','stuck']
        >>> form_check(form, word_list)
        ['fuck', 'tuck']

        >>> form = ['b','','u','c','','']
        >>> form_check(form, word_list)
        []

        >>> form = ['b','','','u','c','','']
        >>> form_check(form, word_list)
        ['fuck', 'tuck']
        '''
        updated = []
        def form_check_helper(form, sliced_hand, hand, length, previous, count):
            if len(form) < length:
                return 
            clean_form = form[:]     
            pointer_form, pointer_hand = 0,0
            #Iterate through form, checking to see if once concatenated word is formed
            while pointer_form < len(form) and pointer_hand < len(sliced_hand):
                if form[pointer_form] == '':
                    form[pointer_form] = sliced_hand[pointer_hand]
                    pointer_form, pointer_hand = pointer_form + 1, pointer_hand + 1
                else:
                    pointer_form += 1
            #Check next letter after last to see if it is blank
            concat = ''.join(form[:length])
            if concat == hand:
                if length < len(form):
                    if previous + concat + form[length] == hand and self.not_all_board(
                        clean_form, hand):
                        if self.vertical_check(form,count,hand):
                            score = self.point_counter(hand, count)
                            return [hand, score, self.orientation, self.row_num, count]
                elif previous + concat == hand and self.not_all_board(clean_form, hand):
                    if self.vertical_check(form,count,hand):
                        score = self.point_counter(hand, count)
                        return [hand, score, self.orientation, self.row_num, count]
                return
            return form_check_helper(clean_form[1:], sliced_hand, 
                hand, length, clean_form[0], count + 1)

        form_join = ''.join(form)
        #Iterate through words
        for w in word_list:
            copy_hand, copy_form = w, form[:]
            #Remove all letters in word on board
            for k in form_join:
                w = w.replace(k,'')
            #send to helper
            check = form_check_helper(copy_form, w, copy_hand, len(copy_hand), '', 0)
            if check and check not in updated:
                updated.append(check)
        return updated

    def vertical_check(self, form, count, hand):
        '''
        checks to see if another word is created by making the word, and verifies that that 
        word is an english word
        '''
        #cycle through word_list
        for i in range(len(hand)):
            if (self.row_num == 0 or self.board[self.row_num-1][count + i] != '' or 
                self.row_num == len(self.board) - 1 or self.board[self.row_num+1][count + i]):
                word, flag = '', False
                for k in range(len(self.board)):
                    if k == self.row_num:
                        word += form[i]
                        flag = True
                    elif self.board[k][count + i] != '':
                        word += self.board[k][count + i]
                    else:
                        if flag:
                            break
                        word = '' 
                if word != '' and word not in self.words_dict[len(word)] and word != form[i]:
                    return False
        return True

    def not_all_board(self,form, word):
        '''
        checks to see that a letter from the hand was placed, and not just returning already
        placed words
        '''
        unchanged_word = word
        letters = ''.join(form)
        for k in letters:
            word = word.replace(k,'')
        if word == '':
            return False
        return True



    def point_counter(self, word, count):
        ''' 
        counts the points per word 
        '''
        point_dict = {}
        #self.row_num = row
        #count = column

        def counter(letter):
            if (letter is 'a' or letter is 'e' or letter is 'i' or letter is 'n' or
                letter is 'o' or letter is 'r' or letter is 's' or letter is 't' or
                letter is 'u'):
                return 1
            elif (letter is 'd' or letter is 'g'):
                return 2
            elif (letter is 'b' or letter is 'c' or letter is 'm' or letter is 'p'):
                return 3
            elif (letter is 'f' or letter is 'h' or letter is 'v' or letter is 'w' or 
                letter is 'y'):
                return 4
            elif (letter is 'k'):
                return 5
            elif (letter is 'j' or letter is 'x'):
                return 8
            else:
                return 10
        points,word_multiplier,letter_multiplier = 0, 1, 1
        for w in word:
            for i in w:
                word_multiplier *= self.board_columns[self.row_num][count].word_multiplier
                letter_multiplier = self.board_columns[self.row_num][count].letter_multiplier
                points, count = points + letter_multiplier * counter(i), count + 1
        return points * word_multiplier

class Board(Scrabble):
    def __init__(self, board, hand, column):
        self.board = board
        self.board_columns = column
        self.hand = hand
        self.words = []
        self.enter()

    def enter(self):
        '''
        cycles through all of the rows and columns to check for words
        '''
        row_num = 0
        # horizontal
        for b in self.board:
            if ''.join(b) != '':
                scrabble_object = Scrabble(self.board, self.hand, row_num, b, self.board_columns, 0).words
                if scrabble_object:
                    self.words.extend(scrabble_object)
            row_num += 1

        self.vertical_board = []

        # vertical
        for i in range(len(b)):
            row = []
            for b in self.board:
                row.append(b[i])
            self.vertical_board.append(row)
        row_num = 0
        for b in self.vertical_board:
            if ''.join(b) != '':
                scrabble_words = Scrabble(self.vertical_board, self.hand, row_num, b, self.board_columns, 1).words
                if scrabble_words:
                    self.words.extend(scrabble_words)
            row_num += 1



