from flask import Flask, render_template, request, flash, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from services.validator import validate_file, sanitize_jd
from services.parser import extract_text
from services.analyzer import analyze

app = Flask(__name__)
app.config.from_object(Config)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per hour"],
    storage_uri="memory://",
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
@limiter.limit("10 per hour")
def analyze_resume():
    resume_file = request.files.get("resume")
    jd_text = request.form.get("jd_text", "").strip()

    # --- Validation ---
    errors = []
    try:
        validate_file(resume_file, Config.MAX_FILE_BYTES)
    except ValueError as e:
        errors.append(str(e))

    if not jd_text:
        errors.append("Job description cannot be empty.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("index"))

    # --- Parse & Sanitize ---
    try:
        resume_text = extract_text(resume_file, Config.MAX_TEXT_CHARS)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("index"))

    jd_clean = sanitize_jd(jd_text)

    # --- AI Analysis ---
    try:
        result = analyze(resume_text, jd_clean)
    except RuntimeError as e:
        flash(f"Analysis failed: {str(e)}", "error")
        return redirect(url_for("index"))

    return render_template("result.html", result=result)


@app.errorhandler(429)
def rate_limit_handler(e):
    flash("Too many requests. Please try again later.", "error")
    return redirect(url_for("index")), 429


@app.errorhandler(413)
def file_too_large(e):
    flash("Uploaded file is too large.", "error")
    return redirect(url_for("index")), 413


if __name__ == "__main__":
    app.run(debug=False)
