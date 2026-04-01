from flask import Flask, render_template, request
import hashlib
import os

# 🔥 Flask app init (IMPORTANT)
app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔐 SHA-256 Hash function
def generate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# 🧠 Main route
@app.route("/", methods=["GET", "POST"])
def index():
    generated_hash = ""
    result = "Awaiting verification..."
    filename = "No file selected"

    if request.method == "POST":
        file = request.files.get("file")
        user_hash = request.form.get("original_hash")
        action = request.form.get("action")

        if file and file.filename != "":
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            filename = file.filename

            # 🔥 Generate hash (once)
            generated_hash = generate_hash(file_path)

            if action == "generate":
                result = "✔ Hash Generated"

            elif action == "verify":
                if not user_hash:
                    result = "⚠ Enter original hash"
                else:
                    # 🔥 Correct comparison
                    if generated_hash.strip().lower() == user_hash.strip().lower():
                        result = "✔ File Not Modified"
                    else:
                        result = "❌ File Modified"

        else:
            result = "⚠ Please upload a file"

    return render_template(
        "index.html",
        generated_hash=generated_hash,
        result=result,
        filename=filename
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))