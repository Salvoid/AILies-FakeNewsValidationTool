# [Imports]====================================================================================================
import tkinter as tkgui # Import tkinter for GUI
import tkinter.ttk as tkttk # Import tkinter themed widgets for GUI Themes
import tkinter.scrolledtext as tkst # Import tkinter scrolled textbox for adding Scroll Textbox
import other_module as otherModule # Other needed functions

# [Declarations & Initializations]====================================================================================================
color_mainBlue = '#253af7'
color_mainRed = '#db3745'
color_black = '#000000'
color_white = '#ffffff'
color_gray = '#828282'
color_lightGray = '#cfcfcf'
color_red = '#eb1313'
color_blue = '#1321eb'

font_title = 'helvetica'
font_label = 'helvetica'
font_content = 'consolas'

count_consoleLineNumber = 0 # Global Variable Declaration
socialMedia = "-" # Global Variable Declaration
tkgui_Entry_f1 = None # Global Variable Declaration
tkgui_ScrolledText_f2 = None # Global Variable Declaration

# [Functions]====================================================================================================
# [Display Main Window Frame and Components.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def display_widget_main(in_func_mainprocess):
    # [Initialize Widgets]--------------------------------------------------
    # [window(Tk)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # =============================
    tkgui_window = tkgui.Tk() #Create a window(GUI)
    tkgui_window.minsize(700,500)
    tkgui_window.title("AlLies: Fake News Validation Tool")
    tkgui_window.iconbitmap(otherModule.define_relativepath(False,"assets\\images\\window_icon.ico"))
    tkgui_window.columnconfigure(0, weight=1)
    tkgui_window.rowconfigure(0, weight=1)

    # [Display Widgets]--------------------------------------------------
    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    tkgui_Frame_main = tkgui.Frame(tkgui_window)
    tkgui_Frame_main.grid(row=0, column=0, padx=5, pady=20, sticky='NSWE')
    tkgui_Frame_main.columnconfigure(0, weight=1)
    tkgui_Frame_main.rowconfigure(2, weight=1)
    tkgui_Frame_main.rowconfigure(3, weight=5)

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # title(Canvas)=============================
    tkgui_Canvas_title_height = 40
    tkgui_Canvas_title_width = 600
    tkgui_Canvas_title = tkgui.Canvas(tkgui_Frame_main)
    tkgui_Canvas_title.config(
        height=tkgui_Canvas_title_height, 
        width=tkgui_Canvas_title_width
    )
    tkgui_Canvas_title.create_text((tkgui_Canvas_title_width/2)-150, 20, anchor='c', text="AlLies: ", fill=color_mainBlue, font=(font_title,20,'bold'))
    tkgui_Canvas_title.create_text((tkgui_Canvas_title_width/2)+70, 20, text="Fake News Validation Tool", fill=color_mainRed, font=(font_title,20,'bold'))
    tkgui_Canvas_title.grid(column=0, row=0, sticky='N')

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f1(Frame)=============================
    tkgui_Frame_f1 = tkgui.Frame(tkgui_Frame_main)
    tkgui_Frame_f1.grid(column=0, row=1, sticky='NSWE')
    tkgui_Frame_f1.columnconfigure(0, weight=1)
    tkgui_Frame_f1.columnconfigure(1, weight=1)
    tkgui_Frame_f1.columnconfigure(2, weight=1)
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f1(Label)=============================
    tkgui_Label_f1 = tkgui.Label(tkgui_Frame_f1)
    tkgui_Label_f1['text'] = "Input URL"
    tkgui_Label_f1.config(
        fg=color_black, 
        font=(font_label,15,'bold')
    )
    tkgui_Label_f1.grid(column=0, row=0, padx=20, pady=4, columnspan=3, sticky='W')
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f1(Entry)=============================
    global tkgui_Entry_f1 # Used to edit a variable's value
    tkgui_Entry_f1_height = 14
    tkgui_Entry_f1 = tkgui.Entry(tkgui_Frame_f1)
    tkgui_Entry_f1.config(
        fg=color_black, 
        bg=color_lightGray, 
        font=(font_content,tkgui_Entry_f1_height,''), 
        borderwidth=3, 
        relief=tkgui.SUNKEN, 
        state=tkgui.NORMAL
    )
    tkgui_Entry_f1.grid(column=0, row=1, padx=20, pady=4, columnspan=3, sticky='NSWE')
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # socialMedia(OptionMenu)=============================
    socialMedia_chosen = tkgui.StringVar()
    socialMedia_chosen.set(socialMedia) # Initialize default Media Sort Type
    mediaSort_options = [
        "-", 
        "Twitter", 
        "Facebook"
    ]
    tkgui_Button_socialMedia = tkgui.OptionMenu(tkgui_Frame_f1, socialMedia_chosen, *mediaSort_options, command=lambda _: change_socialmedia(socialMedia_chosen.get()))
    tkgui_Button_socialMedia.config(
        fg=color_white, 
        bg=color_gray, 
        font=(font_label,12,'bold'), 
        borderwidth=5, 
        relief=tkgui.RAISED, 
        state=tkgui.NORMAL
    )
    tkgui_Button_socialMedia.grid(column=0, row=2, padx=20, pady=4, sticky='WE')
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # check(Button)=============================
    tkgui_Button_validate = tkgui.Button(tkgui_Frame_f1)
    tkgui_Button_validate['text'] = "CHECK VALIDITY"
    tkgui_Button_validate['command'] = lambda: process_request(in_func_mainprocess)
    tkgui_Button_validate.config(
        fg=color_white, 
        bg=color_gray, 
        font=(font_label,12,'bold'), 
        borderwidth=5, 
        relief=tkgui.RAISED, 
        state=tkgui.NORMAL
    )
    tkgui_Button_validate.grid(column=1, row=2, padx=20, pady=4, sticky='WE')
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # clear(Button)=============================
    tkgui_Button_clear = tkgui.Button(tkgui_Frame_f1)
    tkgui_Button_clear['text'] = "CLEAR FIELDS"
    tkgui_Button_clear['command'] = lambda: clear_fields()
    tkgui_Button_clear.config(
        fg=color_white, 
        bg=color_gray, 
        font=(font_label,12,'bold'), 
        borderwidth=5, 
        relief=tkgui.RAISED, 
        state=tkgui.NORMAL
    )
    tkgui_Button_clear.grid(column=2, row=2, padx=20, pady=4, sticky='WE')

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f2(Frame)=============================
    tkgui_Frame_f2 = tkgui.Frame(tkgui_Frame_main)
    tkgui_Frame_f2.grid(column=0, row=2, sticky='NSWE')
    tkgui_Frame_f2.columnconfigure(0, weight=1)
    tkgui_Frame_f2.rowconfigure(1, weight=1)
    # [f2(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f2(Label)=============================
    tkgui_Label_f2 = tkgui.Label(tkgui_Frame_f2)
    tkgui_Label_f2['text'] = "Instructions"
    tkgui_Label_f2.config(
        fg=color_black, 
        font=(font_label,15,'bold')
    )
    tkgui_Label_f2.grid(column=0, row=0, padx=20, pady=4, sticky='W')
    # [f2(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f2(ScrolledText(Custom))=============================
    global tkgui_ScrolledText_f2 # Used to edit a variable's value
    tkgui_ScrolledText_f2_height = 7
    tkgui_ScrolledText_f2 = tkst.ScrolledText(tkgui_Frame_f2)
    tkgui_ScrolledText_f2.config(
        height=tkgui_ScrolledText_f2_height, 
        fg=color_black, 
        bg=color_lightGray, 
        font=(font_content,12,''), 
        undo=True, 
        wrap=tkgui.WORD, 
        borderwidth=3, 
        relief=tkgui.SUNKEN, 
        state=tkgui.DISABLED
    )
    tkgui_ScrolledText_f2.tag_config('textTag_normalboldtext', foreground=color_black, font=(font_content,12,'bold'))
    tkgui_ScrolledText_f2.tag_config('textTag_task', foreground=color_black, font=(font_content,12,'italic'))
    tkgui_ScrolledText_f2.tag_config('textTag_process', foreground=color_red, font=(font_content,12,))
    tkgui_ScrolledText_f2.tag_config('textTag_finish', foreground=color_blue, font=(font_content,12,))
    tkgui_ScrolledText_f2.grid(column=0, row=1, padx=20, pady=4, sticky='NSWE')

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f3(Frame)=============================
    tkgui_Frame_f3 = tkgui.Frame(tkgui_Frame_main)
    tkgui_Frame_f3.grid(column=0, row=3, sticky='NSWE')
    tkgui_Frame_f3.columnconfigure(0, weight=1)
    tkgui_Frame_f3.rowconfigure(1, weight=1)
    # [f3(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f3(Label)=============================
    tkgui_Label_f3 = tkgui.Label(tkgui_Frame_f3)
    tkgui_Label_f3['text'] = "Console"
    tkgui_Label_f3.config(
        fg=color_black, 
        font=(font_label,15,'bold')
    )
    tkgui_Label_f3.grid(column=0, row=0, padx=20, pady=4, sticky='W')
    # [f3(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f3(ScrolledText(Custom))=============================
    global tkgui_ScrolledText_f3 # Used to edit a variable's value
    tkgui_ScrolledText_f3_height = 10

    tkgui_ScrolledText_f3 = tkst.ScrolledText(tkgui_Frame_f3)
    tkgui_ScrolledText_f3.config(
        height=tkgui_ScrolledText_f3_height, 
        fg=color_black, 
        bg=color_lightGray, 
        font=(font_content,12,''), 
        undo=True, 
        wrap=tkgui.WORD, 
        borderwidth=3, 
        relief=tkgui.SUNKEN, 
        state=tkgui.DISABLED
    )
    tkgui_ScrolledText_f3.tag_config('textTag_normalboldtext', foreground=color_black, font=(font_content,12,'bold'))
    tkgui_ScrolledText_f3.tag_config('textTag_task', foreground=color_black, font=(font_content,12,'italic'))
    tkgui_ScrolledText_f3.tag_config('textTag_process', foreground=color_red, font=(font_content,12,))
    tkgui_ScrolledText_f3.tag_config('textTag_finish', foreground=color_blue, font=(font_content,12,))
    tkgui_ScrolledText_f3.grid(column=0, row=1, padx=20, pady=4, sticky='NSWE')

    text_instructions()

    return tkgui_window

