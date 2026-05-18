
import tkinter as tk
from tkinter import ttk, messagebox
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_FAMILY, FONT_SIZE
from src.note_core import NoteCore

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Note Taker")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        self.note_core = NoteCore()
        
        self._create_widgets()
        self._load_notes_list()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        notes_label = ttk.Label(left_frame, text="Notes List", font=(FONT_FAMILY, FONT_SIZE, "bold"))
        notes_label.pack(pady=(0, 5))
        
        self.notes_listbox = tk.Listbox(left_frame, width=30, font=(FONT_FAMILY, FONT_SIZE))
        self.notes_listbox.pack(fill=tk.Y, expand=True)
        self.notes_listbox.bind("<<ListboxSelect>>", self._on_note_select)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(right_frame, text="Title", font=(FONT_FAMILY, FONT_SIZE, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.title_entry = ttk.Entry(right_frame, font=(FONT_FAMILY, FONT_SIZE))
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        
        content_label = ttk.Label(right_frame, text="Content", font=(FONT_FAMILY, FONT_SIZE, "bold"))
        content_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.content_text = tk.Text(right_frame, font=(FONT_FAMILY, FONT_SIZE))
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X)
        
        new_button = ttk.Button(button_frame, text="New Note", command=self._new_note)
        new_button.pack(side=tk.LEFT, padx=(0, 5))
        
        save_button = ttk.Button(button_frame, text="Save Note", command=self._save_note)
        save_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(button_frame, text="Delete Note", command=self._delete_note)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear", command=self._clear_fields)
        clear_button.pack(side=tk.LEFT, padx=5)

    def _load_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        notes = self.note_core.get_all_notes()
        for note in notes:
            self.notes_listbox.insert(tk.END, f"{note[0]} - {note[1]}")

    def _on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            note_id = int(self.notes_listbox.get(index).split(" - ")[0])
            note = self.note_core.load_note(note_id)
            if note:
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, note[1])
                self.content_text.delete(1.0, tk.END)
                self.content_text.insert(1.0, note[2])

    def _new_note(self):
        self.note_core.create_new_note()
        self._clear_fields()

    def _save_note(self):
        title = self.title_entry.get()
        content = self.content_text.get(1.0, tk.END)
        try:
            self.note_core.save_note(title, content)
            messagebox.showinfo("Success", "Note saved successfully!")
            self._load_notes_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _delete_note(self):
        if self.note_core.current_note_id:
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this note?")
            if confirm:
                self.note_core.delete_note(self.note_core.current_note_id)
                messagebox.showinfo("Success", "Note deleted successfully!")
                self._clear_fields()
                self._load_notes_list()
        else:
            messagebox.showwarning("Warning", "No note selected to delete!")

    def _clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.note_core.create_new_note()
