# LLM Comparison Study

This project conducts a comparative study of responses from various large language models (LLMs) (ChatGPT, Gemini, and Claude) on life experience judgment tasks.

## Table of Contents
1. [Requirements](#requirements)
2. [Setup Instructions](#setup-instructions)
3. [Running the Study](#running-the-study)
4. [Exporting and Sharing the Environment](#exporting-and-sharing-the-environment)

---

## Requirements

- **Python**: Version 3.9 (recommended).
- **Conda**: Ensure `conda` is installed for environment management.

The following LLM APIs are used:
- OpenAI (for ChatGPT)
- Google Generative AI (for Gemini)
- Anthropic (for Claude)

You will need API keys for each of these services. Place them in a `.env` file in the root directory.

### `.env` File Example
Put your API keys in the `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
```

---

## Setup Instructions

### 1. Clone the Repository
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/your-repo-url/llm-comparison-study.git
cd llm-comparison-study
```

### 2. Create and Activate the Conda Environment
Create a new Conda environment with Python 3.9 and activate it:
```bash
conda create -n llm_env python=3.9 -y
conda activate llm_env
```

### 3. Install Dependencies
Install the required packages and dependencies:
```bash
# Install general dependencies
conda install -c conda-forge pandas openpyxl tqdm -y
pip install python-dotenv

# Install LLM-specific dependencies
pip install google-generative-ai
pip install anthropic
```

### 4. Verify Setup
Check the installed packages to ensure everything is set up correctly:
```bash
conda list
```

---

## Running the Study

1. **Prepare the Dataset**:
   - Place the dataset file (`All_Studies_SigEvent_details_CLEANED_23.05.2024.xlsx`) in the `./data/dataset/` directory.

2. **Run the Script**:
   Execute the study script:
   ```bash
   python main.py
   ```

   Results will be saved in the `./data/output/` directory for each model.

---

## Exporting and Sharing the Environment

To share or reproduce the environment:

1. **Export the Environment**:
   Save the environment configuration to a `.yaml` file:
   ```bash
   conda env export > llm_env.yaml
   ```

2. **Recreate the Environment**:
   Use the `.yaml` file to recreate the environment on another system:
   ```bash
   conda env create -f llm_env.yaml
   conda activate llm_env
   ```

---

## Notes

- Ensure your API keys have sufficient quota to complete the study.
- Modify the `main.py` file to adjust the number of comparisons or participants.
- Refer to the code comments for further customization.

---