# [Changes social media source.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def change_socialmedia(in_socialMedia_value):
    global socialMedia
    socialMedia = in_socialMedia_value

# [Check if social media source is valid.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_request(in_func_mainprocess):
    # processStatus
        # None --> Unknown Error Occured
        # 0 --> Success
        # 1 --> URL Field is Empty
        # 2 --> Wrong URL Format Length
        # 3 --> No Social Media selected
        # 4 --> URL Format Doesn't Match Twitter Tweet URL Format
        # 5 --> URL Format Doesn't Match Facebook Post URL Format
        # 6 --> Correct Twitter Tweet URL
        # 7 --> Correct Text/Image Facebook Post URL
        # 8 --> Group Facebook Post
        # 9 --> Video Facebook Post
        # 10 --> Twitter Tweet doesn't Exist
        # 11 --> Facebook Post doesn't Exist
        # 12 --> Twitter Tweet Fetch Failed
        # 13 --> Facebook Post Fetch Failed
    processStatus = None
    urlContentValidation = None
    url_input = tkgui_Entry_f1.get() # Get start to end of input excluding last character
    
    print_console(True, False, "URL Input: ", 'textTag_task')
    print_console(False, True, url_input, 'textTag_normalboldtext')
    
    print_console(True, False, "Social Media: ", 'textTag_task')
    print_console(False, True, socialMedia, 'textTag_normalboldtext')

    print_console(True, False, "Content Fetch Status: ", 'textTag_task')
    print_console(False, True, "Validating URL Link Format...", 'textTag_process')

    processStatus, urlContentValidation = in_func_mainprocess(socialMedia, url_input)

    if processStatus == 0:
        print_console(True, False, "Content Validation Status: ", 'textTag_process')
        print_console(False, True, "Success.", 'textTag_process')
        print_console(True, False, "Content Validity: ", 'textTag_normalboldtext')
        if urlContentValidation == "real":
            print_console(False, True, "REAL", 'textTag_finish')
        elif urlContentValidation == "fake":
            print_console(False, True, "FAKE", 'textTag_finish')
    if processStatus == 1:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... URL Field is Empty.", 'textTag_process')
    if processStatus == 2:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... Wrong URL Format Length.", 'textTag_process')
    if processStatus == 3:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... No Social Media selected.", 'textTag_process')
    if processStatus == 4:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... URL Format Doesn't Match Twitter Tweet URL Format.", 'textTag_process')
    if processStatus == 5:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... URL Format Doesn't Match Facebook Post URL Format.", 'textTag_process')
    if processStatus == 10:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... Twitter Tweet doesn't Exist.", 'textTag_process')
    if processStatus == 11:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... Facebook Post doesn't Exist.", 'textTag_process')
    if processStatus == 12:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... Twitter Tweet Fetch Failed.", 'textTag_process')
    if processStatus == 13:
        print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        print_console(False, True, "ERROR... Facebook Post Fetch Failed.", 'textTag_process')
    elif processStatus == None:
        print_console(True, False, "System Status: ", 'textTag_task')
        print_console(False, True, "ERROR... Unknown Error Occured.", 'textTag_process')

