```txt
# AI Agent Project

This project is an AI agent that uses the OpenAI API to analyze and generate data based on a given dataset. The code reads a CSV file, processes the data, and uses two agents to analyze and generate new data.

## Project Structure

- `agent.py`: Main script to run the AI agents.
- `prompts.py`: Contains the system and user prompts for the agents.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Docker configuration for containerizing the application.
- `data/`: Directory containing the input dataset and where the generated dataset will be saved.
- `.env`: Environment file containing your OpenAI API key (not included, must be created).

## Prerequisites

- Python 3.8 or higher
- Docker
- OpenAI API key

## Setup Instructions

### Local Setup

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the root directory with the following content:
    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Place your dataset CSV file** in the `data` directory.

6. **Run the script**:
    ```sh
    python agent.py
    ```

### Docker Setup

1. **Build the Docker image**:
    ```sh
    docker build -t openai-agent .
    ```

2. **Run the Docker container**:
    ```sh
    docker run -it --env-file .env openai-agent
    ```

## Usage

1. When prompted, enter the name of your dataset file (e.g., `dataset.csv`).
2. Enter the number of rows you want in the generated dataset.
3. The agents will analyze the sample data and generate new data, which will be saved in `data/new_dataset.csv`.

## Example

```plaintext
Please enter the dataset file name (e.g., dataset.csv): dataset.csv
Enter the number of rows you want in the dataset: 40

Launching team of Agents...

### Analyzer agent output: ###

<Analysis result here>

-------------------------

Generating new data...
Generated 30 rows out of 40
Generated 40 rows out of 40

Generated data has been saved to data/new_dataset.csv
```

## Error Handling

- If the dataset file is not found, you will see an error message: `Error: File not found at data/<file_name>`.
- If the analysis or data generation fails, you will see appropriate error messages indicating the issue.

## License

This project is licensed under the MIT License.
```
