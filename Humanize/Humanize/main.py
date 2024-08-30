import requests
import json
import html
import tkinter as tk
from tkinter import scrolledtext
from bs4 import BeautifulSoup


def htmlify(text: str) -> str:
    return html.escape(text)


def humanize(text: str):
    htmlifyd_text = htmlify(text)

    url = "https://humanizeaitext-backend-epxkamsm6a-uc.a.run.app/humanize-free"

    payload = json.dumps({
        "type": "bypass_ai_finetune",
        "data": {
            "prompts": [
                htmlifyd_text
            ],
            "target": "EN-US",
            "source": "EN-US",
            "standardGoals": {
                "contentFocus": "Generates content that primarily focuses on conveying information.",
                "engagementLevel": "Generates content with moderate engagement, balancing information and reader interest.",
                "tone": "Maintains a neutral tone.",
                "clarity": "Generates content with a focus on clarity, avoiding ambiguity and confusion.",
                "languageComplexity": "Uses straightforward language and sentence structures suitable for easy comprehension"
            }
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    soup = BeautifulSoup(response['data']['content'][0], 'html.parser')
    removed_html = soup.get_text()

    return removed_html


def check_gptzero(text: str):
    url = "https://api.gptzero.me/v2/predict/text"

    payload = json.dumps({
        "document": text,
        "source": "landing",
        "writing_stats_required": True,
        "sampleTextSubmitted": None,
        "interpretability_required": False,
        "checkPlagiarism": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.request("POST", url, headers=headers, data=payload).json()

def check_gptzerov1(text: str):
    url = "https://us-central1-aiseo-official.cloudfunctions.net/gpt-zero-v1"

    payload = json.dumps({
        "sentence": text
    })
    headers = {
        'Content-Type': 'application/json'
    }

    return requests.request("POST", url, headers=headers, data=payload).json()


def process_text():
    ai_text = text_entry.get('1.0', tk.END)

    humanized = humanize(ai_text)
    removed_html = html.unescape(humanized)

    # gptzero_res = check_gptzero(removed_html)
    #
    # gptzerov2_res = check_gptzerov1(removed_html)

    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Humanized text: \n" + removed_html + "\n\n")

    # gptzero_message = gptzero_res['documents'][0]['result_message']
    # result_text.insert(tk.END, "GPT-zero response: \n" + gptzero_message + "\n\n")
    #
    # ai_percentage = gptzero_res['documents'][0]['class_probabilities']['ai'] * 100
    # human_percentage = gptzero_res['documents'][0]['class_probabilities']['human'] * 100
    # mixed = gptzero_res['documents'][0]['class_probabilities']['mixed'] * 100
    #
    # result_text.insert(tk.END, f"\nPercentage of text written by AI: {ai_percentage:.2f}%\nPercentage of text written "
    #                            f"by a Human: {human_percentage:.2f}%\nPercentage of text mixed: {mixed:.2f}%")


root = tk.Tk()
root.title("Humanize AI Text")

text_entry = scrolledtext.ScrolledText(root, width=70, height=50)
text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

process_button = tk.Button(root, text="Humanize", command=process_text)
process_button.pack(side=tk.LEFT, fill=tk.Y)

result_text = scrolledtext.ScrolledText(root, width=70, height=50)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()
