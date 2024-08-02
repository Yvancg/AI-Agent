'''AI agent'''

import os
import csv
from openai import OpenAI
from dotenv import load_dotenv
from prompts import (
    ANALYZER_SYSTEM_PROMPT,
    GENERATOR_SYSTEM_PROMPT,
    ANALYZER_USER_PROMPT,
    GENERATOR_USER_PROMPT
)

# Load environment variables from .env file
load_dotenv()

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

def read_csv(file_path):
    """Reads a CSV file and returns its content as a list of rows."""
    data = []
    try:
        with open(file_path, "r", newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error: {e}")
    return data

def save_to_csv(data, output_file, headers=None):
    """Saves data to a CSV file. If headers are provided, they are written first."""
    mode = "w" if headers else "a"
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        if data:
            for row in csv.reader(data.splitlines()):
                writer.writerow(row)

def analyzer_agent(sample_data):
    """Analyzes the sample data using the OpenAI API and returns the analysis result."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ANALYZER_SYSTEM_PROMPT},
                {"role": "user", "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)}
            ],
            max_tokens=400,
            temperature=0.1
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None

def generator_agent(analysis_result, sample_data, num_rows=30):
    """Generates new data based on the analysis result and sample data using the OpenAI API."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": GENERATOR_SYSTEM_PROMPT},
                {"role": "user", "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )}
            ],
            max_tokens=1500,
            temperature=1
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during data generation: {e}")
        return None

def main():
    input_file = input("Please enter the dataset file name (e.g., dataset.csv): ")
    input_file_path = os.path.join("data", input_file)
    
    try:
        desired_rows = int(input("Enter the number of rows you want in the dataset: "))
    except ValueError:
        print("Invalid number of rows. Exiting...")
        return

    sample_data = read_csv(input_file_path)
    if not sample_data:
        print("No data found. Exiting...")
        return

    sample_data_str = "\n".join([",".join(row) for row in sample_data])

    print("\nLaunching team of Agents...")
    analysis_result = analyzer_agent(sample_data_str)
    if not analysis_result:
        print("Analysis failed. Exiting...")
        return

    print("\n### Analyzer agent output: ###\n")
    print(analysis_result)
    print("\n-------------------------\n\nGenerating new data...")

    output_file_path = os.path.join("data", "new_dataset.csv")
    headers = sample_data[0]
    save_to_csv("", output_file_path, headers)

    batch_size = 30
    generated_rows = 0

    while generated_rows < desired_rows:
        rows_to_generate = min(batch_size, desired_rows - generated_rows)
        generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)
        if generated_data:
            save_to_csv(generated_data, output_file_path)
            generated_rows += rows_to_generate
            print(f"Generated {generated_rows} rows out of {desired_rows}")
        else:
            print("Data generation failed. Exiting...")
            return

    print(f"\nGenerated data has been saved to {output_file_path}")

if __name__ == "__main__":
    main()
