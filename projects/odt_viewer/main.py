import tkinter as tk
from odfdo import Document

# Function to apply formatting to text based on the element's style
def insert_text_with_formatting(text_widget, text, element_type):
    if element_type == "heading":
        # Example: Apply bold for headings
        text_widget.insert(tk.END, text + "\n", "heading")
    elif element_type == "paragraph":
        # Example: Apply normal text for paragraphs
        text_widget.insert(tk.END, text + "\n", "paragraph")
    elif element_type == "bold":
        text_widget.insert(tk.END, text, "bold")
    elif element_type == "italic":
        text_widget.insert(tk.END, text, "italic")
    else:
        # Default case for unhandled elements
        text_widget.insert(tk.END, text + "\n")

# Function to parse the ODT document and display content in the Tkinter window
def parse_odt_and_display(odt_file, text_widget):
    # Load the ODT document
    document = Document(odt_file)
    print(document.content)
    
    # Iterate through the document elements
    for element in document.body.children:
        print(element.tag)
        if element.tag == "text:h":
            # Heading element
            heading_text = element.text
            insert_text_with_formatting(text_widget, heading_text, "heading")
        elif element.tag == "text:p":
            # Paragraph element
            paragraph_text = element.text
            print(f"P {paragraph_text}")
            insert_text_with_formatting(text_widget, paragraph_text, "paragraph")
        elif element.tag == "text:span":
            # Inline formatted text (e.g., bold, italic)
            span_text = element.text
            # Check for bold or italic formatting
            if element.get_style() == "Bold":
                insert_text_with_formatting(text_widget, span_text, "bold")
            elif element.get_style() == "Italic":
                insert_text_with_formatting(text_widget, span_text, "italic")
            else:
                insert_text_with_formatting(text_widget, span_text, "paragraph")
        elif element.tag == "text:soft-page-break":
            insert_text_with_formatting(text_widget, "--------\n", "bold")
            print(element.text)
        else:
            # Handle other elements as needed
            other_text = element.text
            insert_text_with_formatting(text_widget, other_text, "paragraph")

# Function to display the ODT content in a Tkinter window
def display_odt_in_tkinter(odt_file):
    # Create the main window
    root = tk.Tk()
    root.title("ODT Viewer")

    # Create a Text widget to display the ODT content
    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(expand=True, fill=tk.BOTH)

    # Configure tags for different formatting styles
    text_widget.tag_configure("heading", font=("Arial", 16, "bold"))
    text_widget.tag_configure("paragraph", font=("Arial", 12))
    text_widget.tag_configure("bold", font=("Arial", 12, "bold"))
    text_widget.tag_configure("italic", font=("Arial", 12, "italic"))

    # Parse the ODT file and display the content
    parse_odt_and_display(odt_file, text_widget)

    # Run the Tkinter event loop
    root.mainloop()

# Provide the path to your .odt file
odt_file_path = "example.odt"
display_odt_in_tkinter(odt_file_path)
