import base64
import pickle
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "tryhackme-integrity-lab"

BASE_DIR = Path(__file__).resolve().parent
FLAG_PATH = BASE_DIR / "flag.txt"


def read_flag() -> str:
    if FLAG_PATH.exists():
        return FLAG_PATH.read_text(encoding="utf-8").strip()
    return "THM{INSECURE_DESERIALIZATION}"


LAB_INFO = {
    "title": "Integrity Lab: Insecure Deserialization",
    "tagline": "Accepting untrusted serialized data without verification leads to code execution.",
    "explanation": (
        "This application accepts serialized Python objects (pickle format) and deserializes them "
        "without verifying their integrity or authenticity. Attackers can craft malicious pickle payloads "
        "to execute arbitrary code and access sensitive files."
    ),
}


def insecure_deserialize(pickle_data: str) -> tuple[str, str]:
    """
    Intentionally insecure deserialization - DO NOT use in production!
    Accepts base64-encoded pickle data and deserializes it without verification.
    """
    try:
        decoded = base64.b64decode(pickle_data)
        obj = pickle.loads(decoded)
        return str(obj), ""
    except Exception as e:
        return "", f"Deserialization error: {type(e).__name__}: {e}"


@app.route("/", methods=["GET", "POST"])
def index():
    pickle_input = ""
    deserialized_output = ""
    error_message = ""

    if request.method == "POST":
        pickle_input = request.form.get("pickle_data", "").strip()
        if pickle_input:
            deserialized_output, error_message = insecure_deserialize(pickle_input)

    return render_template(
        "index.html",
        lab=LAB_INFO,
        pickle_input=pickle_input,
        deserialized_output=deserialized_output,
        error_message=error_message,
        flag_path=str(FLAG_PATH.name),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
