# Prompt Playbook v1

## Objective
Capture empirical observations comparing prompt variants and model behaviors. Use this as a living artifact you will refine in future weeks.

## How to Use This File
1. After each script run, append rows to the Results Table.
2. Tag failure modes (see legend) so patterns emerge quickly.
3. Summarize insights after completing stretch assignments.

## Scoring Rubric (1–5)
| Score | Instruction Adherence | Reasoning Depth | Style / Persona | Format Fidelity |
|-------|-----------------------|-----------------|-----------------|-----------------|
| 1 | Misses key directives | Single sentence | Ignores persona | Broken / ignores |
| 3 | Mostly follows | Some steps implicit | Partial persona | Minor drift |
| 5 | Precise & complete | Clear multi-step chain | Fully consistent | Exact, parsable |

## Failure Mode Tags
hallucination, verbosity, shallow, drift (format), persona-loss, json-break, constraint-fail

## Results Table (Populate During Lab)
| Prompt Pattern | Example Used | Model | Adherence (1–5) | Reasoning (1–5) | Style (1–5) | Format (1–5) | Failure Modes | Notes | Reuse? (Y/N) |
|----------------|--------------|-------|------------------|-----------------|-------------|--------------|---------------|-------|--------------|
| Simple | Explain how planes fly | llama3 | 5 | 5 | 5 | 5 |  | Really specific on details without asking them | Y |
| Simple | Explain how planes fly | mistral | 4 | 4 | 5 | 5 |  | Stay with a simple explanation but concise | Y |
| Role | You are an aerospacial engineer | llama3 | 5 | 5 | 5 | 5 |  | Explaines landing and take off | Y |
| Role | You are an aerospacial engineer | mistral | 4 | 4 | 5 | 5 |  | Not much added to the simple model | Y |
| Chain of thought | Explain how planes fly step-by-step | llama3 | 5 | 5 | 5 | 5 |  | Explain all steps correct | Y |
| Chain of thought | Explain how planes fly step-by-step | mistral | 5 | 5 | 5 | 5 |  | Added more inputs than llama3 | Y |
| Few-Shot | Palindrome | llama3 | 4 | 4 | 5 | 5 |  | Just words | Y |
| Few-Shot | Explain how planes fly step-by-step | mistral | 5 | 5 | 5 | 5 |  | Added sentences | Y |
| Persona | Most difficult jobs for a housemaid | llama3 | 5 | 5 | 5 | 5 |  | Impersionate and replied as the role | Y |
| Persona | Explain how planes fly step-by-step | mistral | 4 | 5 | 3 | 5 | persona-loss | Did not reply as the role, but it makes sense | Y |
| Negative | Write a sentence of 10 words without using the vowel a | llama3 | 1 | 5 | 5 | 5 | fail | Could not make it | Y |
| Negative | Write a sentence of 10 words without using the vowel a | mistral | 1 | 5 | 5 | 5 | fail | Could not make it | Y |

## Model Summary (After Initial Pass)
| Capability | Best Model(s) | Evidence Snippet | Notes |
|------------|---------------|------------------|-------|
| Explanatory Clarity | llama3 | **The Four Forces of Flight** ...| It is structured and concise |
| Chain-of-Thought | llama3 | Here's a step-by-step explanation of how planes fly, starting with the necessary inputs and ending with the outputs: | It mixed the process of flying with the physics |
| JSON Adherence | | | |
| Persona Control | llama3 | Good day sir/ma'am! As a housemaid, I'm happy to share with you the three most challenging tasks I face in my daily routine. | It impersonate the persona correctly |
| Instruction Strictness | none | | |

## Insight Log
Record notable surprises, regressions, or improvements.
- Day 1:
- Day 2:
- Day 3:

---

### 1. Role Prompting

*   **Best Practice:**
    *   Clearly define the persona or role you want the AI to adopt. This helps to set the context, tone, and level of detail in the response.
*   **Example:**
    *   Instead of "Explain black holes," use "You are an astrophysicist. Explain the concept of a black hole to a curious 10-year-old."

---

### 2. Few-Shot Learning

*   **Best Practice:**
    *   Provide a few examples of the desired input and output format. This is especially useful for tasks like classification, summarization, or code generation.
*   **Example:**
    *   When asking for a summary, provide one or two examples of a text and its corresponding summary before providing the text you want to be summarized.

---

### 3. Chain-of-Thought (CoT)

