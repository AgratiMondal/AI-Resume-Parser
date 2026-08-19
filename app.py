from flask import Flask, render_template, request
import os
import uuid

from parser import parse_resume


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# ALLOWED FILES
# ============================================================

ALLOWED_EXTENSIONS = {
    "pdf"
}


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# UPLOAD RESUME
# ============================================================

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("resume")

    # --------------------------------------------------------
    # Check if file exists
    # --------------------------------------------------------

    if not file:

        return render_template(
            "index.html",
            error="Please select a resume."
        )


    # --------------------------------------------------------
    # Check filename
    # --------------------------------------------------------

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select a resume."
        )


    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    if not allowed_file(file.filename):

        return render_template(
            "index.html",
            error="Only PDF resume files are supported."
        )


    # --------------------------------------------------------
    # Create unique filename
    # --------------------------------------------------------

    original_name = file.filename

    extension = original_name.rsplit(".", 1)[1].lower()

    unique_filename = (
        f"resume_{uuid.uuid4().hex}.{extension}"
    )


    # --------------------------------------------------------
    # Create file path
    # --------------------------------------------------------

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )


    # --------------------------------------------------------
    # Save resume
    # --------------------------------------------------------

    try:

        file.save(file_path)

    except Exception as e:

        print("File save error:", e)

        return render_template(
            "index.html",
            error="Could not save the uploaded file."
        )


    # --------------------------------------------------------
    # Parse resume
    # --------------------------------------------------------

    try:

        result = parse_resume(file_path)

    except Exception as e:

        print("Resume parsing error:", e)

        return render_template(
            "index.html",
            error="Could not analyze this resume. Please make sure it is a valid PDF."
        )

    finally:

        # ----------------------------------------------------
        # Delete uploaded file after processing
        # ----------------------------------------------------

        try:

            if os.path.exists(file_path):

                os.remove(file_path)

        except Exception as e:

            print("File cleanup error:", e)


    # --------------------------------------------------------
    # Show results
    # --------------------------------------------------------

    return render_template(
        "results.html",
        result=result
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="File is too large. Maximum size is 10 MB."
    ), 413


@app.errorhandler(404)
def page_not_found(error):

    return """
    <h1>404</h1>
    <p>Page not found.</p>
    <a href="/">Go back to Resume Parser</a>
    """, 404


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )