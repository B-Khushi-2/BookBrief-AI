from flask import Flask, render_template, request, jsonify, Response, session
from werkzeug.utils import secure_filename
import os, pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "txt"}

INPUT_FOLDER_ID = "1N2y2DZj8dM07KeqkR1-rFRFLTuorvNz-"
OUTPUT_FOLDER_ID = "1qsduFkWcwDuvstkK79g-Y3Z1xsMFvG_0"

SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRET_FILE = "client_secret.json"

drive_service = None


def get_drive_service():
    global drive_service
    if drive_service:
        return drive_service

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    drive_service = build("drive", "v3", credentials=creds)
    return drive_service


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_to_drive(path, filename):
    service = get_drive_service()
    service.files().create(
        body={"name": filename, "parents": [INPUT_FOLDER_ID]},
        media_body=MediaFileUpload(path),
        supportsAllDrives=True
    ).execute()


def fetch_summary(expected_name):
    if not expected_name:
        return None

    service = get_drive_service()

    results = service.files().list(
        q=f"name = '{expected_name}'",
        fields="files(id,name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()

    files = results.get("files", [])
    if not files:
        return None

    file_id = files[0]["id"]
    content = service.files().get_media(fileId=file_id).execute().decode("utf-8")
    return content


@app.route("/")
def index():
    if "history" not in session:
        session["history"] = []
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "error"})

    filename = secure_filename(file.filename)
    base = filename.rsplit(".", 1)[0]

    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    upload_to_drive(path, filename)
    os.remove(path)

    session["current_file"] = base + "_summary.txt"

    return jsonify({"status": "success"})


@app.route("/get_summary")
def get_summary_api():
    expected = session.get("current_file")
    summary = fetch_summary(expected)

    history = session.get("history", [])

    if summary and expected:
        if not any(h["name"] == expected for h in history):
            history.insert(0, {"name": expected, "content": summary})
            session["history"] = history

    return jsonify({
        "status": "ready" if summary else "processing",
        "summary": summary,
        "filename": expected,
        "history": history
    })


@app.route("/download_current", methods=["POST"])
def download_current():
    data = request.json

    summary = data.get("content")
    filename = data.get("filename")

    if not summary:
        return "No content", 400   # ✅ prevents empty file

    return Response(
        summary,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )


@app.route("/download/<filename>")
def download(filename):
    for item in session.get("history", []):
        if item["name"] == filename:
            return Response(
                item["content"],
                mimetype="text/plain",
                headers={"Content-Disposition": f"attachment;filename={filename}"}
            )
    return "Not found"


@app.route("/delete_history", methods=["POST"])
def delete_history():
    index = int(request.json.get("index"))
    history = session.get("history", [])

    if 0 <= index < len(history):
        history.pop(index)

    session["history"] = history
    return jsonify({"status": "deleted"})


@app.route("/delete_all_history", methods=["POST"])
def delete_all_history():
    session["history"] = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True)