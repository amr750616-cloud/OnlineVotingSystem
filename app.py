from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "online-voting-secret-key"


# -----------------------------
# DEMO DATA
# -----------------------------

voters = {
    "V1001": {
        "password": "1234",
        "name": "Arun",
        "has_voted": False
    },
    "V1002": {
        "password": "1234",
        "name": "Rahul",
        "has_voted": False
    },
    "V1003": {
        "password": "1234",
        "name": "Anu",
        "has_voted": False
    }
}


admin = {
    "username": "admin",
    "password": "admin123"
}


candidates = {
    "Candidate A": {
        "party": "Party A",
        "votes": 0
    },
    "Candidate B": {
        "party": "Party B",
        "votes": 0
    },
    "Candidate C": {
        "party": "Party C",
        "votes": 0
    }
}


# -----------------------------
# HOME
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# VOTER LOGIN
# -----------------------------

@app.route("/voter-login", methods=["GET", "POST"])
def voter_login():

    if request.method == "POST":

        voter_id = request.form.get("voter_id")
        password = request.form.get("password")

        if voter_id in voters and voters[voter_id]["password"] == password:

            session["voter_id"] = voter_id
            session["voter_logged_in"] = True

            return redirect(url_for("voter_dashboard"))

        return render_template(
            "voter_login.html",
            error="Invalid Voter ID or Password"
        )

    return render_template("voter_login.html")


# -----------------------------
# VOTER DASHBOARD
# -----------------------------

@app.route("/voter-dashboard")
def voter_dashboard():

    if not session.get("voter_logged_in"):
        return redirect(url_for("voter_login"))

    voter_id = session["voter_id"]
    voter = voters[voter_id]

    return render_template(
        "voter_dashboard.html",
        voter=voter
    )


# -----------------------------
# VOTE PAGE
# -----------------------------

@app.route("/vote", methods=["GET", "POST"])
def vote():

    if not session.get("voter_logged_in"):
        return redirect(url_for("voter_login"))

    voter_id = session["voter_id"]

    # Prevent voting twice
    if voters[voter_id]["has_voted"]:
        return render_template(
            "vote.html",
            candidates=candidates,
            already_voted=True
        )

    if request.method == "POST":

        selected_candidate = request.form.get("candidate")

        if selected_candidate in candidates:

            candidates[selected_candidate]["votes"] += 1

            voters[voter_id]["has_voted"] = True

            return redirect(url_for("results"))

    return render_template(
        "vote.html",
        candidates=candidates,
        already_voted=False
    )


# -----------------------------
# RESULTS
# -----------------------------

@app.route("/results")
def results():

    total_votes = sum(
        candidate["votes"]
        for candidate in candidates.values()
    )

    return render_template(
        "results.html",
        candidates=candidates,
        total_votes=total_votes
    )


# -----------------------------
# ADMIN LOGIN
# -----------------------------

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == admin["username"]
            and password == admin["password"]
        ):

            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid Admin Username or Password"
        )

    return render_template("admin_login.html")


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------

@app.route("/admin-dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    total_votes = sum(
        candidate["votes"]
        for candidate in candidates.values()
    )

    return render_template(
        "admin_dashboard.html",
        candidates=candidates,
        voters=voters,
        total_votes=total_votes
    )


# -----------------------------
# LOGOUT
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)