import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json

class AddressBookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Address Book Pro")
        self.geometry("600x400")  # Adjust the size of the main window

        self.address_book = {}
        self.load_address_book()

        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label_main_menu = ttk.Label(self.main_frame, text="Address Book Pro", font=("Arial", 16))
        self.label_main_menu.pack(pady=20)

        self.button_insert = ttk.Button(self.main_frame, text="Insert Entry", command=self.open_insert_page)
        self.button_insert.pack()

        self.button_display = ttk.Button(self.main_frame, text="Display Address Book", command=self.display_address_book)
        self.button_display.pack()

        self.button_delete = ttk.Button(self.main_frame, text="Delete Entry", command=self.open_delete_page)
        self.button_delete.pack()

        self.button_partial_search = ttk.Button(self.main_frame, text="Find Entries using Partial Names", command=self.partial_search)
        self.button_partial_search.pack()

        self.button_phone_email_search = ttk.Button(self.main_frame, text="Find Entries using Phone No. or Email", command=self.phone_email_search)
        self.button_phone_email_search.pack()

    def create_insert_page(self):
        self.clear_main_menu()
        self.insert_frame = tk.Frame(self)
        self.insert_frame.pack(fill=tk.BOTH, expand=True)

        self.label_name = ttk.Label(self.insert_frame, text="Name:")
        self.label_name.grid(row=0, column=0, sticky="w")

        self.entry_name = ttk.Entry(self.insert_frame)
        self.entry_name.grid(row=0, column=1)

        self.label_address = ttk.Label(self.insert_frame, text="Address:")
        self.label_address.grid(row=1, column=0, sticky="w")

        self.entry_address = ttk.Entry(self.insert_frame)
        self.entry_address.grid(row=1, column=1)

        self.label_phone = ttk.Label(self.insert_frame, text="Phone:")
        self.label_phone.grid(row=2, column=0, sticky="w")

        self.entry_phone = ttk.Entry(self.insert_frame)
        self.entry_phone.grid(row=2, column=1)

        self.label_email = ttk.Label(self.insert_frame, text="Email:")
        self.label_email.grid(row=3, column=0, sticky="w")

        self.entry_email = ttk.Entry(self.insert_frame)
        self.entry_email.grid(row=3, column=1)

        self.button_insert_entry = ttk.Button(self.insert_frame, text="Insert", command=self.insert_entry)
        self.button_insert_entry.grid(row=4, columnspan=2)

    def create_delete_page(self):
        self.clear_main_menu()
        self.display_address_book()
        self.delete_frame = tk.Frame(self)
        self.delete_frame.pack(fill=tk.BOTH, expand=True)

        self.label_delete = ttk.Label(self.delete_frame, text="Delete Entry")
        self.label_delete.pack(pady=10)

        self.delete_entry_name = simpledialog.askstring("Delete Entry", "Enter the name of the entry you want to delete:")

        if self.delete_entry_name:
            if self.delete_entry_name in self.address_book:
                del self.address_book[self.delete_entry_name]
                self.save_address_book()
                messagebox.showinfo("Success", "Entry deleted successfully.")
            else:
                messagebox.showerror("Error", "Entry not found.")

        self.clear_delete_page()

    def create_partial_search_page(self):
        self.clear_main_menu()
        self.display_address_book()
        self.partial_search_frame = tk.Frame(self)
        self.partial_search_frame.pack(fill=tk.BOTH, expand=True)

        self.label_partial_search = ttk.Label(self.partial_search_frame, text="Partial Search")
        self.label_partial_search.pack(pady=10)

        partial_name = simpledialog.askstring("Partial Search", "Enter partial name to search: ").lower()
        matches = [name for name in self.address_book.keys() if partial_name in name.lower()]

        if matches:
            messagebox.showinfo("Partial Name Matches", "Matches found:\n" + "\n".join(matches))
        else:
            messagebox.showinfo("Partial Name Matches", "No matches found.")

        self.clear_partial_search_page()

    def create_phone_email_search_page(self):
        self.clear_main_menu()
        self.display_address_book()
        self.phone_email_search_frame = tk.Frame(self)
        self.phone_email_search_frame.pack(fill=tk.BOTH, expand=True)

        self.label_phone_email_search = ttk.Label(self.phone_email_search_frame, text="Phone/Email Search")
        self.label_phone_email_search.pack(pady=10)

        contact_info = simpledialog.askstring("Phone/Email Search", "Enter phone number or email to search: ")
        matches = []
        for name, details in self.address_book.items():
            if contact_info in details.get("Phone", "") or contact_info in details.get("Email", ""):
                matches.append(name)

        if matches:
            messagebox.showinfo("Phone/Email Matches", "Matches found:\n" + "\n".join(matches))
        else:
            messagebox.showinfo("Phone/Email Matches", "No matches found.")

        self.clear_phone_email_search_page()

    def clear_main_menu(self):
        self.main_frame.destroy()

    def clear_insert_page(self):
        self.insert_frame.destroy()

    def clear_delete_page(self):
        self.delete_frame.destroy()

    def clear_partial_search_page(self):
        self.partial_search_frame.destroy()

    def clear_phone_email_search_page(self):
        self.phone_email_search_frame.destroy()

    def load_address_book(self):
        try:
            with open("addressbook.json", "r") as f:
                data = f.read()
                if data:  # Check if the file is not empty
                    self.address_book = json.loads(data)
                else:
                    self.address_book = {}
        except FileNotFoundError:
            self.address_book = {}

    def save_address_book(self):
        with open("addressbook.json", "w") as f:
            json.dump(self.address_book, f)

    def insert_entry(self):
        name = self.entry_name.get()
        address = self.entry_address.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        if name and address and phone and email:
            self.address_book[name] = {
                "Address": address,
                "Phone": phone,
                "Email": email
            }
            self.save_address_book()
            messagebox.showinfo("Success", "Entry added successfully.")
            self.clear_insert_page()
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def display_address_book(self):
        if self.address_book:
            display_window = tk.Toplevel(self)
            display_window.title("Address Book")
            display_text = tk.Text(display_window, font=("Arial", 14))  # Increase font size for display text
            display_text.pack()

            for name, details in self.address_book.items():
                display_text.insert(tk.END, f"Name: {name}\n")
                display_text.insert(tk.END, f"Address: {details['Address']}\n")
                display_text.insert(tk.END, f"Phone: {details['Phone']}\n")
                display_text.insert(tk.END, f"Email: {details['Email']}\n")
                display_text.insert(tk.END, "\n")
        else:
            messagebox.showwarning("Empty", "Address book is empty.")

    def open_insert_page(self):
        self.clear_main_menu()
        self.create_insert_page()

    def open_delete_page(self):
        self.clear_main_menu()
        self.create_delete_page()

    def partial_search(self):
        self.clear_main_menu()
        self.create_partial_search_page()

    def phone_email_search(self):
        self.clear_main_menu()
        self.create_phone_email_search_page()

if __name__ == "__main__":
    app = AddressBookApp()
    app.mainloop()