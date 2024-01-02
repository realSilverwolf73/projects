from tkinter import *
from tkinter import Tk, Button, Entry, Label, filedialog
import os
import shutil
import json
import fitz
from PIL import Image, ImageTk

script_dir = os.path.dirname(os.path.realpath(__file__))
class mainGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDF Library")
        self.root.geometry('1090x1080')



class otherButtons:
    def __init__(self, main_gui, pdf_display):
        self.main_gui = main_gui
        self.pdf_display = pdf_display
        self.pdf_files = []  # Initialize the list to store PDF file information
        self.searchbar = Entry(self.main_gui.root, width=30, borderwidth=5, bg="white")
        self.searchbar.place(x=0, y=0)
        self.searchbutton = Button(self.main_gui.root, text="Search", command=self.search)
        self.searchbutton.place(x=190, y=0)
        self.importbutton = Button(self.main_gui.root, text="Import", command=self.import_pdf_dialog)
        self.importbutton.place(x=1033, y=0)
        self.removebutton = Button(self.main_gui.root, text="Remove please", command=self.remove_pdf)
        self.removebutton.place(x=944, y=0)

    def remove_pdf(self):
        global confirmpos
        self.pdf_display.display_all_books()
        self.checked_indices = {}  # Create a list to store the indices of the checked boxes
        xloc, yloc = 13, 80

        pdfList = self.pdf_display.makeList()
        for pdf_name in pdfList:
            x = IntVar()
            box_remove = Checkbutton(self.main_gui.root, variable=x, onvalue=1, offvalue=0)
            box_remove.place(x=xloc, y=yloc)
            self.checked_indices[pdf_name] = x

            confirmpos = 0
            xloc += 220
            if xloc >= 1000:
                yloc += 260
                xloc = 13
                confirmpos = yloc

            self.confirm_button = Button(self.main_gui.root, text="Confirm Remove", command=self.confirm_remove)
            self.confirm_button.place(x=13, y=40)

    def confirm_remove(self):
        for pdf_name, x in self.checked_indices.items():
            if x.get() == 1:
                filename = os.path.basename(pdf_name)  # Get the filename from the path
                destination_path = r"C:\Users\HP\Downloads"
                shutil.move(r"E:\BootlegLibrary\Container\\" + pdf_name, destination_path)

        self.confirm_button.destroy()
        for widget in self.main_gui.root.winfo_children():
            if isinstance(widget, Checkbutton):
                widget.destroy()

        # Update the list of PDF files with the new file information
        self.pdf_display.makeList()
        self.pdf_display.clear_display()
        self.pdf_display.display_all_books()

    def search(self):
        query = self.searchbar.get()
        for widget in self.main_gui.root.winfo_children():
            if isinstance(widget, Checkbutton):
                widget.destroy()
        if query:
            if query == '':
                self.pdf_display.clear_message()
            self.pdf_display.clear_message()
            matched = [i for i in self.pdf_display.makeList() if query.lower() in i.lower()[:len(query)]]
            self.pdf_display.display_search_results(matched)
            if matched == []:  # Check if matched is an empty list
                self.pdf_display.display_message("Can't find any")
        else:
            self.pdf_display.clear_message()
            self.pdf_display.display_all_books()

    def import_pdf(self, pdf_file):
        # Specify the destination folder path
        destination = r"E:\BootlegLibrary\Container"

        # Move the selected PDF file to the destination folder
        filename = os.path.basename(pdf_file)
        destination_file = os.path.join(destination, filename)
        shutil.move(pdf_file, destination_file)

        # Update the list of PDF files with the new file information
        self.pdf_display.clear_display()

    def import_pdf_dialog(self):
        # Open a file dialog to import a PDF file
        pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_file:
            self.import_pdf(pdf_file)
            self.pdf_display.makeList()
            self.pdf_display.display_all_books()


