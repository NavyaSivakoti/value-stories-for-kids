"""Value Stories for Kids Flask application.

A small web app that collects a child's first name, age, and a value to
teach, then asks the configured model for a gentle, age-appropriate story.
"""
from datetime import date

from flask import Flask, render_template, request, session

import config
import validation
from generator import create_story
from llm_client import LLMError

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY


def _stories_used_today():
    """Return how many stories this visitor has generated today."""
    today = date.today().isoformat()
    record = session.get("story_count", {})
    if record.get("date") != today:
        return 0
    return record.get("count", 0)


def _record_story():
    """Increment this visitor's story count for today."""
    today = date.today().isoformat()
    record = session.get("story_count", {})
    if record.get("date") != today:
        record = {"date": today, "count": 0}
    record["count"] = record.get("count", 0) + 1
    session["story_count"] = record


@app.route("/", methods=["GET", "POST"])
def index():
    story = None
    error = None
    form = {"name": "", "age": "", "value": ""}

    if request.method == "POST":
        form["name"] = request.form.get("name", "")
        form["age"] = request.form.get("age", "")
        form["value"] = request.form.get("value", "")

        if _stories_used_today() >= config.DAILY_STORY_LIMIT:
            error = (
                "You have reached today's free story limit. "
                "Please come back tomorrow."
            )
        else:
            try:
                story = create_story(
                    form["name"], form["age"], form["value"]
                )
                _record_story()
            except validation.ValidationError as exc:
                error = str(exc)
            except LLMError:
                error = (
                    "A story could not be written just now. "
                    "Please try again in a moment."
                )

    return render_template(
        "index.html",
        story=story,
        error=error,
        form=form,
        values=validation.VALUE_MEANINGS,
        stories_left=max(
            0, config.DAILY_STORY_LIMIT - _stories_used_today()
        ),
    )


@app.route("/health")
def health():
    """Lightweight health check for post-deployment monitoring."""
    return {"status": "ok", "provider": config.ACTIVE_PROVIDER}


if __name__ == "__main__":
    app.run(debug=True)
