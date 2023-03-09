from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
import glob
import time
from tqdm import tqdm
from plyer import notification
import sys


# this will find all html files in the current directory
html_files = glob.glob("*.html")
print(html_files)  # inspect html files

# loop over the files
for file in tqdm(
    [
        "universities.html",
        "subjects.html",
    ],
    file=sys.stdout,
    colour="green",
):
    print(f"Translating {file}")

    # Open English HTML file
    with open(file, "r", encoding="utf-8") as f:
        # Read HTML content
        html = f.read()

        # Parse HTML using bs4
        soup = BeautifulSoup(html, "html.parser")

        # Find all text nodes that contain English text
        texts = soup.find_all(string=True)

        # Loop through each text node
        for text in texts:
            if text.parent.name not in ["script", "style"]:
                # Skip the element if it's empty
                if (text is not None) and (not text.isspace()):
                    try:
                        # Translate English text to Hindi using GoogleTranslator
                        hindi_text = GoogleTranslator(
                            source="en", target="hi"
                        ).translate(
                            text
                        )  # "उदाहरण"
                        # Replace original text node with translated one
                        text.replace_with(hindi_text)
                    except Exception as e:  # Catch the ValueError exception
                        print(f"File {file} has Exception {e}")  # Handle the error

    # Open Hindi HTML file for writing
    with open(file, "w", encoding="utf-8") as f:
        # Write translated HTML content
        f.write(soup.prettify())

    # wait
    time.sleep(2)  # seconds

    # break

# Send a notification when the code finishes
notification.notify(
    title="Translation done",
    message="All files have been translated to Hindi.",
    timeout=10,
)
