from cs50 import SQL
from flask import Flask, g, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import login_required, apology

app = Flask(__name__)

db = SQL("sqlite:///npc_gen.db")

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
    age = db.execute("SELECT * FROM age_category;")
    alignments = db.execute("SELECT * FROM alignments;")
    attitudes = db.execute("SELECT * FROM attitudes;")
    bodyshape = db.execute("SELECT * FROM bodyshape;")
    classes = db.execute("SELECT * FROM classes;")
    environments = db.execute("SELECT id, environment FROM environments;")
    gender = db.execute("SELECT * FROM gender;")
    looks = db.execute("SELECT * FROM looks;")
    quirk_category = db.execute("SELECT * FROM quirk_category;")
    regions = db.execute("SELECT id, region FROM regions;")
    professions = db.execute("SELECT * FROM professions;")
    prof_category = db.execute("SELECT * FROM profession_category;")
    social_classes = db.execute("SELECT id, social FROM social_classes;")
    species = db.execute("SELECT * FROM species;")
    styles = db.execute("SELECT * FROM styles;")
    talent_category = db.execute("SELECT * FROM talent_category;")
    trait_category = db.execute("SELECT * FROM trait_category;")
    

    return render_template(
        "index.html", alignments=alignments, age=age, attitudes=attitudes, bodyshape=bodyshape, classes=classes, environments=environments,
        gender=gender, looks=looks, professions=professions, prof_category=prof_category, quirk_category=quirk_category, regions=regions, 
        social_classes=social_classes, species=species, styles=styles, talent_category=talent_category, trait_category=trait_category
        )

# AI
@app.route("/api/quirks")
@login_required
def api_quirks():
    rows = db.execute("SELECT * FROM quirks")
    return jsonify([dict(row) for row in rows])

@app.route("/api/talents")
@login_required
def api_talents():
    rows = db.execute("SELECT * FROM talents")
    return jsonify([dict(row) for row in rows])

@app.route("/api/traits")
@login_required
def api_traits():
    rows = db.execute("SELECT * FROM traits")
    return jsonify([dict(row) for row in rows])

@app.route("/api/regions")
@login_required
def api_regions():
    rows = db.execute("SELECT * FROM regions")
    return jsonify([dict(row) for row in rows])

@app.route("/api/environments")
@login_required
def api_environments():
    rows = db.execute("SELECT * FROM environments")
    return jsonify([dict(row) for row in rows])

@app.route("/api/socials")
@login_required
def api_socials():
    rows = db.execute("SELECT * FROM social_classes")
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
            db.execute("""INSERT INTO npc (user_id, name, age_id, alignment_id, attitude_id, 
                   bodyshape_id, class_id, environment_id, gender_id, look_id, profession_id,
                   quirk_id, race_id, region_id, social_id, style_id, talent_id, trait1_id, 
                   trait2_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                   user, npc["name"], npc["age"], npc["alignment"], npc["Attitude"], npc["bodyshape"],
                   npc["class"], npc["environment"], npc["gender"], npc["look"], npc["prof"],
                   npc["quirk"], npc["race"], npc["region"], npc["social"], npc["Style"], npc["talent"],
                   npc["trait1"], npc["trait2"])
        except KeyError:
            return apology("key error", 400)
        except TypeError:
            return apology("type error", 400)
        except ValueError:
            return apology("value error", 400)
        except RuntimeError:
            return apology("runtime error", 400)



        
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
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
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

@app.route("/options")
@login_required
def content():
    quirks = db.execute(
        """SELECT quirks.id, quirks.content, quirks.category_id, quirk_category.name 
        FROM quirks JOIN quirk_category ON quirks.category_id = quirk_category.id 
        ORDER BY quirks.category_id;""")

    return redirect("/")

@app.route("/overview")
@login_required
def overview():
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
                      WHERE user_id = ?""", user)


if __name__ == "__main__":
    app.run(debug=True)
