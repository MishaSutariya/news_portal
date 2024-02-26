import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, StringVar
import webbrowser
from translate import Translator

# Function to fetch news content from the website
def fetch_website_content(url, news_class):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_elements = soup.find_all(class_=news_class)

        return news_elements
    else:
        return None

# Function to translate content using translate library
def translate_content(content, target_language='hi'):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(content)
    return translation

# Function to display translated results
def show_results():
    selected_website = website_var.get()
    selected_language = language_var.get()  # Get selected language

    results_text.config(state='normal')
    results_text.delete(1.0, tk.END)

    if selected_website in websites and selected_language in languages:
        url = websites[selected_website]["url"]
        news_class = websites[selected_website]["class"]

        news_elements = fetch_website_content(url, news_class)

        if news_elements:
            for idx, news_element in enumerate(news_elements, start=1):
                # Extract the link and content
                news_link = news_element.find('a')['href']
                news_content = news_element.get_text(strip=True)

                # Translate the content to the selected language
                translated_content = translate_content(news_content, target_language=selected_language)

                # Display the translated content as clickable blue underlined text only if it starts with 'https://'
                if news_link.startswith('https://'):
                    results_text.insert(tk.END, f"{translated_content}\n")
                    results_text.tag_add(f"link-{idx}", tk.END + f"-{len(translated_content)}c", tk.END)
                    results_text.tag_config(f"link-{idx}", foreground="blue", underline=True)
                    results_text.tag_bind(f"link-{idx}", "<Button-1>", lambda event, link=news_link: open_link(link))
                else:
                    results_text.insert(tk.END, f"{translated_content}\n")

            results_text.config(state='disabled')  # Disable text widget to make it read-only
        else:
            results_text.insert(tk.END, "Error: Unable to fetch the website.")
            results_text.config(state='disabled')  # Disable text widget to make it read-only
    else:
        results_text.insert(tk.END, "Error: Selected website or language not found.")
        results_text.config(state='disabled')  # Disable text widget to make it read-only

# Function to open the link in a web browser
def open_link(link):
    webbrowser.open(link)

# Define the websites and their details
websites = {
    "Health and Family Welfare": {"url": "https://www.mohfw.gov.in/", "class": "update-box"},
    "Education": {"url": "https://www.education.gov.in/", "class": "tabcontentstyle updtfull"},
}

# Languages
languages = ["hi", "en", "gu", "mr", "bn", "sa"]

# Create main window
root = tk.Tk()
root.title("Web Scraping Results")

# Create a dropdown menu to select the website
website_var = StringVar(root)
website_var.set(list(websites.keys())[0])  # Set default value
website_menu = tk.OptionMenu(root, website_var, *websites.keys())
website_menu.pack(pady=10)

# Create a dropdown menu to select the language
language_var = StringVar(root)
language_var.set(languages[0])  # Set default value
language_menu = tk.OptionMenu(root, language_var, *languages)
language_menu.pack(pady=10)

# Create a button to trigger web scraping and display results
fetch_button = tk.Button(root, text="New Update", command=show_results)
fetch_button.pack(pady=10)

# Create a scrolled text widget to display results
results_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, state='disabled')
results_text.pack(padx=10, pady=10)

root.mainloop()




