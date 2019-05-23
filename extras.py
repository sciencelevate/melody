filelabel = Label(root, text="Lets play some music!")
filelabel.pack(pady=10)

filelabel['text'] = "Playing" + "  " + os.path.basename(filename)