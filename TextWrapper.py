from tkinter import Text, END

class TextWrapper:
    txt_fld: Text
    def __init__(self, txt_fld: Text):
        self.txt_fld=txt_fld
        
    def write(self, text:str):
        self.txt_fld.insert(END,text) 
        self.delete()
        self.txt_fld.yview_scroll(number=1,what="units")
        
    def flush(self):
        self.txt_fld.update()
        
    def delete(self):
        text=self.txt_fld.get("1.0","end")
        if len(text)>20000:
            self.txt_fld.delete("1.0","2.0")