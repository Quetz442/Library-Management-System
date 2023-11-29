from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('library.db')
cur = con.cursor()


class Main(object):
    def __init__(self, master):
        self.master = master

        def displayStatestics(evt):
            count_books = cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall()
            print(count_books)
            self.lbl_book_count.config(text='Total :'+str(count_books[0][0])+' books in library')
            self.lbl_member_count.config(text='Total members : '+str(count_members[0][0]))
            self.lbl_taken_count.config(text='Total books :'+str(taken_books[0][0]))
            displaybooks(self)

        def displaybooks(self):
            books = cur.execute("SELECT * FROM books").fetchall()

            self.list_books.delete(0, END)
            count = 0
            for i in books:
                print(i)
                self.list_books.insert(count, str(i[0]) + '] ' + i[1])
                count += 1

            def bookInfo(evt):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('] ')[0]
                book = cur.execute("SELECT * FROM books WHERE book_id=?",(id,))
                book_info = book.fetchall()
                print(book_info)
                self.list_details.delete(0,'end')
                self.list_details.insert(0, "Book Name :" + book_info[0][1])
                self.list_details.insert(1, "Author :" + book_info[0][2])
                self.list_details.insert(2, "Language :" + book_info[0][3])
                if book_info[0][4] == 0:
                    self.list_details.insert(3, "Status : Available")
                else:
                    self.list_details.insert(3, "Status : Not Available")

            def doubleClick(evt):
                global given_id
                value = str(self.list_books.get(self.list_books.curselection()))
                given_id = value.split('] ')[0]
                give_book = GiveBook()

            self.list_books.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatestics)
            self.list_books.bind('<Double-Button-1>', doubleClick)



        # frame
        mainFrame = Frame(self.master)
        mainFrame.pack()
        topFrame = Frame(mainFrame, width=1350, height=70, bg="#f8f8f8",padx=20, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP,fill=X)
        centerFrame = Frame(mainFrame,width=1350, relief=RIDGE, bg="#e0f0f0", height=680)
        centerFrame.pack(side=TOP)
        centerLeftFrame = Frame(centerFrame, width=900, height=700, bg="#e0f0f0", borderwidth=2, relief='sunken')
        centerLeftFrame.pack(side=LEFT)
        centerRightFrame = Frame(centerFrame, width=450, height=700, bg="#e0f0f0", borderwidth=2, relief='sunken')
        centerRightFrame.pack()

    # _____________________________________________________________________________________________________________________________

        search_box = LabelFrame(centerRightFrame, width=440, height=75, text='Search Box', bg="#9bc9ff")
        search_box.pack(fill=BOTH)
        self.lbl_search = Label(search_box, text='Search :', font='arial 12 bold', bg="#9bc9ff", fg='white')
        self.lbl_search.grid(row=0, column=0, padx=20, pady=10)
        self.ent_search = Entry(search_box, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        self.btn_search = Button(search_box, text='Search', font='arial 12 ', bg="#fcc324", fg='white', command=self.searchBooks)
        self.btn_search.grid(row=0, column=4, pady=10, padx=20)

        list_bar = LabelFrame(centerRightFrame, width=440, height=175, text='List Bar', bg="#fcc324")
        list_bar.pack(fill=BOTH)
        lbl_list = Label(list_bar, text='Sort by :', font='times 16 bold', fg='#2488ff', bg='#fcc324')
        lbl_list.grid(row=0, column=2)
        self.listChoice = IntVar()
        rb1 = Radiobutton(list_bar, text='All Books', variable=self.listChoice, value=1, bg='#fcc324')
        rb2 = Radiobutton(list_bar, text='In Library', variable=self.listChoice, value=2, bg='#fcc324')
        rb3 = Radiobutton(list_bar, text='Borrowed Books', variable=self.listChoice, value=3, bg='#fcc324')
        rb1.grid(row=1, column=0)
        rb2.grid(row=1, column=1)
        rb3.grid(row=1, column=2)
        btn_list = Button(list_bar, text='List Books', bg='#2488ff', fg='white', font='arial 12', command=self.listBooks)
        btn_list.grid(row=1, column=3, padx=40, pady=10)

        image_bar = Frame(centerRightFrame,width=400, height=350)
        image_bar.pack(fill=BOTH)
        self.title_right = Label(image_bar, text='Welcome to our Library', font='arial 16 bold')
        self.title_right.grid(row=0)
        self.img_library = PhotoImage(file='icon/library.png')
        self.lblimg = Label(image_bar, image=self.img_library)
        self.lblimg.grid(row=1)
    # __________________________________________________________________________________________________________________________________

        self.iconbook = PhotoImage(file='icon/add_book.png')
        self.btnbook = Button(topFrame, text='Add Book', image=self.iconbook, compound=LEFT, font='arial 12 bold', command=self.addBook)
        self.btnbook.pack(side=LEFT)

        self.iconmember = PhotoImage(file='icon/user_add.png')
        self.btnmember = Button(topFrame, text="Add Member", font='arial 12 bold', padx=10, command=self.addMember)
        self.btnmember.configure(image=self.iconmember, compound=LEFT)
        self.btnmember.pack(side=LEFT)

        self.icongive = PhotoImage(file='icon/give_book.png')
        self.btngive = Button(topFrame, text='Give Book', font='arial 12 bold', padx=10, image=self.icongive, compound=LEFT, command=self.giveBook)
        self.btngive.pack(side=LEFT)

# ------------------------------------------------------------------------------------------------------------------------------------
        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=660)
        self.tabs.pack()
        self.tab1_icon = PhotoImage(file='icon/books.png')
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2_icon = PhotoImage(file='icon/statestics.png')
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='Library Management', image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='Statistics', image=self.tab2_icon, compound=LEFT)


        # lists book
        self.list_books = Listbox(self.tab1, width=40, height=30, bd=5, font='times 12 bold')
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.list_books.grid(row=0, column=0, pady=10, padx=(10, 0), sticky=N)
        self.sb.config(command=self.list_books.yview())
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0 , sticky=N+S+E)

        self.list_details = Listbox(self.tab1, width=80, height=30, bd=5, font='times 12 bold')
        self.list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)



        self.lbl_book_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.lbl_book_count.grid(row=0)
        self.lbl_member_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.lbl_member_count.grid(row=1, sticky=W)
        self.lbl_taken_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.lbl_taken_count.grid(row=2, sticky=W)

        displaybooks(self)
        displayStatestics(self)

    def addBook(self):
        add = AddBook()

    def addMember(self):
        member = AddMember()

    def searchBooks(self):
        value = self.ent_search.get()
        search = cur.execute("SELECT * FROM books WHERE book_name LIKE ?", ('%'+value+'%',)).fetchall()
        print(search)
        self.list_books.delete(0, END)
        count = 0
        for book in search:
            self.list_books.insert(count, str(book[0])+'] '+book[1])
            count += 1

    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks = cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in allbooks:
                self.list_books.insert(count, str(book[0])+'] '+ book[1])
                count += 1
        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM books WHERE book_status=?", (0,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in books_in_library:
                self.list_books.insert(count, str(book[0]) + '] ' + book[1])
                count += 1
        else:
            taken_books = cur.execute("SELECT * FROM books WHERE book_status=?", (1,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + '] ' + book[1])
                count += 1

    def giveBook(self):
        give_book = GiveBook()


class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Book")
        self.resizable(False, False)

        # ----------------------------Frames-------------------------------------

        # top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg= "#fcc324")
        self.bottomFrame.pack(fill=X)

        # ------------------------------heading ,image---------------------------
        self.top_image = PhotoImage(file='icon/add_book2.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='   Add book', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # --------------------------------Entries and Labels----------------------
        self.lbl_name = Label(self.bottomFrame, text='Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_name.insert(0, 'Please enter a book name')
        self.ent_name.place(x=150, y=45)

        self.lbl_author = Label(self.bottomFrame, text='Author :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_author.place(x=40, y=80)
        self.ent_author = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_author.insert(0, 'Please enter a author name')
        self.ent_author.place(x=150, y=85)

        self.lbl_language = Label(self.bottomFrame, text='Language :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_language.place(x=40, y=120)
        self.ent_language = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_language.insert(0, 'Please enter a language')
        self.ent_language.place(x=150, y=125)

        button = Button(self.bottomFrame, text='Add Book', command=self.addBook)
        button.place(x=270, y=200)

    def addBook(self):
        name = self.ent_name.get()
        author = self.ent_author.get()
        language = self.ent_language.get()

        if name and author and language != "":
            try:
                query = "INSERT INTO 'books' (book_name,book_author,book_language) VALUES(?,?,?)"
                cur.execute(query, (name, author, language))
                con.commit()
                messagebox.showinfo('Success', 'Successfully added to database', icon='info')
            except:
                messagebox.showerror("Error", "Can't add to database", icon='warning')
        else:
            messagebox.showerror("Error", "Fields can't be empty", icon='warning')


class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Member")
        self.resizable(False, False)

        # ----------------------------Frames-------------------------------------

        # top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg= "#fcc324")
        self.bottomFrame.pack(fill=X)

        # ------------------------------heading ,image---------------------------
        self.top_image = PhotoImage(file='icon/addmember.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='   Add Member', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # --------------------------------Entries and Labels----------------------
        self.lbl_name = Label(self.bottomFrame, text='Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_name.insert(0, 'Please enter a member name')
        self.ent_name.place(x=150, y=45)

        self.lbl_phone = Label(self.bottomFrame, text='Phone :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, 'Please enter phone number')
        self.ent_phone.place(x=150, y=85)


        button = Button(self.bottomFrame, text='Add Member', command=self.addMember)
        button.place(x=270, y=200)

    def addMember(self):
        name = self.ent_name.get()
        phone = self.ent_phone.get()

        if name and phone != "":
            try:
                query = "INSERT INTO 'members' (member_name,member_phone) VALUES(?,?)"
                cur.execute(query, (name, phone))
                con.commit()
                messagebox.showinfo('Success', 'Successfully added to database', icon='info')
            except:
                messagebox.showerror("Error", "Can't add to database", icon='warning')
        else:
            messagebox.showerror("Error", "Fields can't be empty", icon='warning')


class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False, False)

        query = "SELECT * FROM books WHERE book_status=0"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0]) + "-" + book[1])

        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + "-" + member[1])
        #####################Frames######################

        # Top Frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)
        # Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)
        # heading, image
        self.top_image = PhotoImage(file='icon/addmember.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text=' Lend a Book ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        ############################Etries and Labels###############################################3

        # member name
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text='Book: ', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name['values'] = book_list
        self.combo_name.place(x=150, y=45)

        # phone
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text='Member: ', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member['values'] = member_list
        self.combo_member.place(x=150, y=85)

        # Button
        button = Button(self.bottomFrame, text='Lend Book', command=self.lendBook)
        button.place(x=220, y=120)

    def lendBook(self):
        book_name = self.book_name.get()
        self.book_id=book_name.split('-')[0]
        member_name = self.member_name.get()

        if (book_name and member_name != ""):
            try:
                query = "INSERT INTO 'borrows'(bbook_id,bmember_id) VALUES(?,?)"
                cur.execute(query, (book_name, member_name))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database!", icon='info')
                cur.execute("UPDATE books SET book_status =? WHERE book_id=?", (1, self.book_id))
                con.commit()
            except:
                messagebox.showerror("Error", "Cant add to database", icons='warning')

        else:
            messagebox.showerror("Error", "Fields cant be empty", icons='warning')


def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1350x750+350+200")
    # root.iconbitmap(icon/icon.ico)
    root.mainloop()


if __name__ == '__main__':
    main()
