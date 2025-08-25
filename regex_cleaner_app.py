import re
import gradio as gr
import nltk
from nltk.corpus import stopwords

# Download stopwords (only needed once)
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def regex_cleaner(text):
    # Default regex pattern (remove everything except letters and spaces)
    pattern = r"[^a-zA-Z\s]"

    # Check if input looks like a URL of the form www.something.com
    url_pattern = r"^www\.([^.]+)\.com$"
    url_match = re.match(url_pattern, text)

    if url_match:
        cleaned_text = url_match.group(1)   # extract only 'something'
        code_used = f'''
import re

pattern = r"{url_pattern}"
match = re.match(pattern, text)
if match:
    cleaned_text = match.group(1)  # extracts the middle part
'''
    else:
        # Apply general regex cleaning
        cleaned_text = re.sub(pattern, "", text)

        # Remove stopwords
        words = cleaned_text.split()
        filtered_words = [w for w in words if w.lower() not in stop_words]
        cleaned_text = " ".join(filtered_words)

        code_used = f'''
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))
pattern = r"{pattern}"

# Remove unwanted chars
cleaned_text = re.sub(pattern, "", text)

# Remove stopwords
words = cleaned_text.split()
filtered_words = [w for w in words if w.lower() not in stop_words]
cleaned_text = " ".join(filtered_words)
'''

    return cleaned_text, code_used


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📝 Regex Cleaner (NLP Project)")

    with gr.Row():
        input_text = gr.Textbox(label="Enter Text", lines=4, placeholder="Type your text here...")

    with gr.Row():
        output_text = gr.Textbox(label="Cleaned Text (Regex Removed)", lines=4)
        code_output = gr.Textbox(label="Code Used", lines=6)

    run_btn = gr.Button("Run Regex Cleaner")

    run_btn.click(regex_cleaner, inputs=input_text, outputs=[output_text, code_output])

# Launch app
if __name__ == "__main__":
    demo.launch()
