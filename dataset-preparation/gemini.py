import csv
import google.generativeai as genai
import time
from tqdm import tqdm


api_key='<Paste Gemini API Key here>'

genai.configure(api_key=api_key)


generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
])


def extract_second_column(input_file, start_row):
    second_column_entries = []
    with open(input_file, 'r', newline='', encoding='utf-8') as csv_input:
        reader = csv.reader(csv_input)
        for index, row in enumerate(reader):
            if index >= start_row - 1:  # Adjust index to 0-based
                if len(row) >= 2:
                    second_column_entries.append(row[1])  # Assuming the second column is at index 1
    return second_column_entries


input_file = r'csv\Dataset_OnlyQ.csv'  # Using raw string to handle backslashes
start_row = 78+81+97+74+46
second_column_entries = extract_second_column(input_file, start_row)


with tqdm(total=len(second_column_entries)) as pbar:
    for entry in second_column_entries:
        # Start a chat with the model using the current entry from the second column
        gendral = "Answer the following questions:"
        entry = gendral + entry
        convo.send_message(entry)

        # Check if the conversation has any messages
        if convo.last is not None:
            response = convo.last.text
            print(f"Input: {entry},\n Response: {response}")
        else:
            print(f"Input: {entry}, No response from the model.")

        # Write input and output to a new CSV file
        with open('csv\output_OnlyA.csv', 'a', newline='', encoding='utf-8') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow([entry, response])

        # Introduce a delay to ensure only 60 queries go in a minute
        time.sleep(1)  # Sleep for 1 second between queries
        pbar.update(1)

print("Model's responses printed and saved to 'output.csv'.")
