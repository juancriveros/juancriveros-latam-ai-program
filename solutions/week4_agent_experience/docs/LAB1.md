# Lab: Comparing Prompts Across Multiple LLMs

> Week 1 – Prompt Engineering Basics

## Quick Start (If You Just Want to Run It)
```bash
git clone <your-fork-url>
cd <repo>/w1_prompt_engineering
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3 && ollama pull mistral
python prompt_lab.py --models local
```

## Learning Outcomes
By the end of this lab you will be able to:
1. Distinguish differences between simple, role, and chain-of-thought prompts.
2. Evaluate instruction adherence and tone across multiple LLM families.
3. Select an appropriate model for explanation vs. structured reasoning tasks.
4. Capture reproducible comparison data for future iterations (Prompt Playbook v1).

## Objective
Learn to craft and compare different prompt engineering techniques by sending prompts to multiple Large Language Models (LLMs), including locally-run Ollama models and major cloud-based models like OpenAI's GPT, Anthropic's Claude, and Google's Gemini.

## Instructions

1.  **Install and Run Ollama:**
    *   Follow the instructions on the [Ollama website](https://ollama.ai/) to download and install Ollama.
    *   Open your terminal and pull the models you want to test. We recommend starting with `llama3` and `mistral`:
        ```bash
        ollama pull llama3
        ollama pull mistral
        ```
    *   Ensure Ollama is running in the background.

2.  **Set up your Python Environment:**
    *   It is highly recommended to use a virtual environment.
    *   Activate your virtual environment and install the required libraries from `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```

3.  **(Optional) Configure API Keys:**
    *   To use the cloud-based models, you will need API keys from OpenAI, Anthropic, and Google.
    *   Set these keys as environment variables in your terminal. This is a secure way to handle sensitive keys.

    **For macOS/Linux:**
    ```bash
    export OPENAI_API_KEY='your_openai_api_key'
    export ANTHROPIC_API_KEY='your_anthropic_api_key'
    export GEMINI_API_KEY='your_google_api_key'
    ```

    **For Windows (Command Prompt):**
    ```bash
    set OPENAI_API_KEY=your_openai_api_key
    set ANTHROPIC_API_KEY=your_anthropic_api_key
    set GEMINI_API_KEY=your_google_api_key
    ```
    *   **Note:** You only need to set the keys for the models you want to test. The script will gracefully handle missing keys.

4.  **Run the Python Script:**
    *   Save the provided `prompt_lab.py` script.
    *   The script is configured to send three different prompts to a variety of models.
    *   Run the script from your terminal:
        ```bash
        python prompt_lab.py
        ```

5.  **Analyze the Outputs:**
    *   The script will print the response from each model for each prompt.
    *   Compare the outputs side-by-side. Notice how different models interpret the same prompt.
    *   Pay attention to differences in tone, detail, and adherence to instructions.

6.  **Document Your Findings:**
    *   Open the `PROMPT_PLAYBOOK.md` file.
    *   Based on your observations, document the strengths and weaknesses of each model for different prompt types. This will help you choose the right model for future tasks.

## Recommended Model Sets

### Local (Ollama)
| Model | Purpose | Notes |
|-------|---------|-------|
| llama3 | General baseline | Good balanced capabilities |
| mistral | Speed & efficiency | Often concise |
| phi3 (optional) | Small footprint | Good for lightweight tasks |
| qwen (optional) | Multilingual | Larger variants may be heavier |

### Hosted (Pick 2–3 First Run)
| Provider | Model | Strength |
|----------|-------|----------|
| OpenAI | gpt-4o-mini | Balanced quality/cost |
| OpenAI | gpt-4o | Higher reasoning, higher cost |
| Anthropic | claude-3-haiku | Fast + cheap |
| Anthropic | claude-3.5-sonnet | Strong reasoning + structure |
| Google | gemini-1.5-flash | Fast generation |
| Google | gemini-1.5-pro | Better depth |

> Tip: Only expand to more models after establishing a baseline with 2 local + 2 hosted.

## Suggested Evaluation Criteria
| Criterion | Description | Example Signals |
|-----------|-------------|-----------------|
| Instruction Adherence | Followed every directive? | Persona maintained, JSON valid |
| Reasoning Depth | Multi-step clarity | Intermediate steps explicit |
| Style Control | Tone matches role | Staying in character |
| Conciseness | Avoids rambling | Direct first paragraph |
| Format Fidelity | Structured output stable | Parses as JSON |

## Prompt Playbook Template Snippet
| Prompt Pattern | Example Used | Best Model(s) | Weak Model(s) | Failure Modes | Notes | Reuse? |
|----------------|--------------|---------------|---------------|---------------|-------|-------|

Failure Mode Tags: hallucination, verbosity, shallow, drift, persona-loss, json-break.

---

## Advanced Assignments

The `prompt_lab.py` script is already set up to test multiple prompts and models. To complete these assignments, you can:
1.  Modify the `PROMPTS` dictionary in the script to test your own prompt variations.
2.  Add or remove models from the `models_to_test` dictionary to expand or focus your comparison.

1.  **Chain-of-Thought Prompting:**
    *   **Task:** Create a prompt that asks the models to solve a simple math word problem. Instruct the model to "think step-by-step."
    *   **Success Criteria:** At least 3 intermediate reasoning steps before final answer.

2.  **Few-Shot Prompting:**
    *   **Task:** Craft a prompt that provides 2-3 examples of a task (e.g., sentiment analysis) before asking the model to perform a new one.
    *   **Success Criteria:** Output structure matches examples with <5% deviation.

3.  **Persona Prompting:**
    *   **Task:** Write a prompt that instructs the models to respond as a specific persona (e.g., a skeptical pirate).
    *   **Success Criteria:** Persona tone preserved across at least 3 paragraphs.

4.  **Structured Output (JSON):**
    *   **Task:** Create a prompt that requires the models to provide a response in a specific JSON format.
    *   **Success Criteria:** Valid JSON parses with `json.loads()` with no edits.

5.  **Negative Prompting:**
    *   **Task:** Write a prompt that specifies what you *don't* want (e.g., "Write a poem about the ocean, but do not use the words 'blue' or 'wave'").
    *   **Success Criteria:** Disallowed tokens absent in output.

After completing these assignments, document your new findings in `PROMPT_PLAYBOOK.md`. Compare the effectiveness of these advanced techniques across the different models.

## Troubleshooting
| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| Connection refused (Ollama) | Daemon not running | Start Ollama app / service |
| 401 from API | Missing or invalid key | Re-export env var, no quotes on Windows |
| Empty Gemini text | Safety filter triggered | Simplify or reduce sensitive terms |
| ModuleNotFoundError | venv not active | `source .venv/bin/activate` |
| JSON malformed | Model added commentary | Re-prompt: "Return ONLY valid JSON." |

## Next Week Preview
You will extend these insights into retrieval and context injection (RAG). Collect any questions about context length, lost instructions, or model drift for Week 2.

