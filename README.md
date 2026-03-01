# AI-Assisted-Code-Review-Tool
Modular Python tool that integrates Pylint, Bandit, and Radon to normalize static analysis findings and prepare structured datasets for AI-assisted code review. (Work in progress)

To run the system, use the command line from the project directory:

python run_review.py path/to/file.py

This project is a Python-based code review system that combines traditional static analysis tools with a structured AI explanation layer. It runs Pylint, Bandit, and Radon on a target Python file, collects their findings, and converts them into a consistent format. Although these tools detect issues effectively, their messages are often short and technical. The purpose of this project is to standardize those findings and prepare them for use in an AI model that can generate clearer, structured explanations.

Each analyzer is implemented in its own module, while run_review.py acts as the orchestrator. It validates the input file, executes the analyzers, prints the findings, and optionally exports selected results into a JSONL file. The export feature was specifically designed to support training dataset generation.

To build the dataset, I created small example Python files that intentionally triggered specific static analysis warnings. I then used my own tool to analyze those files and automatically append the normalized findings to a training file. After collecting the structured inputs, I used ChatGPT to generate detailed explanations for each finding. These explanations were reviewed and formatted into strict JSON so they could be used for model fine-tuning.

Each dataset entry contains the normalized finding as input and a structured explanation as output. The long-term goal is to fine-tune a language model so that it can automatically generate explanations for new static analysis findings. This would transform the system from a wrapper around analysis tools into an intelligent code review assistant.