class PDFdisplay:
    def __init__(self, main_gui, other_buttons):
        self.other_buttons = other_buttons
        self.main_gui = main_gui
        self.searchbar = None
        self.message_label = None
        self.booklist = self.makeList()
        self.display_all_books()

    def makeList(self):
        try:
            # List all files in the specified folder
            files = os.listdir(r"E:\BootlegLibrary\Container")
            return files
        except OSError:
            print(f"Error accessing folder: {r'E:\BootlegLibrary\Container'}")
            return []

    def pdfThumbnail(self, pdf_path, height=180, width=130):
        try:
            pdf_document = fitz.open(pdf_path)

            # Check if the document is not empty
            if pdf_document.page_count == 0:
                raise fitz.EmptyFileError("Empty document")

            # Get the first page
            first_page = pdf_document[0]

            # Convert the page to a pixmap
            pixmap = first_page.get_pixmap()

            # Close the PDF document
            pdf_document.close()

            # Convert the pixmap to a PhotoImage
            image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(resized_image)

            return photo_image
        except fitz.EmptyFileError as e:
            # Handle the empty document error, you can print a message or log it
            print(f"Error: {e}")
            # You may choose to return a default image or handle it in another way
            return None

    def open_file(self, file_path):
        os.startfile(file_path)

    def display_all_books(self):
        self.clear_display()
        piss = self.makeList()
        axe, why = 40, 80
        for book in piss:
            thumbnail = self.pdfThumbnail(r"E:\BootlegLibrary\Container\\" + book)
            if thumbnail:
                book_display = Button(self.main_gui.root, image=thumbnail, height=180, width=130,
                                      command=lambda x=(r"E:\BootlegLibrary\Container\\" + book): self.open_file(x))
                book_name = Label(self.main_gui.root, text=book[:-4], anchor="n", height=3, width=21, wraplength=130, justify="left", font=("Helvetica", 9, "bold"))
                book_name.place(x=axe - 10, y=why + 185)
                book_display.image = thumbnail
                book_display.place(x=axe, y=why)
                axe += 220
                if axe >= 1000:
                    why += 260
                    axe = 40

    def display_search_results(self, matched):
        self.clear_display()
        axe, why = 40, 80
        for book in matched:
            thumbnail = self.pdfThumbnail(r"E:\BootlegLibrary\Container\\" + book)
            if thumbnail:
                book_display = Button(self.main_gui.root, image=thumbnail, height=180, width=130,
                                      command=lambda x=(r"E:\BootlegLibrary\Container\\" + book): self.open_file(x))
                book_name = Label(self.main_gui.root, text=book[:-4], anchor="n", height=3, width=21, wraplength=130, justify="left", font=("Helvetica", 9, "bold"))
                book_name.place(x=axe - 10, y=why + 185)
                book_display.image = thumbnail
                book_display.place(x=axe, y=why)
                axe += 220
                if axe >= 1000:
                    why += 260
                    axe = 40

    def clear_display(self):
        for widget in self.main_gui.root.winfo_children():
            if self.other_buttons is not None:
                if isinstance(widget, (Button, Label)) and widget not in [
                    self.other_buttons.searchbutton, self.other_buttons.importbutton,
                    self.other_buttons.removebutton]:
                    widget.destroy()

    def clear_message(self):
        # Check if there's an existing message label and destroy it
        if self.message_label:
            self.message_label.destroy()

    def display_message(self, message):
        self.clear_message()  # Clear existing message label
        self.message_label = Label(self.main_gui.root, text=message, 
                                   font=("Helvetica", 16, "bold"))
        self.message_label.place(x=475, y=325)


if __name__ == "__main__":
    gui = mainGUI()
    other_buttons = otherButtons(gui, pdf_display=None)  # Pass None for now, it will be updated later
    pdf_display = PDFdisplay(gui, other_buttons=other_buttons)  # Pass other_buttons to PDFdisplay
    other_buttons.pdf_display = pdf_display  # Set pdf_display in other_buttons after creating PDFdisplay instance
    gui.root.mainloop()