# [Clear Fields(Process) after clicking CLEAR FIELDS(Button)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def clear_fields():
    tkgui_Entry_f1.delete("0", tkgui.END) # (For Entry)Clear start to end of input

    tkgui_ScrolledText_f3.config(state=tkgui.NORMAL) # Enable Locked Text(Textarea)
    tkgui_ScrolledText_f3.delete("1.0", tkgui.END) # (For Text(Textarea))Clear start to end of input
    tkgui_ScrolledText_f3.config(state=tkgui.DISABLED) # Disable Locked Text(Textarea)

    global count_consoleLineNumber # Used to edit a variable's value
    count_consoleLineNumber = 0

    global inputPost # Used to edit a variable's value
    inputPost = None

# [Print To Instructions(Process)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_instructions(in_addcount_consoleLineNumber, in_addNewline, in_insertText, in_textTag):
    global count_consoleLineNumber # Used to edit a variable's value
    tkgui_ScrolledText_f2.config(state=tkgui.NORMAL) # Enable Locked Text(Textarea)
    if in_addcount_consoleLineNumber:
        count_consoleLineNumber += 1
        tkgui_ScrolledText_f2.insert(tkgui.END, '[' + str(count_consoleLineNumber) + ']', 'textTag_normalboldtext') # Insert Console Line Number on Text(Textarea)
    
    if in_addNewline:
        tkgui_ScrolledText_f2.insert(tkgui.END, in_insertText + '\n', in_textTag) # Insert to End Text(Textarea) with newline
    else:
        tkgui_ScrolledText_f2.insert(tkgui.END, in_insertText, in_textTag) # Insert to End Text(Textarea)
    tkgui_ScrolledText_f2.config(state=tkgui.DISABLED) # Disable Locked Text(Textarea)
    tkgui_ScrolledText_f2.see(tkgui.END)