*   **Best Practice:**
    *   Encourage the model to "think step by step" or to "show its work." This is particularly effective for complex reasoning tasks, such as math problems or logic puzzles.
*   **Example:**
    *   Append "Let's think step by step" to your prompt when you need the model to reason through a problem.

---

### 4. Anti-Patterns to Avoid
## Reflection (End of Week)
Answer briefly:
1. Which two prompt patterns yielded the largest delta between models?
2. Which failure mode was most frequent? Root cause?
3. Default model choice for: explanation / reasoning / structure.
4. Open questions heading into Week 2.
*   **Ambiguity:**
    *   Avoid vague or open-ended questions. Be as specific as possible.
*   **Leading Questions:**
    *   Don't phrase your prompt in a way that suggests a desired answer.
*   **Overly Complex Prompts:**
    *   Break down complex tasks into smaller, more manageable prompts.

---

# Week 2:

## Evaluation & Logging

| Query | Mode (raw/RAG) | k | Retrieved IDs | Strengths | Weaknesses | Failure Modes | Notes | Latency (s) |
|--------|------|---|----------------|------------|-------------|----------------|--------|--------------|
| How can I return a product? | RAG | 1 | faq1 | Completeness | Brevity | verbose | Long but it invents steps. | 9.23 |
| How can I return a product? | RAG | 2 | faq1, faq10 | Grounding | Brevity | verbose | Some redundency | 5.68 |
| How can I return a product? | RAG | 3 | faq1, faq10, faq4 | Completeness | Brevity | partial | Good. | 4.17 |
| How can I return a product? | RAG | 4 | faq1, faq10, faq4, faq2 | Traceability | Relevance | irrelevant | Adds trancking context. | 5.10 |
| What's the process for tracking my package? | RAG | 1 | faq2 | Relevance | Brevity | – | Precise. | 3.15 |
| What's the process for tracking my package? | RAG | 2 | Grounding | Brevity | – | Some additional context | 3.56 |
| What's the process for tracking my package? | RAG | 3 | Traceability | Relevance | irrelevant | Adds some incorrect context. | 3.74 |
| What's the process for tracking my package? | RAG | 4 | Traceability | Relevance | irrelevant | Add wrong context. | 4.70 |
| Do you ship to Canada? | RAG | 1 | faq3 | Grounding | – | – | Good. | 1.32 |
| Do you ship to Canada? | RAG | 2 | faq3, faq8 | Completeness | Grounding | partial | Use good context | 1.96 |
| Do you ship to Canada? | RAG | 3 | faq3, faq8, faq6 | Traceability | Relevance | irrelevant | Add wrong context. | 1.89 |
| Do you ship to Canada? | RAG | 4 | Traceability | Grounding | verbose | Ad wrong context. | 2.44 |
| What are the support hours? | RAG | 1 | faq7 | Grounding | – | – | Concise. | 2.38 |
| What are the support hours? | RAG | 2 | Traceability | Relevance | irrelevant | Adds wrong context. | 1.66 |
| What are the support hours? | RAG | 3 | Completeness | Brevity | partial | Good. | 2.23 |
| What are the support hours? | RAG | 4 | Traceability | Relevance | irrelevant | Adds mwrong context. | 2.44 |
| Can I pay with Bitcoin? | RAG | 1 | faq5 | Grounding | Brevity | verbose | Reapeatable. | 2.63 |
| Can I pay with Bitcoin? | RAG | 2 | faq5, faq3 | Grounding | Brevity | verbose | Good. | 2.90 |
| Can I pay with Bitcoin? | RAG | 3 | faq5, faq3, faq6 | Grounding | Brevity | verbose | Good. | 3.51 |
| Can I pay with Bitcoin? | RAG | 4 | faq5, faq3, faq6, faq4 | Grounding | Brevity | verbose | Good. | 3.00 |
| How can I return a product? | raw | – | – | Completeness | Grounding | hallucination | It invents the process. | 23.87 |
| What's the process for tracking my package? | raw | – | – | Completeness | Brevity | verbose | Generic. | 14.65 |
| Do you ship to Canada? | raw | – | – | Relevance | Grounding | partial | Generic. | 6.36 |
| What are the support hours? | raw | – | – | Completeness | Grounding | stale | Invents process. | 5.80 |
| Can I pay with Bitcoin? | raw | – | – | Completeness | Grounding | partial | Creates another policies. | 6.40 |
