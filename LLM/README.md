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

### How to Obtain API Keys for LLM Providers

To use this project, you'll need API keys for OpenAI (ChatGPT), Google Generative AI (Gemini), and Anthropic (Claude). Follow the instructions below to obtain the API keys:

---

#### **OpenAI (ChatGPT)**

1. **Sign Up or Log In:**
   - Visit the [OpenAI Platform](https://platform.openai.com/signup) to create an account or log in.

2. **Navigate to API Keys:**
   - Go to the [API Keys page](https://platform.openai.com/account/api-keys).

3. **Create a New Key:**
   - Click on "Create new secret key" to generate your API key.

4. **Copy and Store the Key:**
   - Copy the generated key and store it securely. You'll need it to authenticate your API requests.

For more details, refer to OpenAI's guide: [Where do I find my OpenAI API Key?](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)

---

#### **Google Generative AI (Gemini)**

1. **Access Google AI Studio:**
   - Navigate to [Google AI Studio](https://ai.google.dev/).

2. **Sign In with Google Account:**
   - Use your Google account to sign in.

3. **Create a New Project:**
   - If you don’t already have a project, create a new one in the Google Cloud Console.

4. **Enable Gemini API:**
   - In your project dashboard, enable the Gemini API.

5. **Generate API Key:**
   - Go to the "Credentials" section and click on "Create Credentials" to generate an API key.

6. **Secure Your API Key:**
   - Copy the API key and store it securely for future use.

For more information, see Google's guide: [Get a Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)

---

#### **Anthropic (Claude)**

1. **Visit Anthropic's Console:**
   - Go to the [Anthropic Console](https://console.anthropic.com/).

2. **Sign Up or Log In:**
   - Create an account or log in if you already have one.

3. **Access API Keys Section:**
   - In the console, navigate to the "API Keys" section.

4. **Generate a New API Key:**
   - Click on "Create API Key" to generate a new key.

5. **Store the Key Securely:**
   - Copy the API key and ensure it’s stored securely for your application's use.

For detailed steps, refer to Anthropic's documentation: [Initial setup](https://docs.anthropic.com/en/docs/initial-setup)

---

### `.env` File Example
Put your API keys in the `/LLM/.env` file:
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