# [Print To Console(Process)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_console(in_addcount_consoleLineNumber, in_addNewline, in_insertText, in_textTag):
    global count_consoleLineNumber # Used to edit a variable's value
    tkgui_ScrolledText_f3.config(state=tkgui.NORMAL) # Enable Locked Text(Textarea)
    if in_addcount_consoleLineNumber:
        count_consoleLineNumber += 1
        tkgui_ScrolledText_f3.insert(tkgui.END, '[' + str(count_consoleLineNumber) + ']', 'textTag_normalboldtext') # Insert Console Line Number on Text(Textarea)
    
    if in_addNewline:
        tkgui_ScrolledText_f3.insert(tkgui.END, in_insertText + '\n', in_textTag) # Insert to End Text(Textarea) with newline
    else:
        tkgui_ScrolledText_f3.insert(tkgui.END, in_insertText, in_textTag) # Insert to End Text(Textarea)
    tkgui_ScrolledText_f3.config(state=tkgui.DISABLED) # Disable Locked Text(Textarea)
    tkgui_ScrolledText_f3.see(tkgui.END)

# [Set Widget Options.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def set_widget_options(in_tkgui_window):
    style = tkttk.Style()
    style.theme_use('clam')

    in_tkgui_window.resizable(True, True) #Window resizability: Width = True; Height = True;
    in_tkgui_window.mainloop() #Keeps the window(GUI) active/displayed on screen

# [Set Instructions.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def text_instructions():
        print_instructions(True, True, "Validate Content: ", 'textTag_normalboldtext')
        print_instructions(True, True, "-Select Social Media from the Dropdown Menu.", '')
        print_instructions(True, True, "-Paste the appropriate and working URL according to the Social Media selected URL Format below.", '')
        print_instructions(True, True, "-Click the 'Check Validity' button.", '')
        print_instructions(True, True, "-See the Console Area to check for the progress, errors, and final validation.", '')
        print_instructions(True, True, "-Wait for the fetching and validation process to finish.", '')
        print_instructions(True, True, "-If all processes is working, validation will be printed on the Console Area with the caption 'Content Validity'.", '')

        print_instructions(False, True, "", 'textTag_task')
        
        print_instructions(True, True, "URL Format: ", 'textTag_normalboldtext')
        print_instructions(True, False, "Twitter: ", 'textTag_finish')
        print_instructions(False, True, "{http/https}://{www.twitter.com/twitter.com}/(Twitter Username)/status/(Tweet Number)", 'textTag_task')
        print_instructions(True, False, "Facebook Text/Image Post: ", 'textTag_finish')
        print_instructions(False, True, "{http/https}://{www.facebook.com/facebook.com}/(Facebook Username)/posts/(Facebook Post Number Code)", 'textTag_task')
        print_instructions(True, False, "Facebook Group Post: ", 'textTag_finish')
        print_instructions(False, True, "{http/https}://{www.facebook.com/facebook.com}/groups/(Facebook Group Number)/posts/(Facebook Post Number)", 'textTag_task')
        print_instructions(True, False, "Facebook Video Post: ", 'textTag_finish')
        print_instructions(False, True, "{http/https}://{www.facebook.com/facebook.com}/(Facebook Group Name)/videos/(Facebook Post Short Description)/(Facebook Post Number)", 'textTag_task')

        print_instructions(False, True, "", 'textTag_task')

        print_instructions(True, True, "Clear Fields: ", 'textTag_normalboldtext')
        print_instructions(True, True, "-Click the 'Check Validity' button.", '')
        print_instructions(True, True, "-Both Input URL and Console Area will be cleared from text.", '')
