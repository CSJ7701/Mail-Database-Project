import customtkinter as ctk
import CTkListbox
from datetime import datetime
# from gui import NavGUI

class Reports(NavGUI):
    def __init__(self, main_frame, ParentGUI):

        self.parent=ParentGUI
        self.main_frame=main_frame
        
        self.options_frame=ctk.CTkFrame(self.main_frame, width=300, height=400, fg_color=("#d3d3d3", "#191919"))
        self.options_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.choose_report_frame=ctk.CTkFrame(self.options_frame)
        self.choose_report_frame.pack(side="top", padx=10, pady=10, ipady=10, fill="both")
        
        self.report_options_frame=ctk.CTkFrame(self.options_frame)
        self.report_options_frame.pack(side="top", padx=10, pady=(0,10), fill="both", expand=True)

        # Choose Report Frame

        reports=["None", "All Time", "Day of the Week", "Time of Day", "Company", "Class"]
        
        self.report_choice_label=ctk.CTkLabel(self.choose_report_frame, text="Visualise packages by:")
        self.report_choice_label.pack(side="top", padx=10, pady=(20,0))
        self.report_choice=ctk.CTkOptionMenu(self.choose_report_frame, values=reports)
        self.report_choice.pack(side="top", padx=10, pady=10)

        self.report_start_date_label=ctk.CTkLabel(self.choose_report_frame, text="Start Date")
        self.report_start_date_entry=ctk.CTkEntry(self.choose_report_frame, placeholder_text="YYYY-MM-DD")
        self.report_start_date_label.pack(side="top", padx=10, pady=(20,0))
        self.report_start_date_entry.pack(side="top", padx=10, pady=(5,0))
        self.report_end_date_label=ctk.CTkLabel(self.choose_report_frame, text="End Date")
        self.report_end_date_entry=ctk.CTkEntry(self.choose_report_frame, placeholder_text="YYYY-MM-DD")
        self.report_end_date_label.pack(side="top", padx=10, pady=(5,0))
        self.report_end_date_entry.pack(side="top", padx=10, pady=5)

        self.report_start_date_entry.bind("<FocusOut>", self.CheckDate)
        self.report_end_date_entry.bind("<FocusOut>", self.CheckDate)

        # Report Filter Frame

        filters=["None", "Cadet Class", "Cadet Company"]
        self.filter_choice_label=ctk.CTkLabel(self.report_options_frame, text="Filter report by:")
        self.filter_choice=ctk.CTkOptionMenu(self.report_options_frame, values=filters)
        self.filter_choice_label.pack(side="top", padx=10, pady=(10,0))
        self.filter_choice.pack(side="top", padx=10, pady=(10,0))

        companies=["Alfa", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel"]
        years=self.GetYears()

        self.exclude_label=ctk.CTkLabel(self.report_options_frame, text="Exclude:")
        self.exclude_company=CTkListbox.CTkListbox(self.report_options_frame, multiple_selection=True, text_color="#000")
        self.exclude_year=CTkListbox.CTkListbox(self.report_options_frame, multiple_selection=True, text_color="#000")
        self.exclude_label.pack(side="top", padx=10, pady=(30,0))
        self.exclude_company.pack(side="top", padx=10, pady=(10,0))
        self.exclude_year.pack(side="top", padx=10, pady=(10,0))

        for i in range(len(companies)):
            if i==len(companies)-1:
                ind="END"
            else:
                ind=i
            self.exclude_company.insert(ind, companies[i])

        for i in range(len(years)):
            if i==len(years)-1:
                ind="END"
            else:
                ind=i
            self.exclude_year.insert(ind, years[i])

        self.plot=ctk.CTkButton(self.report_options_frame, text="Plot")
        self.plot.pack(side="bottom",padx=10, pady=20)

        # Average number of packages per day
        # # Sort by company, class

        # Average number of packages by hour
        # # Sort by company, class

        # Average number of packages by company
        # # Sort by class

        # Average number of packages by class
        # # Sort by company

        # For all of these, can limit time range. 
   
        
    def CheckDate(self, event):
        start=self.report_start_date_entry.get()
        end=self.report_end_date_entry.get()

        if start:
            try:
                datetime.strptime(start, '%Y-%m-%d')
                if datetime.strptime(start, '%Y-%m-%d') > datetime.today():
                    self.show_error("Start date cannot be later than today's date")
                    return False
                return True
            except ValueError:
                self.show_error("Start date is incorrect.\nPlease format as 'YYYY-MM-DD'")
        if end:
            try:
                datetime.strptime(end, '%Y-%m-%d')
                return True
            except ValueError:
                self.show_error("End date is incorrect.\nPlease format as 'YYYY-MM-DD'")

    def GetYears(self):
        CurrentYear=int(datetime.today().strftime("%Y"))
        years=[]
        i=5
        while i>0:
            years.append(CurrentYear-i)
            i=i-1
        i=0
        while i<6:
            years.append(CurrentYear+i)
            i=i+1
        return years

        
