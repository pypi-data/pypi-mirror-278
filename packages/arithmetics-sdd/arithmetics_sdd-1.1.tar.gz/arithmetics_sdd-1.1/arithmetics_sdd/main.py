try:
    #importing packages that are required to run the program

    from tkinter import *
    import customtkinter
    from tkinter import ttk
    from PIL import Image, ImageTk
    import pyttsx3
    from pathlib import Path
    from os import path

    directory_path = Path(__file__).resolve().parents[0]
    images_path = path.join(directory_path, "images")
    Text_path = path.join(directory_path, "Text")



    #configurations of the program
    fullscreen = False
    language = "english"

    ##setting many veriables to the same value

    #setting up statistics
    incorrect_counter=correct_counter=J=0

    #the flag veriable asigned to each level and storyboard scene
    l1=l2=l3=l4=l5= l6= l7= l8= l9= l10= l11= l12= l13= l14= l15= l16= l17= l18= l19=l20=L=menu_screen_state=options_menu_state=level_menu_state=level_selection_state=False

    #setting the level flags to a list to retrieve them quickly and do functions with all of them in a loop (Tomas hates manual lines compared to looping)
    lvl_list = [l1,l2,l3,l4,l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20]

    #Configuring the program root values
    root = customtkinter.CTk()
    root.title('Understanding Arithmetics: Interactive Experience')
    root.geometry("1280x720")
    root.minsize(width=1280, height=720)
    root.iconbitmap(path.join(images_path, "program_icon.ico"))
    customtkinter.deactivate_automatic_dpi_awareness()

    #Obtains languages from google translate and puts them in a list
    language_list=[
    'afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 
    'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 
    'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hebrew', 'hindi', 'hmong',
    'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz',
    'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)',
    'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona',
    'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 
    'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']

    #the answers for each question (index is the question number)
    answers_list = [1,3,4,3,2,4,3,1,3,2,4,1,1,3,2,3,2,2,2,4]



    #this function closes the application from the "exit" button from the main menu
    def close_app():
        root.destroy()



    #this function reads the text files which are found in the text files directory in the parent folder of the main.py
    def read_text():
        global text_file, language

        #try is required since this function needs to run at least once when the program starts to get the english files
        #for the first time the function is run, language is already set, so it doesnt matter if it cant get it from the
        #combobox as the function cannot retrive information from the translated combobox is not set yet so it passes

        try:
            language = translated_combo.get()
        except: pass


        #setting up the string value for the path to the language files, this can be done shorter *note, that could be a future update
        #files are decoded and encoded using UTF-8 which is what the google translate module uses so most characters are recongised such
        #as japanese or arabic characters

        file_path = path.join(Text_path, f"{language}.txt")
        files = open(file_path, encoding='utf-8')

        #the text_file list contains all the lines of text from the program in a list so it can be retireved quicker, for the first time
        #it is set up to be used, for any subsequent times the function is called, the old texts are wiped, allowing for the new language
        #text to be added and used instead
        text_file = []


        #the for loop reads every line in a txt file line by line and corects the division symbol and removed the \n part due to
        #the nature of python where print("words \n words1") prints out words and words1 in two lines
        #all the words are then appended to a list. Objects can now use any word from the list by using text_file[index] where
        #index is the position of the word in the list. 

        for i in files.readlines():
            add = i.replace("Ã·","÷")
            add = add.replace("\n","")
            text_file.append(add)


        #the try function is required for the first time the function is run (it runs with language = "english"), this occurs in the menu screen
        #where the veriables configered do not exist. However, for any subsequent time the function is run, it changes the text files and will apply
        #to other menus when they load, but do not update current objects. This section updates the options menu objects to translate since running
        #options menu again creates problems

        try:
            fullscreen_checkbox.configure(text = text_file[5])
            apply_button.configure(text = text_file[6])
            root.title(text_file[130])
        except: pass



    #this function switched the screen from fullscreen to not fullscreen and vice versa, fullscreen veriable is set before hand
    #and is toggled when the program is run
    def switch_screen_toggle():
        global fullscreen
        if fullscreen == False:
            root.attributes("-fullscreen", True)
            fullscreen = True
        else:
            root.attributes("-fullscreen", False)
            fullscreen = False



    #this short function is used for text to speech, it retrieves text based on the current level (explained later)
    #the speaking rate is set to 125 (default 200)
    #the runAndWait function is for the text to speech module to speak the text, it halts the program as it is speaking
    #*note, still trying to find a way to not halt the program while it speaks however there are reasons for this halt
    #functions as users spamming the button could crash the program or overlap the audio casuing other problems
    def text_to_speech(text):
        tts = pyttsx3.init()
        tts.setProperty('rate',125)
        tts.say(text)
        tts.runAndWait()



    #this function scales all objects on the current screen to fit the resolution picked by the user
    #the veriable event is assigned to the passed values
    def scaler(event):                                                                   
        global avg_multi, newx_multi, lvl_button_list, a45

        #setting up new values for the width and height of the program and averaging values using basic math
        new_width = event.width                                         #Gets information about window
        newx_multi = new_width/1920                                     #scales objects to the x-axis in relation to 1080p resolution
        new_height = event.height                                       #same for y-axis
        newy_multi = new_height/1080
        avg_multi = (newx_multi+newy_multi)/2

        #checks which screen the scaler needs to affect and applies the changes accordingly, the manual line by line method could've been
        #done in a shorter way using lists to hold all button data but at the cost of readability of code *note, future update could implement that
        image = copy_of_image.resize((new_width,new_height))            #resizes image
        photo = ImageTk.PhotoImage(image)
        background.config(image = photo)                                #configures/updates the background image
        background.image = photo

        x140 = int(140*newx_multi)
        x50 = int(50*newx_multi)
        y42 = int(42*newy_multi)
        a140 = int(140*avg_multi)
        a120 = int(120*avg_multi)
        a50 = int(50*avg_multi)
        a45 = int(45*avg_multi)

        if menu_screen_state == True:
            start_button.configure(font=("Comic Sans MS Bold",a50), width = x140, height = y42) 
            options_button.configure(font=("Comic Sans MS Bold",a50), width = x140, height = y42)
            exit_button.configure(font=("Comic Sans MS Bold",a50), width = x140, height = y42)
            title1.configure(font=("Comic Sans MS Bold",a140), width = x140, height = y42)
            title2.configure(font=("Comic Sans MS Bold",a140), width = x140, height = y42)
        
        if options_menu_state == True:
            apply_button.configure(font=("Comic Sans MS Bold",x50))
            fullscreen_checkbox.configure(font=("Comic Sans MS Bold",x50))
            translated_combo.configure(font=("Comic Sans MS Bold",x50))
        
        if level_selection_state == True:
            title3.configure(font=("Comic Sans MS Bold",a120))
            
        if level_menu_state == True:
            question.configure(font=("Comic Sans MS Bold",a45), wraplength = 855*newx_multi)
            answer3.configure(font=("Comic Sans MS Bold",a45), width = newx_multi*375, height = newy_multi*113)
            answer1.configure(font=("Comic Sans MS Bold",a45), width = newx_multi*375, height = newy_multi*113)
            answer2.configure(font=("Comic Sans MS Bold",a45), width = newx_multi*375, height = newy_multi*113)
            answer4.configure(font=("Comic Sans MS Bold",a45), width = newx_multi*375, height = newy_multi*113)

            #Try is required here since the explanation may not always exist
            #If it does fail, it does not break the code
            try:
                explanation.configure(font=("Comic Sans MS Bold",a45), wraplength = 1305*newx_multi)
            except: pass



    #This function changes the screen from the previous (sender) screen to the menu screen
    #*note, currently the only sender screen is the menu screen
    def options_menu():

        #Making local variables accessible
        global language_list, translated_combo, options_menu_state, background, copy_of_image, back_button
        global options_frame, back_button_options_menu, apply_button, fullscreen_checkbox, level_selection_state, menu_screen_state

        #resetting flags, lets the program know what is happening
        menu_screen_state = False
        options_menu_state = True
        level_selection_state = False

        #clears the previous gui
        start_menu_frame.destroy()
        background.destroy()
        icon_button.destroy()
        
        #sets the background image found in images directory in the parent folder
        image = Image.open(path.join(images_path, "options_menu.png"))                                        #opens the image file
        copy_of_image = image.copy()                                                         #creates a copy of the image file
        photo = ImageTk.PhotoImage(image)
        background = Label(root, image = photo)                                              #Assigns the image to the label
        background.bind("<Configure>", scaler)                                               #Configures the image to the screen
        background.pack(fill=BOTH, expand = YES) 

        #assigning the frame on the current menu, probably couldve used the same frame for all screens since its only used locally
        #but for better readability of code, it is seperate.
        options_frame = customtkinter.CTkFrame(root, border_width=5, corner_radius=30, bg_color="#F1EDE3", fg_color="light grey", border_color="grey", width=200, height=200)
        options_frame.place(relx = 0.35, rely= 0.55, anchor = W)

        #Setting up the checkbox for toggling fullscreen and applying the corect status of the checkbox
        #by using the flag veriable assigned before
        fullscreen_checkbox = customtkinter.CTkCheckBox(options_frame, text=text_file[5], command=switch_screen_toggle, hover_color="#D3D3D3",font=("Comic Sans MS Bold",30), text_color="#453735")
        fullscreen_checkbox.pack(padx=20, pady=20,fill=BOTH, expand = YES)
        if fullscreen == True:
            fullscreen_checkbox.select()

        #adding a combobox to the frame to select a language (default is english)
        translated_combo=ttk.Combobox(options_frame, values=language_list, font=("Comic Sans MS Bold",20), foreground="#453735", state= "readonly", width=11)
        translated_combo.set(language)
        translated_combo.pack(padx=20 ,fill=BOTH, expand = YES)
        
        #setting up a back button for the options menu, it has no text but rather is a png file
        back_button = Image.open(path.join(images_path, "back.png"))    
        back_button = back_button.resize((50,50))
        back_button_options_menu = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(back_button), command=menu_screen, text="", width=0, fg_color="#F1EDE3", corner_radius=0, hover=DISABLED)
        back_button_options_menu.place(relx=0.03, rely=0.95, anchor= CENTER)
        
        #adding an apply button to the options menu frame
        apply_button = customtkinter.CTkButton(options_frame,text=text_file[6], command= read_text, font=("Comic Sans MS Bold",30), text_color="#453735", corner_radius=60)
        apply_button.pack(padx=20, pady=20 ,fill=BOTH, expand = YES)



    #this function decides what to do after a choice is clicked (in the quiz)
    def next(choice):
        global correct_counter, incorrect_counter, J, explanation, lvl_list

        #the selected choice is correct, the program compares the user selection to
        #the correct choice (correct_answer is retrieved from the text_file, read the 
        #documentation of the read_text() function for more detail)

        if choice == correct_answer:

            #setting up the button to click to continue the quiz after getting a question right
            next_button = Image.open(path.join(images_path, "mext.png"))    
            next_button = next_button.resize((50,50))

            #this for loop checks if the current level is completed (using the flag veriable for levels)
            #L is defined as anything (it will be rewritten anyway)
            for i in range(0,20):
                if L == i+1:
                    lvl_list[i] = True

            #this veriable tells the program what level should be the next level
            next_level = L + 1
            
            #this is the button to allow the user to go to the next level, it is not enabled yet since this 
            #may occur at level 20 which doesnt make sense which is why theres an if statement next
            next_button = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(next_button),
            command=lambda:level_menu(next_level), text="", width=0, fg_color="#F1EDE3", corner_radius=0, hover=DISABLED, state=DISABLED)
            next_button.place(relx=0.97, rely=0.95, anchor= CENTER)

            #if the L (current level) is 20, it does not make sense for the next button to go to level 21 so the 
            #next_button is reconfigured making the user go to the stats menu and redirected to the main menu
            #the button is also enabled now     
            if L == 20:
                next_button.configure(command = stats_menu, state= NORMAL)
            

            #if the next level is already complete, it does not allow the user to repeat it (for better statistics)
            #when the next level is a level is already complete, it removes the next button and sends the user to
            #the level selection menu.
            for i in range(0,19):
                if next_level == i+2 and lvl_list[i+1] == True:
                    next_button.destroy()
                    level_selection()
                
            #if the next level is not already complete, it configures the button to be enabled. A try function is 
            #required in case the next_button got destroyed. There is a small (under 1 second) window of time 
            #where the user can press the next button before it gets destroyed where the program will run level
            #21 but that will never happen since this is not run if the current level is 20.
                else:
                    try:
                        next_button.configure(state=NORMAL)
                    except: pass
            
            #This is inside the if statment for when the user gets the corect answer, the correct_counter counts
            #the number of correct answers and then disables all the other buttons to not ruin the statistics
            correct_counter += 1
            answer1.configure(state= DISABLED)
            answer2.configure(state= DISABLED)
            answer3.configure(state= DISABLED)
            answer4.configure(state= DISABLED)


        #this is if the user does not click on the right answer
        else:
            #Question 8 has 2 right answers, so other right answer would've
            #been counted as wrong but not anymore
            if L == 8 and choice == 2:
                next(1)

            else:
                #places the explanation to the answer and counts the incorrect answer(s)
                if J != L:
                    explanation = customtkinter.CTkLabel(master = root, text=text_file[13+6*(L-1)], text_color="Black", fg_color= "#F1EDE3", font=("Comic Sans MS Bold",25), wraplength = 870)
                    explanation.place(relx = 0.5, rely = 0.85, anchor = CENTER)
                    J = L
                    incorrect_counter += 1

                    #adjusts the size of the lable depending on the screen size
                    explanation.configure(font=("Comic Sans MS Bold",a45), wraplength = 1305*newx_multi)
                    
                #disables the button the user has selected previously (so they dont click on the same wrong button twice)
                if choice == 1:
                    answer1.configure(state = DISABLED)
                if choice == 2:
                    answer2.configure(state = DISABLED)
                if choice == 3:
                    answer3.configure(state = DISABLED)
                if choice == 4:
                    answer4.configure(state = DISABLED)



    #this function is the menu for all the levels, depending on what lvl is sent to the function
    def level_menu(lvl):
        global background, level_selection_frame, copy_of_image, level_menu_state, level_selection_state, question, answer4, answer1, answer2, answer3, L, correct_answer, level_menu_frame

        #depending on the screen the level menu was requested from, the previous screen GUI
        #elements gets destoryed.
        if level_selection_state == True:
            background.destroy()
            level_selection_frame.destroy()

        if level_menu_state == True:
            background.destroy()
            level_menu_frame.destroy()

        #sets the flag veriables for the screen states
        level_selection_state = False
        level_menu_state = True

        #placeholder for the current level
        L = lvl

        image = Image.open(path.join(images_path, "level_menu.png"))                             #opens the image file
        copy_of_image = image.copy()                                          #creates a copy of the image file
        photo = ImageTk.PhotoImage(image)
        background = Label(root, image = photo)                               #Assigns the image to the label
        background.bind("<Configure>", scaler)                                #Configures the image to the screen
        background.pack(fill=BOTH, expand = YES)                              #packs the label onto the GUI

        #setting up the frame and places background onto the screen
        level_menu_frame = customtkinter.CTkFrame(master=root, border_width=5, corner_radius=30, bg_color="#F1EDE3", fg_color="light grey", border_color="grey")
        level_menu_frame.place(relx=0.5, rely = 0.55, anchor = CENTER)        #Frame in the level menu

        #retrieves the correct answer for this level
        correct_answer = int(answers_list[lvl-1])

        #setting up and placing the questions and multiple choice answers onto the GUI
        question = customtkinter.CTkLabel(master = root, text=text_file[8+6*(lvl-1)], font=("Comic Sans MS Bold",30), wraplength=855, text_color="black", fg_color= "white")
        question.place(relx = 0.5, rely = 0.185, anchor = CENTER)

        answer1 = customtkinter.CTkButton(master = level_menu_frame, text = text_file[9+6*(lvl-1)], text_color="white", fg_color= "grey", hover_color="blue", anchor=W, command= lambda:next(1))
        answer1.grid(padx = 20, pady = 20, row = 0, column = 0 )

        answer2 = customtkinter.CTkButton(master = level_menu_frame, text = text_file[10+6*(lvl-1)], text_color="white", fg_color= "grey", hover_color="blue", anchor=W, command= lambda:next(2))
        answer2.grid(padx = 20, pady = 20, row = 0, column = 1 )

        answer3 = customtkinter.CTkButton(master = level_menu_frame, text = text_file[11+6*(lvl-1)], text_color="white", fg_color= "grey", hover_color="blue", anchor=W, command= lambda:next(3))
        answer3.grid(padx = 20, pady = 20, row = 1, column = 0 )

        answer4 = customtkinter.CTkButton(master = level_menu_frame, text = text_file[12+6*(lvl-1)], text_color="white", fg_color= "grey", hover_color="blue", anchor=W, command= lambda:next(4))
        answer4.grid(padx = 20, pady = 20, row = 1, column = 1 )
    
        #setting up and placing the fullscreem toggle button
        icon = Image.open(path.join(images_path, "maximise_nav.png"))                            #Maximise/minimise icon
        icon = icon.resize((30,30))
        icon_button = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(icon), command=switch_screen_toggle, text="", width=0, fg_color="#F1EDE3", corner_radius=0, hover=DISABLED)
        icon_button.place(x=5, y=5) 

        #configures and places the icon that speaks the text on the screen
        speak = Image.open(path.join(images_path, "speak.png"))                               #speech to text icon
        speak = speak.resize((40,40))
        speak_button = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(speak),
        command=lambda:text_to_speech(text_file[8+6*(lvl-1)]), text="", width=0, fg_color="#F1EDE3", corner_radius=0, hover=DISABLED)
        speak_button.place(relx=0.5, rely=0.348, anchor = CENTER) 

        #configures and places the back button
        back_button = Image.open(path.join(images_path, "Back.png"))    
        back_button = back_button.resize((50,50))
        back_button_options_menu = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(back_button), command=level_selection, text="", width=0, fg_color="#F1EDE3", corner_radius=0, hover=DISABLED)
        back_button_options_menu.place(relx=0.03, rely=0.95, anchor= CENTER)





    #The menu that pops up at the end to display the statistics of the user
    def stats_menu():
            #Makes local variables accessible
            global incorrect_counter, correct_counter, L, lvl_list

            #Conffiguring the new window
            stats = customtkinter.CTkToplevel(master = root, takefocus = True)
            stats.geometry('500x200')
            stats.grab_set()
            stats.title(text_file[131])

            #configuring the text on the new window and packing them
            correct_text = text_file[132]+" "+str(correct_counter)
            incorrect_text = text_file[133]+" "+str(incorrect_counter)    
            correct = customtkinter.CTkLabel(master = stats, text = correct_text, font = (None, 25))
            incorrect = customtkinter.CTkLabel(master = stats, text = incorrect_text, font =  (None, 25))
            correct.pack()
            incorrect.pack()

            #calculated the accuracy of the user (from answered questions)
            #and results of the user (correct answers out of the whole quiz)
            #and packs them onto the window
            accuracy = text_file[134]+" "+str(float(correct_counter/(correct_counter + incorrect_counter))*100)+"%"
            accuracy_label = customtkinter.CTkLabel(master = stats, text = accuracy, font =  (None, 25))
            accuracy_label.pack()

            result = text_file[135]+" "+str(float(correct_counter/20)*100)+"%"
            result_label = customtkinter.CTkLabel(master = stats, text = result, font =  (None, 25))
            result_label.pack()

            #indicates to the user if they properly finished the quiz
            #(i.e not doing all the questions before level 20)
            if correct_counter != 20:
                final_msg = text_file[129]
            else:
                final_msg = text_file[128]
            final_msg_label = customtkinter.CTkLabel(master = stats, text = final_msg, font =  (None, 25))
            final_msg_label.pack()

            #resets the statistics allowing the user to play again
            incorrect_counter = 0
            correct_counter = 0

            #resets level flags allowing the user to play again
            for i in range(0,20,1):
                lvl_list[i] = False
            L = 0

            #send user back to the main screen
            menu_screen()



    #The function that switches the screen from the main menu to the question selection menu
    def level_selection():

        #Makes local variables accessible
        global background, start_menu_frame, copy_of_image, title3, level_selection_state, level_selection_frame, menu_screen_state, options_menu_state, back_button_options_menu
        global incorrect_counter, correct_counter, L, lvl_list, lvl_button_list
        
        #Alters flags to the coresponding GUI screen
        if menu_screen_state == True:
            background.destroy()
            start_menu_frame.destroy()

        if level_menu_state == True:
            background.destroy()

        #Configuring the background of the question selection menu
        image = Image.open(path.join(images_path, "level_selection.png"))                                   #opens the image file
        copy_of_image = image.copy()                                                     #creates a copy of the image file
        photo = ImageTk.PhotoImage(image)
        background = Label(root, image = photo)                                          #Assigns the image to the label
        background.bind("<Configure>", scaler)                                           #Configures the image to the screen
        background.pack(fill=BOTH, expand = YES)                                         #packs the label onto the GUI

        #Configures the frame within the GUI
        level_selection_frame = customtkinter.CTkFrame(master=root, border_width=5, corner_radius=30, bg_color="#F1EDE3", fg_color="light grey", border_color="grey")
        level_selection_frame.place(relx=0.5, rely = 0.6, anchor = CENTER)

        #Title of the screen
        title3 = customtkinter.CTkLabel(master = root, text = text_file[7], font=("Comic Sans MS Bold",120), text_color="#453735", fg_color="#F1EDE3")
        title3.place(relx = 0.5, rely = 0.12, anchor = CENTER)

        #Setting up navigational buttons (back button)
        back_button = Image.open(path.join(images_path, "Back.png"))    
        back_button = back_button.resize((50,50))
        back_button_options_menu = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(back_button), command=menu_screen, text="", width=0, fg_color="#F1EDE3", corner_radius=0, hover=DISABLED)
        back_button_options_menu.place(relx=0.03, rely=0.95, anchor= CENTER)

        #Configuring buttons coresponding to different questions and placing them on
        #a grid style pattern in the frame made earlier
        lvl1 = customtkinter.CTkButton(master = level_selection_frame, text="1", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(1))
        lvl2 = customtkinter.CTkButton(master = level_selection_frame, text="2", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(2))
        lvl3 = customtkinter.CTkButton(master = level_selection_frame, text="3", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(3))
        lvl4 = customtkinter.CTkButton(master = level_selection_frame, text="4", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(4))
        lvl5 = customtkinter.CTkButton(master = level_selection_frame, text="5", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(5))

        lvl1.grid(row = 0, column = 0, padx = 30, pady = 30)
        lvl2.grid(row = 0, column = 1, padx = 0, pady = 30)
        lvl3.grid(row = 0, column = 2, padx = 30, pady = 30)
        lvl4.grid(row = 0, column = 3, padx = 0, pady = 30)
        lvl5.grid(row = 0, column = 4, padx = 30, pady = 30)

        lvl6 = customtkinter.CTkButton(master = level_selection_frame, text="6", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(6))
        lvl7 = customtkinter.CTkButton(master = level_selection_frame, text="7", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(7))
        lvl8 = customtkinter.CTkButton(master = level_selection_frame, text="8", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(8))
        lvl9 = customtkinter.CTkButton(master = level_selection_frame, text="9", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(9))
        lvl10 = customtkinter.CTkButton(master = level_selection_frame, text= "10", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(10))

        lvl6.grid(row = 1, column = 0, padx = 30, pady = 22)
        lvl7.grid(row = 1, column = 1, padx = 0, pady = 22)
        lvl8.grid(row = 1, column = 2, padx = 30, pady = 22)
        lvl9.grid(row = 1, column = 3, padx = 0, pady = 22)
        lvl10.grid(row = 1, column = 4, padx = 30, pady = 22)

        lvl11 = customtkinter.CTkButton(master = level_selection_frame, text="11", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(11))
        lvl12 = customtkinter.CTkButton(master = level_selection_frame, text="12", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(12))
        lvl13 = customtkinter.CTkButton(master = level_selection_frame, text="13", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(13))
        lvl14 = customtkinter.CTkButton(master = level_selection_frame, text="14", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(14))
        lvl15 = customtkinter.CTkButton(master = level_selection_frame, text="15", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(15))

        lvl11.grid(row = 2, column = 0, padx = 30, pady = 22)
        lvl12.grid(row = 2, column = 1, padx = 0, pady = 22)
        lvl13.grid(row = 2, column = 2, padx = 30, pady = 22)
        lvl14.grid(row = 2, column = 3, padx = 0, pady = 22)
        lvl15.grid(row = 2, column = 4, padx = 30, pady = 22)

        lvl16 = customtkinter.CTkButton(master = level_selection_frame, text="16", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(16))
        lvl17 = customtkinter.CTkButton(master = level_selection_frame, text="17", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(17))
        lvl18 = customtkinter.CTkButton(master = level_selection_frame, text="18", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(18))
        lvl19 = customtkinter.CTkButton(master = level_selection_frame, text="19", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(19))
        lvl20 = customtkinter.CTkButton(master = level_selection_frame, text="20", font=("Comic Sans MS Bold",50), hover_color="blue", fg_color="grey", command= lambda:level_menu(20))

        lvl16.grid(row = 3, column = 0, padx = 30, pady = 30)
        lvl17.grid(row = 3, column = 1, padx = 0, pady = 30)
        lvl18.grid(row = 3, column = 2, padx = 30, pady = 30)
        lvl19.grid(row = 3, column = 3, padx = 0, pady = 30)
        lvl20.grid(row = 3, column = 4, padx = 30, pady = 30)

        #Creating the list containing 
        lvl_button_list = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, lvl7, lvl8, lvl9, lvl10, lvl11, lvl12, lvl13, lvl14, lvl15, lvl16, lvl17, lvl18, lvl19, lvl20]

        #Disabling buttons corresponding to the completed questions
        for i in range(0,20,1):
            if lvl_list[i] == True:
                lvl_button_list[i].configure(state= DISABLED)

        #Updating flag variables
        menu_screen_state = False
        options_menu_state = False
        level_selection_state = True

        #Configuring the back button
        icon = Image.open(path.join(images_path, "maximise_nav.png"))    
        icon = icon.resize((30,30))
        icon_button = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(icon), command=switch_screen_toggle, text="", width=0, fg_color="#F1EDE3", corner_radius=0, hover=DISABLED)
        icon_button.place(x=5, y=5)




    #Function to switch to the main menu screen
    def menu_screen():

        #Making local variables accessible
        global background, start_button, options_button, exit_button, start_menu_frame, copy_of_image, icon
        global icon_button, menu_screen_state, options_menu_state, title1, title2, level_selection_state, level_menu_state

        #Updating flag variables and destroying previous GUI elements
        if options_menu_state == True:
            background.destroy()
            options_frame.destroy()                

        if level_selection_state == True:
            background.destroy()
            back_button_options_menu.destroy()

        if level_menu_state == True:
            background.destroy()

        menu_screen_state = True
        options_menu_state = False
        level_selection_state = False
        level_menu_state= False

        #Configuring and setting the background of menu screen
        image = Image.open(path.join(images_path, "Learn_Arithmetic.png"))               #opens the image file
        copy_of_image = image.copy()                                 #creates a copy of the image file
        photo = ImageTk.PhotoImage(image)
        background = Label(root, image = photo)                      #Assigns the image to the label
        background.bind("<Configure>", scaler)                       #Configures the image to the screen
        background.pack(fill=BOTH, expand = YES)                     #packs the label onto the GUI

        #Configuring and placing a frame in the main menu
        start_menu_frame = customtkinter.CTkFrame(master=root, border_width=5, corner_radius=30, bg_color="white", fg_color="light grey", border_color="grey")
        start_menu_frame.place(relx=0.45, rely = 0.7, anchor = CENTER)

        #Configuring and placing the lable for the title in the main menu, it was originally
        #split to alter font size of the two words to make them same length but it looked bad
        title1 = customtkinter.CTkLabel(master = root, text = text_file[0], font=("Comic Sans MS Bold",140), text_color="#453735", fg_color="white")
        title2 = customtkinter.CTkLabel(master = root, text = text_file[1], font=("Comic Sans MS Bold",140), text_color="#453735", fg_color="white")
        title1.place(relx = 0.45, rely = 0.23, anchor = S)
        title2.place(relx = 0.45, rely = 0.27, anchor = N)

        #Configuring and placing the buttons in the main menu
        start_button = customtkinter.CTkButton(start_menu_frame, text = text_file[2], font=("Comic Sans MS Bold",50),
        text_color="#453735", fg_color="#BDBDBD", corner_radius=25, hover_color="#E3E3E3", command = level_selection)
        
        options_button = customtkinter.CTkButton(start_menu_frame, text = text_file[3], font=("Comic Sans MS Bold",50),
        text_color="#453735", fg_color="#BDBDBD", corner_radius=25, hover_color="#E3E3E3", command=options_menu)

        exit_button = customtkinter.CTkButton(start_menu_frame, text = text_file[4], font=("Comic Sans MS Bold",50),
        text_color="#453735", fg_color="#BDBDBD", corner_radius=25, hover_color="#E3E3E3", command= close_app)


        start_button.pack(padx=20, pady = 20,fill=BOTH, expand = YES)
        options_button.pack(padx=20,fill=BOTH, expand = YES)
        exit_button.pack(padx=20, pady = 20,fill=BOTH, expand = YES)

        #Maximise/minimise icon
        icon = Image.open(path.join(images_path, "maximise.png"))    
        icon = icon.resize((30,30))
        icon_button = customtkinter.CTkButton(root, image=ImageTk.PhotoImage(icon), command=switch_screen_toggle, text="", width=0, fg_color="#453735", corner_radius=0, hover=DISABLED)
        icon_button.place(x=5, y=5)


    def main():
        #this is the first function that runs when the program is started, function is the one above
          
        read_text()

        #Runs the menu screen first (first screen)
        menu_screen()                            

        #Tkinter required function to keep GUI running/updated
        root.mainloop()


except Exception as ex:
    with open ("err.txt", "w") as f:
        f.write(f"{type(ex).__name__}, {type(ex)}, {str(ex)}")

if __name__ == "__main__":
    main()