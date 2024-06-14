import os
import tkinter as tk
import tkinter.messagebox
from tkinter import ACTIVE, LEFT, RIGHT, Button, Frame, filedialog, ttk
from tkinter.simpledialog import Dialog

from .uebase import desktop

"""This module contains the gui elements used by uvs, the UnrealVersionSelector"""


def find_icon():
    # we need to find an icon for the handler
    paxoicon = os.path.abspath(os.path.join(os.path.dirname(__file__), "paxo.ico"))
    if not os.path.isfile(paxoicon):
        return None
    return paxoicon


class EngineSelector(Dialog):
    def __init__(self, engines, initial_id=None):
        title = "Select Unreal Engine Version"
        self.initial_id = initial_id
        self.filepicker_id = None
        self.result = None
        self.engines = engines
        self.descr = {
            k: desktop.get_engine_description(k, v) for k, v in engines.items()
        }
        self.ids = list(engines.keys())

        def compare_ids(a, b):
            if a == b:
                return 0
            if desktop.is_preferred_identifier(a, b):
                return -1
            return 1

        self.ids = desktop.sort_identifiers(self.ids)
        try:
            self.idx = self.ids.index(initial_id)
        except ValueError:
            self.idx = -1
        super().__init__(None, title)

    def body(self, master):
        self.minsize(450, 0)  # Set the minimum size of the dialog
        self.attributes("-topmost", True)  # Set the dialog to be on top
        # self.attributes("-toolwindow", True)  # Set the dialog to be a tool window (no minimize/maximize buttons
        self.iconbitmap(find_icon())
        # grow the master frame to fill the window
        master.pack(fill=tk.BOTH, expand=True)

        # Create a Frame for the body
        # body_frame = tk.Frame(master)
        # body_frame.pack(fill=tk.BOTH, expand=True)  # Set fill and expand options

        # Create a Combobox for the left side
        values = [self.descr[k] for k in self.ids]
        combobox = ttk.Combobox(master, values=values)
        if self.idx >= 0:
            combobox.current(self.idx)
        combobox.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True
        )  # Set fill and expand options
        self.combobox = combobox

        # Create a Button for the right side
        button = tk.Button(master, text=" ... ", command=self.filepicker)
        button.pack(side=tk.RIGHT)  # Set fill and expand options

    def buttonbox(self):
        """add standard button box.

        overriding to place buttons to the right
        """

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        # pack the box to the right
        box.pack(side=RIGHT)

    def filepicker(self):
        # find the first engine root which is not a x.x id
        for id in self.ids:
            if not desktop.is_stock_engine_release(id):
                start = self.engines[id]
                break
        else:
            start = None

        engine_root = filedialog.askdirectory(
            parent=self,
            initialdir=start,
            title="Select the Unreal Engine installation to use for this project",
        )
        if not engine_root:
            return
        if not desktop.is_valid_root_directory(engine_root):
            tkinter.messagebox.showerror(
                parent=self,
                title="Error",
                message=f"The selected directory is not a valid engine installation: {engine_root}",
            )
            return  # try again

        self.filepicker_id = desktop.get_engine_identifier_from_root_dir(engine_root)
        self.ok()

    def apply(self):
        if self.filepicker_id:
            self.result = self.filepicker_id
        else:
            idx = self.combobox.current()
            if idx >= 0:
                self.result = self.ids[idx]


class ProjectFilesWindow(desktop.FeedbackSink):
    def __init__(self):
        self.cancelled = False
        self.root = tk.Tk()
        self.root.title("Generate Project Files")
        self.root.iconbitmap(find_icon())
        self.root.attributes("-topmost", True)  # Set the dialog to be on top
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.upper_frame = tk.Frame(self.root)
        self.upper_frame.configure(width=400, height=50)
        self.upper_frame.pack(fill=tk.BOTH, expand=False)
        self.lower_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        self.lower_frame.pack(fill=tk.BOTH, expand=True)

        progressframe = tk.Frame(self.upper_frame)
        self.label = tk.Label(progressframe, text="Generating project files...")
        self.label.pack(expand=True, pady=10, anchor="w")

        self.progressbar = ttk.Progressbar(
            progressframe, orient="horizontal", length=300, mode="determinate"
        )
        self.progressbar.pack(pady=10)
        progressframe.pack(side="left", expand=False, padx=5)

        # add a button to show the log window
        self.show_log_button = tk.Button(
            self.upper_frame, text="Show Log", command=self.show_log
        )
        self.show_log_button.pack(side="right", padx=5)

        self.logwindow = tk.Text(self.lower_frame, height=10, wrap="word")
        self.logwindow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(self.lower_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.logwindow.config(yscrollcommand=scroll.set)
        scroll.config(command=self.logwindow.yview)
        self.lower_frame.pack_forget()

    def show_log(self):
        """Shows the log window"""
        if not self.lower_frame.winfo_ismapped():
            self.lower_frame.pack(fill=tk.BOTH, expand=True)
            self.show_log_button.config(text="Hide Log")
        else:
            self.lower_frame.pack_forget()
            self.show_log_button.config(text="Show Log")

    def add_log_line(self, line: str):
        """Adds a line to the text in the log window"""
        if not self.root:
            return
        self.logwindow.insert(tk.END, line + "\n")
        # scroll to the end
        self.logwindow.see(tk.END)

    def update_progress_bar(self, progress: float):
        """Updates the progress bar to the given value"""
        # progress is a flat in the range 0..1
        self.progressbar["value"] = progress * 100

    def update_progress_bar_title(self, title: str):
        """Updates the progress bar title"""
        self.label["text"] = title

    def on_close(self):
        self.cancel()

    def cancel(self):
        """Just signal that the operation should be cancelled"""
        self.cancelled = True
        self.root.quit()

    def close(self):
        self.root.destroy()

    # FeedbackSink methods
    def poll(self, delay: float = 0.0) -> str:
        """Polls the feedback sink for any new messages and runs the event loop"""
        # if window isn't destroyed, run the event loop
        if self.cancelled:
            return "cancel"
        if delay > 0.0:
            self.root.after(int(delay * 1000), self.root.quit)
            self.root.mainloop()
        else:
            self.root.update()
        if self.cancelled:
            return "cancel"
        return ""

    def log(self, message: str, level: str = "info") -> None:
        """Logs a message to the feedback sink"""
        self.add_log_line(message)

    def progress_message(self, message: str) -> None:
        self.update_progress_bar_title(message)

    def progress_value(self, progress: float) -> None:
        self.update_progress_bar(progress)

    @classmethod
    def test(cls):
        """Test the ProjectFilesWindow"""
        window = cls()

        line = "This is a test line"
        i = 0

        def update():
            nonlocal i
            window.add_log_line(f"{line} {i}")
            i += 1
            window.root.after(1000, update)

        window.root.after(100, update)
        window.root.mainloop()


if __name__ == "__main__":
    ProjectFilesWindow.test()
