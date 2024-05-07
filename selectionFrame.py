import tkinter as tk

class ListFrame(tk.Frame):
    def __init__(self, master, items=[], autonumbering=False):
        super().__init__(master)
        self.list = tk.Listbox(self)
        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.list.yview)
        self.list.config(yscrollcommand=self.scroll.set)
        self.autonumbering = autonumbering
        self.add_all(items)
        self.list.pack(side=tk.LEFT)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)

    def pop_selection(self):
        index = self.list.curselection()
        if index:
            value = self.list.get(index)
            self.list.delete(index)
            if(self.autonumbering):
                value = value[value.find('.')+1:]
                self.refresh_list()
            return value
    
    def remove_all(self):
        items=[]
        for index in range(self.list.index(tk.END)):
            value = self.list.get(0)
            self.list.delete(0)
            if(self.autonumbering):
                value = value[value.find('.')+1:]
            items.append(value)
        return items
    
    def add_all(self, items):
        end = self.list.index(tk.END)
        for item in items:
            if(self.autonumbering):
                item = str(end + 1) + '.' + item
            self.list.insert(tk.END, item)
            end += 1

    def refresh_list(self):
        if(self.autonumbering):            
            allItems = self.list.get(0, tk.END)
            newItems = []
            for i, item in enumerate(allItems):
                newItem = str(i+1) + '.' + item[2:]
                newItems.append(newItem)
            self.list.delete(0,tk.END)
            self.list.insert(0,*newItems) 

    def insert_item(self, item):
        if(self.autonumbering):            
            allItems = self.list.get(0, tk.END)
            item = str(len(allItems) + 1) + '.' + item

        self.list.insert(tk.END, item)

    def get_items(self):
        return self.list.get(0, tk.END)
    
class SelectionFrame(tk.LabelFrame):
    def __init__(self, master, items=[], **args):
        super().__init__(master, **args)

        self.frame_a = ListFrame(self, items)
        self.frame_b = ListFrame(self,autonumbering=True)
        self.btn_right = tk.Button(self, text='>', command=self.move_right)
        self.btn_left = tk.Button(self, text='<', command=self.move_left)
        self.btn_addall = tk.Button(self, text='Add All', command=self.add_all)
        self.btn_removeall = tk.Button(self, text='Remove All', command=self.remove_all)

        self.frame_a.pack(side=tk.LEFT, padx=10, pady=10)
        self.frame_b.pack(side=tk.RIGHT, padx=10, pady=10)
        self.btn_addall.pack(expand=True, ipadx=5)
        self.btn_right.pack(expand=True, ipadx=5)
        self.btn_left.pack(expand=True, ipadx=5)
        self.btn_removeall.pack(expand=True, ipadx=5)

    def move_right(self):
        self.move(self.frame_a, self.frame_b)

    def move_left(self):
        self.move(self.frame_b, self.frame_a)

    def add_all(self):
        items = self.frame_a.remove_all()
        self.frame_b.add_all(items)

    def add_lframe(self, items):
        items = self.frame_a.add_all(items=items)
    
    def add_rframe(self, items):
        items = self.frame_b.add_all(items=items)

    def get_rframe_items(self):
        return self.frame_b.get_items()

    def get_lframe_items(self):
        return self.frame_a.get_items()
    
    def clear_selection_frame(self):
        self.frame_a.remove_all()
        self.frame_b.remove_all()

    def remove_all(self):
        items = self.frame_b.remove_all()
        self.frame_a.add_all(items)

    def move(self, frame_from, frame_to):
        value = frame_from.pop_selection()
        if value:
            frame_to.insert_item(value)

