from datetime import date, timedelta
from tkinter import StringVar, Event #Spinbox
import CTkSpinbox as Spinbox

_PLUS_ONE_DAY = timedelta(days=1)
_MINUS_ONE_DAY = timedelta(days=-1)


class DatePicker(Spinbox):
    def __init__(self, master=None, initial: date = None, **kw):
        if initial is None:
            initial = date.today()
        self.date = initial
        self.string_var = StringVar(master, "1")
        super().__init__(master, textvariable=self.string_var, from_=0, to=10000, **kw)

        self.string_var.set(initial.isoformat())
        self.config(command=self._check_value_change)
        self.string_var.trace_add("write", self._on_string_var_change)
        self.bind('<Return>', self._on_enter_pressed)

    def _on_enter_pressed(self, event: Event):
        self.string_var.set(self.date.isoformat())
        self.winfo_toplevel().focus_set()

    def _on_string_var_change(self, s0: str, s1: str, s2: str):
        try:
            year, month, day = self.string_var.get().split("-")
            self.date = date(int(year), int(month), int(day))
        except ValueError:
            return

    def _check_value_change(self):
        new_value = self.get()
        if new_value == str(self.date.year - 1):
            self.date += _MINUS_ONE_DAY
        elif new_value == str(self.date.year + 1):
            self.date += _PLUS_ONE_DAY

        self.string_var.set(self.date.isoformat())
