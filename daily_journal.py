from tkinter import *
from datetime import date, timedelta
from os import listdir
from tkinter import ttk
from tkinter import font
import calendar


class DailyJournal():
    def __init__(self, master):

        self.daily_journal_path = 'C:/Users/USER/Desktop/Daily_Journal/'


        self.today = str(date.today())
        self.today_file = self.today + '.txt'
        self.yesterday = str(date.today() - timedelta(days=1))
        self.yesterday_file = self.yesterday + '.txt'
        self.top_text_box_current_file = self.today + '.txt'
        self.font_helvetica = 'Helvetica'

        self.font_style = self.font_helvetica

        self.font_size = 10
        self.bold = False
        self.italic = False
        self.underline = False
        self.font = (self.font_style, self.font_size)


        self.template_file_content = ''

        # Styling for widgets
        self.relief_style = 'groove'
        self.brd_width = 3
        self.btb_colour = 'white'
        self.ttb_colour = 'white'
        self.slb_colour = 'white'
        self.tlbr_colour = 'white'

        s = ttk.Style()
        #s.theme_use('alt')
        print(s.theme_use())
        print(s.theme_names())
        s.configure('new.TButton', weight='bold', background='blue')

        self.frame = Frame(master)
        self.frame.grid(sticky='nswe')

        # weight=0 makes column/row not expand when window is moved
        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(3, weight=0)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.createUI()

    def createUI(self):

        #Create toolbar frame and widgets inside of toolbar
        self.toolbar = Frame(self.frame, bg=self.tlbr_colour, relief=self.relief_style, bd=self.brd_width)
        self.toolbar.grid(row=0, columnspan='4', sticky='nswe')
        # In the command option do not put self.tlbr_save() as the brackets call the function without the button being
        # pressed and foxing schtuff up
        self.tlbr_save_image = PhotoImage(file='save-disk.png')
        self.tlbr_goal_image = PhotoImage(file='trophy.png')
        self.tlbr_q_image = PhotoImage(file='questioning.png')
        self.tlbr_save_button = ttk.Button(self.toolbar, image=self.tlbr_save_image, command=self.tlbr_save)
        self.tlbr_save_button.pack(side='left')
        self.tlbr_goals_btn = ttk.Button(self.toolbar, image=self.tlbr_goal_image, command= self.load_goals)
        self.tlbr_goals_btn.pack(side='left')
        self.tlbr_goals_btn.bind('<Double-Button-1>', self.on_dbl_goals_btn)

        self.settings_img = PhotoImage(file='settings.png')
        self.tlbr_settings_btn = ttk.Button(self.toolbar, image= self.settings_img)
        self.tlbr_settings_btn.pack(side='right')

        self.tlbr_q_btn = ttk.Button(self.toolbar, image=self.tlbr_q_image, command=self.load_prompt_qs)
        self.tlbr_q_btn.pack(side='left')
        self.tlbr_q_btn.bind('<Double-Button-1>', self.on_dbl_q_btn)

        #self.tlbr_lbl = ttk.Label(self.toolbar, text = self.top_text_box_current_file )
        #self.tlbr_lbl.pack(side=LEFT)

        # Font styling buttons on left hand side of toolbar
        boldfont = font.Font(family=self.font_style, weight='bold')
        nonboldfont = font.Font(family=self.font_style, weight='normal')
        helv36 = font.Font(family='Helvetica', size=36, weight='bold')
        self.t_pic = PhotoImage(file= 'underline-text.png')
        self.bold_pic = PhotoImage(file='bold-text.png')
        self.font_style_btn = ttk.Button(self.toolbar, image = self.t_pic)
        self.font_style_btn.pack(side='right', fill=BOTH)
        #self.font_bold_btn = ttk.Button(self.toolbar, image= self.bold_pic)
        #self.font_bold_btn.pack(side='right', fill=BOTH)


        self.top_text_box = Text(self.frame, bg=self.ttb_colour, padx=5, pady=5, wrap=WORD, relief=self.relief_style,
                                 bd=self.brd_width, font=self.font)
        self.top_text_box.grid(row=1, column=1, sticky='nsew')
        self.bottom_text_box = Text(self.frame, bg= self.btb_colour, padx=5, pady=5, wrap=WORD, relief=self.relief_style,
                                    bd=self.brd_width, font=self.font)
        self.bottom_text_box.grid(row=2, column=1, sticky='nswe')

        # Scollbar widgets for the text boxes
        self.scrollbar_top = Scrollbar(self.frame)
        self.scrollbar_top.config(command=self.top_text_box.yview)
        self.top_text_box.config(yscrollcommand=self.scrollbar_top.set)
        self.scrollbar_top.grid(row=1, column=3, sticky='nswe')
        self.scrollbar_bottom = Scrollbar(self.frame)
        self.scrollbar_bottom.config(command=self.bottom_text_box.yview)
        self.bottom_text_box.config(yscrollcommand=self.scrollbar_bottom.set)
        self.scrollbar_bottom.grid(row=2, column=3, sticky='nswe')
        self.scrollbar_top.config(background='#000000')

        # Side listbox with the daily journal files listed set up
        self.side_listbox = Listbox(self.frame, relief=self.relief_style, bd=self.brd_width, bg= self.slb_colour)
        # activestyle = 'none' stops the selected item in the listbox from being underlined
        self.side_listbox.config(activestyle='none')
        self.side_listbox.grid(row=1, rowspan=2, column=0, sticky='nsew')
        # double click item in listbox calls on_dbl_listbox function
        self.side_listbox.bind('<Button-1>', self.on_dbl_listbox)
        self.side_listbox.bind('<Button-3>', self.on_rightclk_listbox)


        # Load listbox
        self.load_side_listbox()

        # Fill  top text box with today's journal entry
        self.open_journal_entry(self.today_file, 'top_text_box')

        # Fill bottom text box with yesterdays journal entry
        self.open_journal_entry(self.yesterday_file, 'bottom_text_box')

    '''def text_selection_format(self):
        #selected_text = self.top_text_box.selection_get()

        if self.bold == True:
            self.bold = False
            self.font.Font(weight='bold')
        else:
            self.bold = True
            self.font.Font(weight='normal')'''
    def on_rightclk_listbox(self, event):
        widget = event.widget
        selection = widget.curselection()
        selected_date = widget.get(selection[0])
        self.open_journal_entry(selected_date, 'top_text_box')


    def on_dbl_goals_btn(self, event):
        self.open_journal_entry('Goals.txt', 'top_text_box')

    def on_dbl_q_btn(self, event):
        self.open_journal_entry('DailyJournalQs.txt', 'top_text_box')

    def load_prompt_qs(self):
        self.open_journal_entry('DailyJournalQs.txt', 'bottom_text_box')

    def load_goals(self):
        self.open_journal_entry('Goals.txt', 'bottom_text_box')

    def on_dbl_listbox(self, event):
        widget = event.widget
        selection = widget.curselection()
        selected_date = widget.get(selection[0])
        self.open_journal_entry(selected_date, 'bottom_text_box')

    def load_side_listbox(self):
        self.side_listbox_list = listdir(self.daily_journal_path)
        i=0
        for item in self.side_listbox_list:
            if item[0] == '2':
                self.side_listbox.insert(END, item)

                idate = item[0:10]
                iyear = idate[0:4]
                imonth= idate[5:7]
                iday = idate[8:10]
                iweekday = date(int(iyear), int(imonth), int(iday)).isoweekday()
                print(iweekday)
                if iweekday == 6 or iweekday == 7:
                    self.side_listbox.itemconfig([i], foreground="red")
                i+= 1


    def open_journal_entry(self, entry_date_file, text_box):
        if text_box == 'top_text_box':
            self.top_text_box.delete(1.0, END)
            journal_content = self.get_journal_content(entry_date_file)
            self.top_text_box.insert(1.0, journal_content)
            # Set top_text_box_current_file to the file being displayed in the top text file
            self.top_text_box_current_file = str(entry_date_file)
        elif text_box == 'bottom_text_box':
            # Delete current content out the bottom text box
            self.bottom_text_box.delete(1.0, END)
            journal_content = self.get_journal_content(entry_date_file)
            self.bottom_text_box.insert(1.0, journal_content)

    def get_journal_content(self, journal_date_file):
        daily_file_dir = listdir(self.daily_journal_path)
        daily_file_name = str(journal_date_file)
        daily_file_path = self.daily_journal_path + daily_file_name
        if daily_file_name in daily_file_dir:
            f_daily_file = open(daily_file_path, 'r')
            file_content = f_daily_file.read()
            f_daily_file.close()
            return file_content
        else:
            self.create_new_daily_entry_file(self.today_file)
            template_file_name = 'Daily_template.txt'
            template_file_path = self.daily_journal_path + template_file_name
            f_template_file = open(template_file_path, 'r')
            # Have to make template_file_content not local as otherwise when it is returned it looses its value!
            self.template_file_content = f_template_file.read()
            f_template_file.close()
            return self.template_file_content

    def create_new_daily_entry_file(self, journal_date_file):
        new_entry_file_name = journal_date_file
        new_entry_file_path = self.daily_journal_path + new_entry_file_name
        file_new = open(new_entry_file_path, 'w')
        file_new.close()

    def tlbr_save(self):

        current_file_path = self.daily_journal_path + self.top_text_box_current_file
        fopen = open(current_file_path, 'w')
        content_to_save = self.top_text_box.get(1.0, END)
        fopen.write(content_to_save)
        fopen.close()


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# Maximise the window but not underneath the toolbar
root.state('zoomed')
root.wm_title('Daily Journal')
app = DailyJournal(root)
root.mainloop()
