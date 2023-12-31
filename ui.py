import tkinter
from tkinter import *

BG_GRAY = "#ABB2B9"
BG_COLOR = "#c5f0e3"
TEXT_COLOR = "#000000"

# BG_GRAY = "#ABB2B9"
# BG_COLOR = "#1c172a"
# TEXT_COLOR = "#ffffff"


FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def send(event):
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#000000", font=("Verdana", 12 ))

        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        
        
base = Tk()
base.title("E-Commerce Chatbot")
base.resizable(width=FALSE, height=FALSE)
base.configure(width=800, height=800, bg=BG_COLOR)


#Create Chat window
ChatLog = Text(base, bd=0, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_BOLD)
ChatLog.config(state=DISABLED)

head_label = Label(base, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome to E-Commerce Chatbot", font=FONT_BOLD, pady=10)
head_label.place(relwidth=1)

line = Label(base, width=450, bg=BG_GRAY)


#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
ChatLog.focus()

#Create Button to send message
SendButton = Button(base, font=("Verdana", 12,'bold'), text="Send", width="12", height=15,
                    bd=0, bg="#ed9061", activebackground="#3c9d9b",fg='#ffffff',
                    command=lambda: send)

#Create the box to enter message
EntryBox = Text(base, bg="white",width="29", height="5", font="Arial", background="#dddddd")
EntryBox.focus()
EntryBox.bind("<Return>", send)
#EntryBox.bind("<Return>", send)

# bottom label
# bottom_label = Label(base, bg=BG_GRAY, height=80)
# bottom_label.place(relwidth=1, rely=0.825)
        
# message entry box
#EntryBox = Entry(bottom_label, fg=TEXT_COLOR, font=FONT)
# msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, |relx=0.011)
# msg_entry.focus()


#Place all components on the screen
# scrollbar.place(relheight=1, relx=0.974)
# ChatLog.place(relheight=1, width=1)
# EntryBox.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
# SendButton.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.20)\

scrollbar.place(x=775,y=6, height=800)
line.place(x=0,y=35, height=1, width=770)
ChatLog.place(x=5,y=40, height=700, width=770)
EntryBox.place(x=0, y=740, height=60, width=600)
SendButton.place(x=600, y=740, height=60, width=175)