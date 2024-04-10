import customtkinter as ctk
from matplotlib import figure
import CTkListbox
from datetime import datetime, timedelta
from collections import Counter
import numpy
# from gui import NavGUI
from Screen import Screen
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
from matplotlib.figure import Figure
from matplotlib.dates import MonthLocator, WeekdayLocator, YearLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Reports(Screen):
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
        self.report_choice_label.pack(side="top", padx=10, pady=(10,0))
        self.report_choice=ctk.CTkOptionMenu(self.choose_report_frame, values=reports)
        self.report_choice.pack(side="top", padx=10, pady=10)

        self.report_start_date_label=ctk.CTkLabel(self.choose_report_frame, text="Received - Start Date")
        self.report_start_date_entry=ctk.CTkEntry(self.choose_report_frame, placeholder_text="YYYY-MM-DD")
        self.report_start_date_label.pack(side="top", padx=10, pady=(10,0))
        self.report_start_date_entry.pack(side="top", padx=10, pady=(5,0))
        self.report_end_date_label=ctk.CTkLabel(self.choose_report_frame, text="Received - End Date")
        self.report_end_date_entry=ctk.CTkEntry(self.choose_report_frame, placeholder_text="YYYY-MM-DD")
        self.report_end_date_label.pack(side="top", padx=10, pady=(5,0))
        self.report_end_date_entry.pack(side="top", padx=10, pady=5)

        self.report_ret_choice=ctk.CTkCheckBox(self.choose_report_frame, text="Filter by Pickup Date?")
        self.report_ret_choice.pack(side="top", padx=10, pady=(10,0))

        self.report_ret_start_date_label=ctk.CTkLabel(self.choose_report_frame, text="Picked Up - Start Date")
        self.report_ret_start_date=ctk.CTkEntry(self.choose_report_frame, placeholder_text="YYYY-MM-DD")
        self.report_ret_start_date_label.pack(side="top", padx=10, pady=(10,0))
        self.report_ret_start_date.pack(side="top", padx=10, pady=(5,0))
        self.report_ret_end_date_label=ctk.CTkLabel(self.choose_report_frame, text="Picked Up - End Date")
        self.report_ret_end_date=ctk.CTkEntry(self.choose_report_frame, placeholder_text="YYYY-MM-DD")
        self.report_ret_end_date_label.pack(side="top", padx=10, pady=(5,0))
        self.report_ret_end_date.pack(side="top", padx=10, pady=5)

        self.report_start_date_entry.bind("<FocusOut>", self.CheckDate)
        self.report_end_date_entry.bind("<FocusOut>", self.CheckDate)

        # Report Filter Frame
        companies=["Alfa", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel"]
        years=self.GetYears()

        self.exclude_label=ctk.CTkLabel(self.report_options_frame, text="Exclude Cadets:\nCompany and Grad Year")
        self.exclude_company=CTkListbox.CTkListbox(self.report_options_frame, multiple_selection=True, text_color="#000", height=120)
        self.exclude_year=CTkListbox.CTkListbox(self.report_options_frame, multiple_selection=True, text_color="#000", height=120)
        self.exclude_label.pack(side="top", padx=10, pady=(30,0))
        self.exclude_company.pack(side="top", padx=10, pady=(10,0), fill="y", expand=True)
        self.exclude_year.pack(side="top", padx=10, pady=(10,0), fill="y", expand=True)

        self.both_choice=ctk.CTkCheckBox(self.report_options_frame, text="Union?")
        self.both_choice.pack(side="top", padx=10, pady=10)

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

        self.plot=ctk.CTkButton(self.report_options_frame, text="Plot", command=self.Plot)
        self.plot.pack(side="bottom",padx=10, pady=(10,15))

        # Plot Frame

        self.plot_frame=ctk.CTkFrame(self.main_frame, width=600, height=400, fg_color=("#d3d3d3", "#191919"))
        self.plot_frame.pack(side="right", fill="both", expand=True)

    def CheckDate(self, event):
        start=self.report_start_date_entry.get()
        end=self.report_end_date_entry.get()
        ret_start=self.report_ret_start_date.get()
        ret_end=self.report_ret_end_date.get()

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
        if ret_start:
            try:
                datetime.strptime(ret_start, '%Y-%m-%d')
                if datetime.strptime(ret_start, '%Y-%m-%d') > datetime.today():
                    self.show_error("Start date cannot be later than today's date")
                    return False
                return True
            except ValueError:
                self.show_error("Start date is incorrect.\nPlease format as 'YYYY-MM-DD'")
        if ret_end:
            try:
                datetime.strptime(ret_end, '%Y-%m-%d')
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

    def GetExcludes(self) -> list[list[str]]:
        """Gets subsets of data to exclude from the 'exclude' lists. Returns the 'WHERE x IS NOT y' for SQL Query"""
        both=self.both_choice.get()
        if both == 1:
            union="AND"
        elif both == 0:
            union="OR"
        ex_company=self.exclude_company.get()
        ex_year=self.exclude_year.get()
        if not ex_year and not ex_company:
            return []
        query=f"SELECT name FROM cadets WHERE "
        if ex_company:
            companies=','.join(['?']*len(ex_company))
            query+=f"company IN ({companies})"
            query_sub=ex_company
        if ex_company and ex_year:
            query+=f" {union} "
        if ex_year:
            years=','.join(['?']*len(ex_year))
            query+=f"graduation_date IN ({years})"
            query_sub=ex_year
        if ex_company and ex_year:
            query_sub=ex_company+ex_year

        self.parent.database.cursor.execute(query, query_sub)
        results=self.parent.database.cursor.fetchall()
        return results

    def GetDateFilter(self) -> list[tuple[str, str]]:
        """Gets dates to filter results"""
        rec_start=self.report_start_date_entry.get()
        rec_end=self.report_end_date_entry.get()
        if not rec_start:
            self.parent.database.cursor.execute("SELECT MIN(date(received)) AS lowest_date FROM packages;")
            rec_start=str(self.parent.database.cursor.fetchone()[0])
        if not rec_end:
            self.parent.database.cursor.execute("SELECT MAX(date(received)) AS highest_date FROM packages;")
            rec_end=str(self.parent.database.cursor.fetchone()[0])

        ret_start=self.report_ret_start_date.get()
        ret_end=self.report_ret_end_date.get()
        if not ret_start:
            self.parent.database.cursor.execute("SELECT MIN(date(picked_up)) AS lowest_date FROM packages;")
            ret_start=str(self.parent.database.cursor.fetchone()[0])
        if not ret_end:
            self.parent.database.cursor.execute("SELECT MAX(date(picked_up)) AS highest_date FROM packages;")
            ret_end=str(self.parent.database.cursor.fetchone()[0])
        return [(rec_start, rec_end), (ret_start,ret_end)]
            

    def PlotAllTime(self):
        excluded_names=self.GetExcludes()
        date_range=self.GetDateFilter()
        if self.report_ret_choice.get()==1:
            if excluded_names:
                query=f"SELECT received FROM packages WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'"
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"SELECT received FROM packages WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'"
                self.parent.database.cursor.execute(query)
        else:
            if excluded_names:
                query=f"SELECT received FROM packages WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'"
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"SELECT received FROM packages WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'"
                self.parent.database.cursor.execute(query)            
        data=self.parent.database.cursor.fetchall()
        data=[datetime.strptime(date[0], '%Y-%m-%d') for date in data]
        date_range=max(data)-min(data)
        date_counts={}
        for date in data:
            date_counts[date] = date_counts.get(date, 0)+1

        if date_range < timedelta(days=7):
            date_freq='day'
        elif date_range < timedelta(weeks=4):
            date_freq='week'
        elif date_range < timedelta(days=365):
            date_freq='month'
        else:
            date_freq='year'
        
        x=list(date_counts.keys())
        y=list(date_counts.values())
        fig, ax=plt.subplots(figsize=(12,12))
        ax.plot(x,y,marker='o', color='blue', linestyle='-')
        ax.set_title('Packages Sorted by Delivery Date')
        ax.set_xlabel('Date')
        ax.grid(True)
        plt.xticks(rotation=90)

        if date_freq == 'day':
            ax.xaxis.set_major_locator(MaxNLocator(7))
            ax.xaxis.set_minor_locator(MaxNLocator(25))
            ax.xaxis.set_tick_params(rotation=45)
        elif date_freq == 'week':
            ax.xaxis.set_major_locator(MaxNLocator(4))
            ax.xaxis.set_minor_locator(MaxNLocator(25))
            ax.xaxis.set_tick_params(rotation=45)
        elif date_freq == 'month':
            ax.xaxis.set_major_locator(MonthLocator())
            ax.xaxis.set_minor_locator(WeekdayLocator())
            ax.xaxis.set_tick_params(rotation=45)
        elif date_freq =='year':
            ax.xaxis.set_major_locator(YearLocator())
            ax.xaxis.set_minor_locator(MonthLocator())
            ax.xaxis.set_tick_params(rotation=45)
        return fig 

    def PlotWeekDay(self):
        excluded_names=self.GetExcludes()
        date_range=self.GetDateFilter()
        if self.report_ret_choice.get()==1:
            if excluded_names:
                query=f"SELECT received, picked_up FROM packages WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'"
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"SELECT received, picked_up FROM packages WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'"
                self.parent.database.cursor.execute(query)
        else:
            if excluded_names:
                query=f"SELECT received, picked_up FROM packages WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'"
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"SELECT received, picked_up FROM packages WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'"
                self.parent.database.cursor.execute(query)
        data=self.parent.database.cursor.fetchall()
        weekdays=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        received_counter=Counter({day: 0 for day in weekdays})
        picked_counter=Counter({day: 0 for day in weekdays})
        for received_date, picked_date in data:
            received_date_obj=datetime.strptime(received_date, '%Y-%m-%d')
            received_weekday=weekdays[received_date_obj.weekday()]
            received_counter[received_weekday] += 1
            if picked_date is not None:
                picked_date_obj=datetime.strptime(picked_date, '%Y-%m-%d')
                picked_weekday=weekdays[picked_date_obj.weekday()]
                picked_counter[picked_weekday] += 1
 

        fig, ax=plt.subplots()
        bar_width=0.35
        index=numpy.arange(len(weekdays))
        ax.bar(index-bar_width/2, received_counter.values(), bar_width, label='Received', color='blue')
        ax.bar(index+bar_width/2, picked_counter.values(), bar_width, label='Picked Up', color='red')
        ax.set_xlabel('Weekday')
        ax.set_ylabel('Packages')
        ax.set_title('Packages Received and Picked Up by Weekday')
        ax.set_xticks(index)
        ax.set_xticklabels(weekdays)
        ax.xaxis.set_tick_params(rotation=45)
        ax.legend()
        return fig

    def PlotTime(self):
        excluded_names=self.GetExcludes()
        date_range=self.GetDateFilter()
        if self.report_ret_choice.get()==1:
            if excluded_names:
                query=f"SELECT picked_up_time FROM packages WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'"
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"SELECT picked_up_time FROM packages WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'"
                self.parent.database.cursor.execute(query)
        else:
            if excluded_names:
                query=f"SELECT picked_up_time FROM packages WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'"
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"SELECT picked_up_time FROM packages WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'"
                self.parent.database.cursor.execute(query)
        data=self.parent.database.cursor.fetchall()
        pickup_times=[]
        for row in data:
            pickup_time=row[0]
            if pickup_time:
                pickup_times.append(datetime.strptime(pickup_time, '%H:%M:%S'))
        hours=[time.hour + time.minute / 60 for time in pickup_times]
        fig, ax = plt.subplots()
        ax.hist(hours, bins=24, edgecolor='black', alpha=0.7)
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Packages')
        ax.set_title('Packages Picked Up by Hour')
        ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: '{:02d}:00'.format(int(val))))
        ax.xaxis.set_tick_params(rotation=45)
        return fig

    def PlotCompany(self):
        excluded_names=self.GetExcludes()
        date_range=self.GetDateFilter()
        if self.report_ret_choice.get()==1:
            if excluded_names:
                query=f"""SELECT cadets.company, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'
                       GROUP BY cadets.company"""
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"""SELECT cadets.company, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'
                       GROUP BY cadets.company"""
                self.parent.database.cursor.execute(query)
        else:
            if excluded_names:
                query=f"""SELECT cadets.company, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'
                       GROUP BY cadets.company"""
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"""SELECT cadets.company, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'
                       GROUP BY cadets.company"""
                self.parent.database.cursor.execute(query)
        data=self.parent.database.cursor.fetchall()
        companies=[row[0] for row in data]
        counts=[row[1] for row in data]
        fig, ax=plt.subplots()
        ax.bar(companies, counts)
        ax.set_xlabel("Company")
        ax.set_ylabel("Packages")
        ax.set_title("Packages Received by Cadet Company")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig

    def PlotGradYear(self):
        excluded_names=self.GetExcludes()
        date_range=self.GetDateFilter()
        if self.report_ret_choice.get()==1:
            if excluded_names:
                query=f"""SELECT cadets.graduation_date, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'
                       GROUP BY cadets.graduation_date
                       """
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"""SELECT cadets.graduation_date, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}' AND picked_up BETWEEN '{date_range[1][0]}' AND '{date_range[1][1]}'
                       GROUP BY cadets.graduation_date
                       """
                self.parent.database.cursor.execute(query)
        else:
            if excluded_names:
                query=f"""SELECT cadets.graduation_date, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE adressee NOT IN ({','.join(['?']*len(excluded_names))}) AND received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'
                       GROUP BY cadets.graduation_date
                       """
                excluded_names=[name[0] for name in excluded_names]
                self.parent.database.cursor.execute(query,excluded_names)
            else:
                query=f"""SELECT cadets.graduation_date, COUNT(packages.adressee) AS package_count
                       FROM packages
                       JOIN cadets ON packages.adressee=cadets.name
                       WHERE received BETWEEN '{date_range[0][0]}' AND '{date_range[0][1]}'
                       GROUP BY cadets.graduation_date
                       """
                self.parent.database.cursor.execute(query)
        data=self.parent.database.cursor.fetchall()
        grad_years=[int(row[0]) for row in data]
        counts=[row[1] for row in data]
        fig, ax=plt.subplots()
        ax.bar(grad_years, counts)
        ax.set_xlabel("Graduation Year")
        ax.set_ylabel("Packages")
        ax.set_title("Packages Received by Cadet Class")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout
        return fig
        

        

    def Plot(self):
        for child in self.plot_frame.winfo_children():
            child.destroy()
        report=self.report_choice.get()
        if report == "All Time":
            fig=self.PlotAllTime()
        if report == "Day of the Week":
            fig=self.PlotWeekDay()
        if report == "Time of Day":
            fig=self.PlotTime()
        if report == "Company":
            fig=self.PlotCompany()
        if report == "Class":
            fig=self.PlotGradYear()

        
        canvas=FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        
