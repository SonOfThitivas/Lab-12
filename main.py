from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        
        self.filetype = [("text files", ".txt"), ("all files", ".*")]
        self.word = IntVar()
        self.char = IntVar()
        self.file_size = StringVar(value="N/A")
        self.search = StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        frame_left = Frame(self)
        frame_right = Frame(self)
        # frame left
        btn_search = Button(frame_left, text="Search", font=("Arial",25), command=self.searching)
        btn_openfile = Button(frame_left, text="Open File", font=("Arial", 25), command=self.open_file)
        btn_savefile = Button(frame_left, text="Save File", font=("Arial", 25), command=self.save_file)
        btn_cleartext = Button(frame_left, text="Clear Text", font=("Arial", 25), command=self.clear_text)
        self.ent_search = Entry(frame_left, font=("Arial", 25), textvariable=self.search)
        frame_bleft = Frame(frame_left)
        wordLabel = Label(frame_bleft, text="Word:", font=("Arial",25))
        charLabel = Label(frame_bleft, text="Character:", font=("Arial", 25))
        fileSizeLabel = Label(frame_bleft, text="File Size:", font=("Arial", 25))
        
        # word
        wordLabel.grid(row=0, column=0, padx=10)
        Label(frame_bleft, textvariable=self.word, font=("Arial", 25)).grid(row=0,column=1,padx=10)
        Label(frame_bleft, text="words", font=("Arial", 25)).grid(row=0,column=2, padx=10)
        # char
        charLabel.grid(row=1,column=0 ,padx=10)
        Label(frame_bleft, textvariable=self.char, font=("Arial", 25)).grid(row=1,column=1,padx=10)
        Label(frame_bleft, text="characters", font=("Arial", 25)).grid(row=1,column=2, padx=10)
        # file size
        fileSizeLabel.grid(row=2,column=0,padx=10)
        Label(frame_bleft, textvariable=self.file_size, font=("Arial", 25)).grid(row=2,column=1,padx=10)
        Label(frame_bleft, text="bytes", font=("Arial", 25)).grid(row=2,column=2, padx=10)
        # frame right
        self.textArea = Text(frame_right, font=("Arial", 25))
        self.textArea.bind("<Key>", self.counter)
        self.bind_all("<Enter>", self.counter)
        
        Label(frame_left, text="Searh Text:", font=("Arial", 25)).pack()
        self.ent_search.pack(padx=10, pady=10)
        btn_search.pack()
        btn_openfile.pack(padx=10, pady=10)
        btn_savefile.pack(padx=10, pady=10)
        btn_cleartext.pack(padx=10, pady=10)
        frame_bleft.pack()
        
        self.textArea.pack(padx=10, pady=10, fill='y')
        
        frame_left.grid(row=0, column=0)
        frame_right.grid(row=0,column=1)
        
    def open_file(self):
        self.clear_text()
        file = filedialog.askopenfilename(parent=self,
                                          initialdir=os.getcwd(),
                                          title="Please select a file:",
                                          filetypes=self.filetype)
        rev = list(file[-1:-5:-1])
        rev.reverse()
        rev = "".join(rev)
        if rev != ".txt":
            messagebox.showerror("Error", "File is not .txt")
            print(file[-1:-5])
        else:
            print(file)
            with open(file, 'rt') as pick:
                content = pick.read()
                # text
                self.textArea.insert(INSERT, content)
                words = content.split()
                # words
                self.word.set(len(words))
                # chars
                countchar = 0
                for char in words:
                    countchar += len(char)
                self.char.set(countchar)
                
            with open(file, 'rt') as pick:
                b = pick.read()
                self.file_size.set(str(len(b)))
            
    def save_file(self):
        file = filedialog.asksaveasfilename(parent=self,
                                            initialdir=os.getcwd(),
                                            title="Please select a file name for saving:",
                                            filetypes= self.filetype)
        fromTextArea = self.textArea.get("1.0", END)
        with open(file, "wt") as pick:
            pick.write(fromTextArea)
    
    def clear_text(self):
        self.textArea.delete("1.0", END)
        self.file_size.set("N/A")
        
    def counter(self, event):
        text = self.textArea.get("1.0", END)
        text = text.split()
        # words 
        self.word.set(len(text))
        # chars
        countChar = 0
        for char in text:
            countChar += len(char)
        self.char.set(countChar)
        
    def searching(self):
        print("search called")
        # clear highlight
        self.textArea.tag_remove("search", "1.0", "end   ")
        
        index = "1.0"
        text = self.textArea.get("1.0", END)
        text = text.split()
        searchWord = self.ent_search.get()

        index = self.textArea.search(searchWord, index, nocase=True, stopindex="end")
        
        if self.search.get() == "":
            messagebox.showwarning("Searching", "Search term not found")
        else:
            # last index sum of current index and
            # length of text
            lastidx = '% s+% dc' % (index, len(searchWord))
            self.textArea.tag_add("search", index, lastidx)
            self.textArea.tag_config("search", background="yellow")
    
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()