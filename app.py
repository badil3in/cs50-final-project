import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import login_required, apology

app = Flask(__name__)

# AI
# setzt den DB‑Pfad relativ zum Dateistandort deiner App
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "npc_gen.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
# def get_db():
#     conn = sqlite3.connect("npc_gen.db")
#     conn.row_factory = sqlite3.Row
#     return conn

# AI
# flask schließt Verbindung automatisch wg. decorator 
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# db = SQL("sqlite:///npc_gen.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# print("hash: ", generate_password_hash("DPK?jxjH4G!kceTF"))

@app.route("/")
@login_required
def index():
    db = get_db()

    age = db.execute("SELECT * FROM age_category;").fetchall()
    alignments = db.execute("SELECT * FROM alignments;").fetchall()
    attitudes = db.execute("SELECT * FROM attitudes;").fetchall()
    bodyshape = db.execute("SELECT * FROM bodyshape;").fetchall()
    classes = db.execute("SELECT * FROM classes;").fetchall()
    environments = db.execute("SELECT id, environment FROM environments;").fetchall()
    gender = db.execute("SELECT * FROM gender;").fetchall()
    looks = db.execute("SELECT * FROM looks;").fetchall()
    quirk_category = db.execute("SELECT * FROM quirk_category;").fetchall()
    regions = db.execute("SELECT id, region FROM regions;").fetchall()
    professions = db.execute("SELECT * FROM professions;").fetchall()
    prof_category = db.execute("SELECT * FROM profession_category;").fetchall()
    social_classes = db.execute("SELECT id, social FROM social_classes;").fetchall()
    species = db.execute("SELECT * FROM species;").fetchall()
    styles = db.execute("SELECT * FROM styles;").fetchall()
    talent_category = db.execute("SELECT * FROM talent_category;").fetchall()
    trait_category = db.execute("SELECT * FROM trait_category;").fetchall()
    

    return render_template(
        "index.html", alignments=alignments, age=age, attitudes=attitudes, bodyshape=bodyshape, classes=classes, environments=environments,
        gender=gender, looks=looks, professions=professions, prof_category=prof_category, quirk_category=quirk_category, regions=regions, 
        social_classes=social_classes, species=species, styles=styles, talent_category=talent_category, trait_category=trait_category
        )

# AI
@app.route("/api/quirks")
@login_required
def api_quirks():
    db = get_db()

    rows = db.execute("SELECT * FROM quirks").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/talents")
@login_required
def api_talents():
    db = get_db()

    rows = db.execute("SELECT * FROM talents").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/traits")
@login_required
def api_traits():
    db = get_db()

    rows = db.execute("SELECT * FROM traits").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/regions")
@login_required
def api_regions():
    db = get_db()

    rows = db.execute("SELECT * FROM regions").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/environments")
@login_required
def api_environments():
    db = get_db()

    rows = db.execute("SELECT * FROM environments").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/socials")
@login_required
def api_socials():
    db = get_db()

    rows = db.execute("SELECT * FROM social_classes").fetchall()
    print("JSON socials: ", jsonify([dict(row) for row in rows]))
    return jsonify([dict(row) for row in rows])

@app.route("/api/save_npc", methods=["POST"])
@login_required
def api_savenpc():
    

    if request.method == "POST":
        user = session.get("user_id")
        npc = request.get_json()
        print("npc: ", npc)
        if not npc:
            return apology("no data", 400)
        try:
            db = get_db()
            db.execute("""INSERT INTO npc (
                       user_id, name, age_id, alignment_id, attitude_id, bodyshape_id, 
                       class_id, environment_id, gender_id, look_id, profession_id,
                       quirk_id, race_id, region_id, social_id, style_id, talent_id, trait1_id, 
                       trait2_id
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (user, 
                    npc["name"], 
                    npc["age"], 
                    npc["alignment"], 
                    npc["Attitude"], 
                    npc["bodyshape"],
                    npc["class"], 
                    npc["environment"], 
                    npc["gender"], 
                    npc["look"], 
                    npc["prof"],
                    npc["quirk"], 
                    npc["race"], 
                    npc["region"], 
                    npc["social"], 
                    npc["Style"], 
                    npc["talent"],
                    npc["trait1"], 
                    npc["trait2"]))
            db.commit() # nur bei Änderungen in der DB
        except KeyError as e:
            print("Key Error:", e)
            return apology("SQL Lite Error", 500)          
        except sqlite3.Error as e:
            print("SQL Lite error:", e)
            return apology("SQL Lite Error", 500)
        
    # return response for JS 
    return jsonify({
        "Status": "success",
        "redirect": "/overview"
    })

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    db = get_db()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        ).fetchall()
        print("rows: ", rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# @app.route("/options")
# @login_required
# def content():
#     db = get_db()

#     quirks = db.execute(
#         """SELECT quirks.id, quirks.content, quirks.category_id, quirk_category.name 
#         FROM quirks JOIN quirk_category ON quirks.category_id = quirk_category.id 
#         ORDER BY quirks.category_id;""").fetchall()

#     return redirect("/")

@app.route("/overview")
@login_required
def overview():
    db = get_db()

    user = session.get("user_id")
    rows = db.execute("""SELECT npc.name, age_category.age, alignments.alignment, attitudes.attitude,
                      attitudes.attitude_desc, bodyshape.bodyshape, bodyshape.body_desc,
                      classes.class, environments.environment, environments.env_desc, gender.gender,
                      looks.look, looks.look_desc, professions.profession, quirks.quirk, regions.region, 
                      regions.region_desc, social_classes.social, social_classes.social_desc, species.race, 
                      styles.style, styles.style_desc, talents.talent, traits.trait, traits.trait_desc 
                      FROM "npc"
                      JOIN age_category ON age_category.id = npc.age_id
                      JOIN alignments ON alignments.id = npc.alignment_id
                      JOIN attitudes ON attitudes.id = npc.attitude_id
                      JOIN bodyshape ON bodyshape.id = npc.bodyshape_id
                      JOIN classes ON classes.id = npc.class_id
                      JOIN environments ON environments.id = npc.environment_id
                      JOIN gender ON gender.id = npc.gender_id
                      JOIN looks ON looks.id = npc.look_id
                      JOIN professions ON professions.id = npc.profession_id
                      JOIN quirks ON quirks.id = npc.quirk_id
                      JOIN regions ON regions.id = npc.region_id
                      JOIN social_classes ON social_classes.id = npc.social_id
                      JOIN species ON species.id = npc.race_id
                      JOIN styles ON styles.id = npc.style_id
                      JOIN talents ON talents.id = npc.talent_id
                      JOIN traits ON traits.id = npc.trait1_id 
                      WHERE user_id = ?""", user,).fetchall()


if __name__ == "__main__":
    app.run(debug=True)
