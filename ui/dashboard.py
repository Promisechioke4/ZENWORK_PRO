import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import ttkbootstrap as ttkb
import threading

class ZenWorkDashboard(ttkb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("ZenWork Pro Dashboard")
        self.geometry("900x650")
        self.resizable(False, False)

        self.work_duration = 25 * 60  # 25 minutes
        self.break_duration = 5 * 60  # 5 minutes
        self.time_left = self.work_duration
        self.timer_running = False
        self.on_break = False
        self.timer_thread = None

        self.work_sessions = 0
        self.break_sessions = 0
        self.habit_list = []

        self.create_layout()

    def create_layout(self):
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(container, bg="#eaeaea", width=150)
        self.sidebar.pack(side="left", fill="y")

        self.canvas = tk.Canvas(container, bg="white")
        self.scroll_frame = tk.Frame(self.canvas, bg="white")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.sections = {}
        self.create_sidebar()
        self.create_timer_section()
        self.create_habit_section()
        self.create_report_section()

    def create_sidebar(self):
        tk.Label(self.sidebar, text="ZENWORK PRO", font=("Helvetica", 12, "bold"), bg="#eaeaea").pack(pady=20)

        buttons = [("Timer", "timer"), ("Habits", "habits"), ("Reports", "reports"), ("Settings", "settings")]
        for text, tag in buttons:
            btn = ttk.Button(self.sidebar, text=text, style="secondary.TButton", command=lambda t=tag: self.scroll_to(t))
            btn.pack(fill="x", padx=10, pady=5)

        theme_btn = ttk.Button(self.sidebar, text="💡 Toggle", command=self.toggle_dark_mode)
        theme_btn.pack(side="bottom", pady=10)

    def scroll_to(self, tag):
        section = self.sections.get(tag)
        if section:
            self.canvas.yview_moveto(section.winfo_y() / self.scroll_frame.winfo_height())

    def create_timer_section(self):
        section = tk.Frame(self.scroll_frame, bg="white")
        section.pack(fill="x", pady=30)
        self.sections["timer"] = section

        tk.Label(section, text="⏱ TIMER", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
        self.timer_display = tk.Label(section, text="25:00", font=("Helvetica", 32), bg="white")
        self.timer_display.pack(pady=10)

        self.timer_label = tk.Label(section, text="Focus on development", font=("Helvetica", 12), bg="white")
        self.timer_label.pack()

        btn_frame = tk.Frame(section, bg="white")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Start", width=10, command=self.start_timer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Pause", width=10, command=self.pause_timer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Reset", width=10, command=self.reset_timer).pack(side="left", padx=5)

        self.progress = ttk.Progressbar(section, length=300)
        self.progress.pack(pady=10)

        self.session_label = tk.Label(section, text="Work: 0 • Break: 0", font=("Helvetica", 10), bg="white")
        self.session_label.pack()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.time_left = self.break_duration if self.on_break else self.work_duration
        self.update_timer_display()

    def run_timer(self):
        while self.timer_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.update_timer_display()
            self.progress["value"] = ((self.work_duration - self.time_left) / self.work_duration) * 100 if not self.on_break else ((self.break_duration - self.time_left) / self.break_duration) * 100
            self.after(1000)
            self.time_left -= 1
        if self.time_left <= 0:
            self.on_break = not self.on_break
            if self.on_break:
                self.break_sessions += 1
                self.time_left = self.break_duration
                self.timer_label.config(text="Take a break!")
            else:
                self.work_sessions += 1
                self.time_left = self.work_duration
                self.timer_label.config(text="Focus on development")
            self.session_label.config(text=f"Work: {self.work_sessions} • Break: {self.break_sessions}")
            self.reset_timer()

    def update_timer_display(self):
        mins, secs = divmod(self.time_left, 60)
        self.timer_display.config(text=f"{mins:02d}:{secs:02d}")

    def create_habit_section(self):
        section = tk.Frame(self.scroll_frame, bg="white")
        section.pack(fill="x", pady=30)
        self.sections["habits"] = section

        tk.Label(section, text="📋 HABITS", font=("Helvetica", 16, "bold"), bg="white").pack(pady=5)
        self.habit_frame = tk.Frame(section, bg="white")
        self.habit_frame.pack()

        self.new_habit_var = tk.StringVar()
        input_frame = tk.Frame(section, bg="white")
        input_frame.pack(pady=10)
        ttk.Entry(input_frame, textvariable=self.new_habit_var, width=25).pack(side="left", padx=5)
        ttk.Button(input_frame, text="Add", command=self.add_habit).pack(side="left")

    def add_habit(self):
        habit = self.new_habit_var.get().strip()
        if habit:
            self.habit_list.append({"name": habit, "completed": False})
            self.new_habit_var.set("")
            self.refresh_habit_list()

    def refresh_habit_list(self):
        for widget in self.habit_frame.winfo_children():
            widget.destroy()
        for habit in self.habit_list:
            var = tk.BooleanVar(value=habit["completed"])
            cb = ttk.Checkbutton(self.habit_frame, text=habit["name"], variable=var)
            cb.pack(anchor="w", padx=30)

    def create_report_section(self):
        section = tk.Frame(self.scroll_frame, bg="white")
        section.pack(fill="x", pady=30)
        self.sections["reports"] = section

        tk.Label(section, text="📊 REPORTS", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        stats_frame = tk.Frame(section, bg="white")
        stats_frame.pack(pady=5)

        tk.Label(stats_frame, text="20 mins\nWork Time", font=("Helvetica", 10), bg="white").grid(row=0, column=0, padx=20)
        tk.Label(stats_frame, text="80 %\nTasks Completed", font=("Helvetica", 10), bg="white").grid(row=0, column=1, padx=20)
        tk.Label(stats_frame, text="7 days\nStreak", font=("Helvetica", 10), bg="white").grid(row=0, column=2, padx=20)

        # Add dummy settings section for scroll nav
        dummy = tk.Label(self.scroll_frame, text="⚙️ Settings (coming soon)", font=("Helvetica", 12), bg="white")
        dummy.pack(pady=50)
        self.sections["settings"] = dummy

    def toggle_dark_mode(self):
        current = self.style.theme.name
        new_theme = "darkly" if current == "flatly" else "flatly"
        self.style.theme_use(new_theme)


if __name__ == '__main__':
    print("🧘‍♀️ Launching ZenWork Pro Dashboard...")
    app = ZenWorkDashboard()
    app.mainloop()
