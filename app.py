# app.py
from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-federal-key-2024'

def build_dork(name=None, username=None, email=None, site_filter=None):
    terms = []
    if name:
        terms.append(f'"{name}"')
    if username:
        terms.append(f'"{username}"')
    if email:
        terms.append(f'"{email}"')

    if not terms:
        return None, None

    # Build query parts
    query_parts = []

    # Add site filter if provided
    if site_filter and site_filter.strip():
        clean_site = site_filter.strip().removeprefix("site:").strip()
        if clean_site:
            query_parts.append(f"site:{clean_site}")

    # Add personal data OR group
    query_parts.append("(" + " OR ".join(terms) + ")")

    # Add file type filters
    query_parts.append("(filetype:pdf OR filetype:docx OR filetype:csv OR filetype:txt)")

    full_query = " ".join(query_parts)

    # URL-encode for Google
    encoded = urllib.parse.quote(full_query)
    google_url = f"https://www.google.com/search?q={encoded}"

    return full_query, google_url

@app.route("/", methods=["GET", "POST"])
def index():
    dork_query = None
    dork_url = None
    data = {
        "name": "",
        "username": "",
        "email": "",
        "site_filter": ""
    }

    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "username": request.form.get("username", "").strip(),
            "email": request.form.get("email", "").strip(),
            "site_filter": request.form.get("site_filter", "").strip()
        }
        dork_query, dork_url = build_dork(
            name=data["name"],
            username=data["username"],
            email=data["email"],
            site_filter=data["site_filter"]
        )

    return render_template("index.html", dork_query=dork_query, dork_url=dork_url, data=data)

# --- RUN ON PORT 5000 ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)