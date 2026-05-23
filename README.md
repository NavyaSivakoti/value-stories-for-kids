# Value Stories for Kids

A small web app that writes short, original stories to help a child grow a good value.

A caregiver chooses the child's first name (optional), age, and a value such as kindness, courage, or patience. The app then generates a gentle, age-appropriate story built around that value, written in a clear five-part shape and ending with a one-line takeaway.

## What it does

- Generates an original short story for a chosen value, for children ages 1 to 14.
- Draws on the spirit of timeless fables and folk tales, retold in fresh words.
- Matches the vocabulary and ideas to the child's age band.
- Personalises the story with the child's first name when one is given.
- Keeps content gentle, secular, and original: no violence, no scary themes, no branded characters.

## How it works

The app collects three inputs (name, age, value), validates them, builds a request, and sends it with a fixed system prompt to a language model. The model returns the story, which is shown in the browser.

The system prompt in `system_prompt.txt` is the heart of the product. It defines the story shape, the age handling, the safety rules, and the storytelling style.

The app can run on any one of three providers: Google Gemini, OpenAI, or Anthropic. The active provider is set with a single environment variable, so swapping the live model is a one-line change.

## Tech stack

- Python 3 and Flask
- Direct REST calls to each model provider, with no vendor SDKs
- python-dotenv for configuration
- pytest for unit tests
- PromptFoo for prompt evaluation

## Running it locally

1. Clone the repository and enter the folder.

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create your environment file:

   ```bash
   cp .env.example .env
   ```

   Open `.env`, add at least one provider API key, and set `VALUE_STORIES_PROVIDER` to that provider.

   Also set `FLASK_SECRET_KEY` to a long random string. It is not something you get from a provider, you generate it yourself. You can create one with:

   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

   Copy the printed value into `.env` as `FLASK_SECRET_KEY`.

5. Start the app:

   ```bash
   flask run
   ```

6. Open the local address shown in the terminal.

## Configuration

Every setting is read from environment variables, so secrets never live in the code. See `.env.example` for the full list. The main settings are:

- `VALUE_STORIES_PROVIDER`: which model powers the app (`gemini`, `openai`, or `anthropic`)
- the matching API key and model name for that provider
- `VALUE_STORIES_MAX_TOKENS`, `VALUE_STORIES_TEMPERATURE`, `VALUE_STORIES_DAILY_LIMIT`

The real `.env` file is never committed. It is listed in `.gitignore`.

## Project structure

```
app.py                     Flask routes and the request flow
config.py                  Loads all settings from the environment
validation.py              Input validation for age, value, and name
generator.py               Ties validation, the prompt, and the model together
llm_client.py              Multi-provider model client over REST
system_prompt.txt          The system prompt that shapes every story
templates/                 The HTML page
static/                    Styles
promptfooconfig.yaml        PromptFoo evaluation config and assertions
story_prompt.json          The chat-format prompt used by the evaluation
random_children_data.yaml  The test inputs (name, age, value) for the evaluation
EVAL_FINDINGS.md           A running log of issues found through evaluation
requirements.txt           Python dependencies
.env.example               Template for the environment settings
```

## Testing and evaluation

Quality is a deliberate focus of this project. The testing work is being built in stages:

- Prompt evaluation with PromptFoo: In progress. `promptfooconfig.yaml` runs every story through a suite of checks across all three providers. The checks mix deterministic rules (word count, the child's name, the closing lesson line) with model-graded rubrics for tone, age-fit, safety, and whether the value comes through.
- Unit tests with pytest for the input validation logic: Planned
- Red teaming for prompt injection, leakage, and unsafe content: Planned
- A CI pipeline to run the checks automatically: Planned

The evaluation inputs live in `random_children_data.yaml` and the chat prompt in `story_prompt.json`. Issues found through evaluation are recorded in `EVAL_FINDINGS.md`, so anyone reading the repo can see what the evals caught and what still needs fixing.

To run the prompt evaluation:

```bash
promptfoo eval
promptfoo view
```

Add `-o report.html` to the eval command to save a standalone HTML report.

## Status

The app is built and working. The PromptFoo evaluation suite, unit tests, red teaming, the CI pipeline, and deployment are still in progress.
