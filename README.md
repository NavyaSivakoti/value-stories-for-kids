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
app.py                Flask routes and the request flow
config.py             Loads all settings from the environment
validation.py         Input validation for age, value, and name
generator.py          Ties validation, the prompt, and the model together
llm_client.py         Multi-provider model client over REST
system_prompt.txt     The system prompt that shapes every story
templates/            The HTML page
static/               Styles
promptfooconfig.yaml  PromptFoo evaluation config
requirements.txt      Python dependencies
.env.example          Template for the environment settings
```

## Testing and evaluation

Quality is a deliberate focus of this project, and the testing work is being built in stages:

- Unit tests with pytest for the input validation logic
- Prompt evaluation with PromptFoo, checking each story against rules and running across all three providers
- Red teaming for prompt injection, leakage, and unsafe content
- A CI pipeline to run the checks automatically

To run the prompt evaluation:

```bash
promptfoo eval
promptfoo view
```

This section will be updated as each part is completed.

## Status

The app is built and working. The testing, evaluation, and deployment work is in progress.
