import tkinter as tk
import matplotlib.pyplot as plt
import re
import io
from PIL import Image
from email.mime.image import MIMEImage
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar
from datetime import datetime, timedelta

from GUI.generate_stocks_graph.bloc import GenerateStocksGraphBloc, GenerateStocksGraphError


def get_screen_size(root):
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width, height


def clear_root(root):
    for ele in root.winfo_children():
        ele.destroy()


class ChooseFromToDates:
    def __init__(self):

        self.fig = None
        self.bloc = GenerateStocksGraphBloc()
        self.bloc.add_listener(lambda state: self.update_gui(state))
        self.root = tk.Tk()
        self.to_date_calendar = None
        self.from_date_calendar = None
        self.stock_entry = None
        self.stock_list = None
        self.email_entry = None
        self.create_root_window()
        self.add_header()
        self.create_calendars()
        self.create_next_button()
        self.root.mainloop()

    def update_gui(self, state):
        if self.stock_list is not None:
            self.stock_list.delete(0, tk.END)
            for ticker in state.stocks_list:
                self.stock_list.insert("end", ticker)

    def create_root_window(self):
        self.root.title("View Stock Graph")

        width, height = get_screen_size(self.root)
        half_width, half_height = int(width * (3 / 4)), int(height * (3 / 4))
        x_offset = (width - half_width) // 2
        y_offset = (height - half_height) // 2
        self.root.geometry(f"{half_width}x{half_height}+{x_offset}+{y_offset}")

    def add_header(self):
        choose_stocks_header = tk.Label(self.root, text="Choose Dates", font=("Arial", 16))
        choose_stocks_header.pack(pady=10)

    def create_calendars(self):
        # Create a frame to hold the calendars
        calendar_frame = tk.Frame(self.root)
        calendar_frame.pack(pady=10)

        # Calculate the default date for the first calendar (5 days before the current date)
        default_date_from = datetime.now() - timedelta(days=5)

        # Calculate the default date for the second calendar (current date)
        default_date_to = datetime.now()

        # Add "From Date" label and Calendar
        from_label = tk.Label(calendar_frame, text="From Date:", font=("Arial", 14))  # Set font size to 14
        from_label.grid(row=0, column=0, padx=10, pady=10)

        self.from_date_calendar = Calendar(calendar_frame, selectmode='day',
                                           year=default_date_from.year, month=default_date_from.month,
                                           day=default_date_from.day)
        self.from_date_calendar.grid(row=1, column=0, padx=50, pady=10)

        # Add "To Date" label and Calendar
        to_label = tk.Label(calendar_frame, text="To Date:", font=("Arial", 14))  # Set font size to 14
        to_label.grid(row=0, column=1, padx=10, pady=10)

        self.to_date_calendar = Calendar(calendar_frame, selectmode='day',
                                         year=default_date_to.year, month=default_date_to.month,
                                         day=default_date_to.day)
        self.to_date_calendar.grid(row=1, column=1, padx=10, pady=10)

    def create_next_button(self):
        next_button = tk.Button(self.root, text="Next", font=("Arial", 14),
                                command=self.on_next_button_click)
        next_button.pack(pady=10)

    def on_next_button_click(self):
        from_date = datetime.strptime(self.from_date_calendar.get_date(), "%m/%d/%y").date()
        to_date = datetime.strptime(self.to_date_calendar.get_date(), "%m/%d/%y").date()
        res = self.bloc.choose_from_to_dates(from_date, to_date)
        if isinstance(res, GenerateStocksGraphError):
            messagebox.showerror("showerror", res.err_str)
            return
        clear_root(self.root)
        self.create_choose_stocks_header()
        self.create_stock_entry_frame()

    def create_choose_stocks_header(self):
        # Add header "Choose Stocks"
        choose_stocks_header = tk.Label(self.root, text="Choose Stocks", font=("Arial", 16))
        choose_stocks_header.pack(pady=10)

    def create_stock_entry_frame(self):
        # Create a frame for the stock entry
        stock_entry_frame = tk.Frame(self.root)
        stock_entry_frame.pack(pady=20)

        # Add a one-line entry for the stock name
        self.stock_entry = tk.Entry(stock_entry_frame, font=("Arial", 14))
        self.stock_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create a list to store the stock names
        self.stock_list = tk.Listbox(stock_entry_frame, font=("Arial", 14), )
        self.stock_list.grid(row=1, column=0, padx=10, pady=10)

        # Add the "Add" button with the correct command
        add_button = tk.Button(stock_entry_frame, text="Add", font=("Arial", 12), command=self.add_to_stocks_list)
        add_button.grid(row=2, column=0, padx=10, pady=10)

        # Add the "Clear List" button with the correct command
        clear_list_button = tk.Button(stock_entry_frame, text="Clear List", font=("Arial", 12),
                                      command=self.clear_stocks_list)
        clear_list_button.grid(row=3, column=0, padx=10, pady=10)

        # Add the "Generate Graph" button with the correct command
        generate_graph_button = tk.Button(stock_entry_frame, text="Generate Graph", font=("Arial", 12),
                                          command=lambda: self.generate_graph(self.stock_list))
        generate_graph_button.grid(row=4, column=0, padx=10, pady=10)

    def add_to_stocks_list(self):
        res = self.bloc.add_to_stocks_list(self.stock_entry.get())
        if isinstance(res, GenerateStocksGraphError):
            messagebox.showerror("showerror", res.err_str)
            return
        self.stock_entry.delete(0, tk.END)

    def generate_graph(self, stock_list):
        self.stock_list = None
        self.bloc.generate_graph_data()

        clear_root(self.root)

        self.fig, ax = plt.subplots()
        ax.plot(self.bloc.state.x_data, self.bloc.state.y_data)
        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Graph')

        # Calculate the desired height for the graph (one-third of the window's height)
        window_height = self.root.winfo_height()
        graph_height = window_height * (2 / 3)

        # Embed the plot in a tkinter window
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(height=graph_height)
        canvas_widget.pack(pady=20)

        # Create a label and entry field for the email address
        email_label = tk.Label(self.root, text="Mail:", font=("Arial", 12))
        email_label.pack()
        self.email_entry = tk.Entry(self.root, font=("Arial", 12))
        self.email_entry.pack(pady=20)

        # Create a "Send Mail" button
        send_mail_button = tk.Button(self.root, text="Send Mail", font=("Arial", 12), command=lambda: self.send_mail())
        send_mail_button.pack(pady=20)

    def clear_stocks_list(self):
        self.bloc.clear_stocks_list()

    def send_mail(self):
        # Save the figure to a BytesIO object
        self.fig.savefig('fig.png')
        email = self.email_entry.get()
        if re.search(r'[\w.]+\@[\w.]+', email):
            self.bloc.send_email(email, 'fig.png')

        else:
            messagebox.showerror("showerror", 'invalid email')
