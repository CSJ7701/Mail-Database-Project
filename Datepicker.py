from datetime import date, timedelta
from tkinter import StringVar, Event #, Spinbox
from tkcalendar import DateEntry

class DatePicker(CTkSpinbox):
    def __init__(self, master=None, initial: date = None, **kw):
        if initial is None:
            initial = date.today()
        self.date = initial
        self.string_var = StringVar(master, "1")
        super().__init__(master, variable=self.string_var, min_value=0, max_value=10000, **kw)

        self.string_var.set(initial.isoformat())
        self.configure(command=self._check_value_change)
        self.string_var.trace_add("write", self._on_string_var_change)
        self.bind('<Return>', self._on_enter_pressed)




