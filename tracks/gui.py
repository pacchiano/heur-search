from Tkinter import *

def onclick():
   pass

#root = Tk()
#text = Text(root)

class Display(Frame):

   def __init__(self, parent = 0 ):
      Frame.__init__(self, parent)
      self.entry = Entry(self)
      self.entry.pack()
      self.doIt = Button(self, text = "submit track", command = self.onEnter)
      self.doIt.pack()
      self.text = Text(self)
      self.text.pack()
      self.counter = 1
      self.after(2000, self.task)
      self.pack()

   def onEnter(self):
      self.task()

   def task(self):
      print str(self.counter)
      self.counter += 1
      #self.text.clear()
      self.text.delete(1.0, END)
      self.text.insert(INSERT, str(self.counter))
      self.text.pack()
      return self.after(2000, self.task)

if __name__ == '__main__':
   Display().mainloop()
