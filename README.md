# PhraseCraft

A multilingual grammar coach built with Streamlit and the OpenAI API. Enter a sentence in
any language and it detects the language, corrects it, and explains each mistake — in the
language you were writing in, not in English.

![PhraseCraft](chatbot.png)

## What it does

Submit a sentence to the Grammar Checker and you get back:

- **The detected language**, including `Mixed` for code-switched text and `Unclear` for
  input it can't classify
- **A corrected sentence**, or a confirmation when the input was already correct
- **Each mistake listed separately**, tagged by type — grammar, spelling, punctuation,
  word order, or vocabulary — showing the original fragment, the fix, and why it was wrong
- **Notes** on anything else worth flagging

Explanations come back in the detected language, so a Spanish learner reads the reasoning
in Spanish. The whole prompt is built around that.

## How it works

The hard part isn't calling the model — it's getting output you can actually render.
`prompts.py` constrains the model to a strict JSON schema and gives it an explicit
decision tree for the three cases that matter:

| Input | `status` | `corrected` |
|---|---|---|
| Already correct | `perfect` | `"Input Correct"` |
| Has mistakes | `imperfect` | the fixed sentence |
| Gibberish or undecipherable | `unclear` | `null` |

The prompt forbids guessing at corrections for unclear input, and is more lenient on very
short texts (1–7 words) where a single word is often fine as written.

`utils.py` chains prompt → model → parser with LangChain, strips code fences the model
sometimes adds, and returns an error payload instead of crashing when a response can't be
parsed or the API call fails.

Model: `gpt-4o-mini` at `temperature=0`.

## Setup

Requires Python 3.9+.

```bash
git clone https://github.com/pranavrjukanti/PhraseCraft.git
cd PhraseCraft
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

The app reads your API key from Streamlit secrets, which are gitignored. Create the file:

```bash
mkdir -p .streamlit
echo 'OPENAI_API_KEY = "sk-your-key-here"' > .streamlit/secrets.toml
```

Run it:

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Project structure

```
app.py              Streamlit entry point and sidebar navigation
grammarchecker.py   Grammar Checker page — input, results, error states
utils.py            LangChain chain, OpenAI call, JSON parsing
prompts.py          The grammar-checking prompt and its JSON schema
requirements.txt    Pinned dependencies
```

## Roadmap

Only the Grammar Checker is built so far. Still to come:

- [ ] Conversational practice mode
- [ ] Vocabulary building
- [ ] Progress tracking toward fluency milestones

## Built with

Python · Streamlit · OpenAI API · LangChain
