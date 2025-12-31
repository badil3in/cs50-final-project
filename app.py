import os
import sqlite3
import requests

from datetime import datetime
from flask import Flask, g, redirect, render_template, request, session, jsonify, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import login_required, apology, isInteger

app = Flask(__name__)

# AI
# setzt den DB‑Pfad relativ zum Dateistandort deiner App
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "npc_gen.db")

# adapted from AI copilot 
# savedir depending on environment
if os.environ.get("WEBSITE_SITE_NAME"): # Azure 
    IMAGE_DIR = "/home/images" 
else: 
    IMAGE_DIR = "static/images" # local

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def promptBuilder(npc):
    # get literals for IDs from db
    print("npc promptBuilder: ", npc)
    db = get_db()
    rows = db.execute("""
                      SELECT age_category.age, attitudes.attitude,
                      attitudes.attitude_desc, bodyshape.bodyshape, bodyshape.body_desc,
                      classes.class, environments.environment, environments.env_desc, gender.gender,
                      looks.look, looks.look_desc, professions.profession, regions.region, 
                      regions.region_desc, social_classes.social, social_classes.social_desc, species.race, 
                      species.race_desc,
                      styles.style, styles.style_desc
                      FROM age_category
                      JOIN attitudes ON attitudes.id = ?
                      JOIN bodyshape ON bodyshape.id = ?
                      JOIN classes ON classes.id = ?
                      JOIN environments ON environments.id = ?
                      JOIN gender ON gender.id = ?
                      JOIN looks ON looks.id = ?
                      JOIN professions ON professions.id = ?
                      JOIN regions ON regions.id = ?
                      JOIN social_classes ON social_classes.id = ?
                      JOIN species ON species.id = ?
                      JOIN styles ON styles.id = ?
                      JOIN traits ON traits.id = ?
                      JOIN traits AS traits2 ON traits2.id = ?
                      WHERE age_category.id = ?""", 
                      (npc["Attitude"], npc["bodyshape"], npc["class"], npc["environment"], npc["gender"],
                      npc["look"], npc["prof"], npc["region"], npc["social"], npc["race"], npc["Style"],
                      npc["trait1"], npc["trait2"],
                      npc["age"])).fetchall()
    print("rows: ", npc["name"])

    if npc["gender"] == 1:
        pronoun = "She"
    else:
        pronoun = "He"

    print("pronoun: ", pronoun)
    # TODO hair, skin and uniqueFacials conditional
    prompt = (f"A realistic fantasy portrait illustration with detailed textures and cinematic lighting of {npc["name"]},"
            f" who is a {rows[0]["gender"].lower()} {rows[0]["race"].lower()} - a {rows[0]["race_desc"]}. {pronoun}"
            f" is a {rows[0]["age"].lower()} professional {rows[0]["profession"].lower()}. Appearance: {pronoun}")
    # print("prompt 1: ", prompt)

    if npc["hair"] != "None" and npc["hair"] != "bald":
        prompt += f" has {npc["hair"]} hair,"
    elif npc["hair"] == "bald":
        prompt += f" is {npc["hair"],}"

    if npc["skin"] != "None":
        prompt += f" has {npc["skin"]} skin," 

    if npc["uniqueFacials"] != "None":
        prompt += f" has {npc["uniqueFacials"]},"

    prompt +=   (f" has a {rows[0]["bodyshape"].lower()} bodyshape for a {rows[0]["race"].lower()} -"
                f" {rows[0]["body_desc"]}. {pronoun} has a {rows[0]["look"].lower()} look - {rows[0]["look_desc"]}." 
                f" {pronoun} emanates a {rows[0]["attitude"].lower()} attitude - {rows[0]["attitude_desc"].lower()}."
                f" Dress style: {rows[0]["style"].lower()}, {rows[0]["style_desc"].lower()} with faint"
                f" influences of their {rows[0]["environment"].lower()} and {rows[0]["social"].lower()} origin.")
    
    print("prompt: ", prompt)
    return (prompt)
    
# AI adapted
def call_image_api(prompt):
    # metadaten
    API_KEY = os.getenv("API_KEY_OPEN_AI")
    API_URL = "https://api.openai.com/v1/images/generations"

    # API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        # check if error ocurred during request by requests method raise_for_status
        response.raise_for_status() 
        data = response.json()
        # print("data: ", data)

    except requests.exceptions.HTTPError as e:
        # print("HTTPError: ", e, 
        #       "message: ", response.json()["error"]["message"])
        message = response.json()["error"]["message"]
        return message
    except requests.exceptions.RequestException as e:
        # print("RequestException: ", e,
        #     "message: ", response.json()["error"]["message"])
        message = response.json()["error"]["message"]
        return message

    # print("response: ", response.status_code)
    # print("data: ", data)
    return data

# AI code
# with this decoration flask closes DB connection automaticaly 
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# from cs50 problemset 
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/creation")
@login_required
def creation():
    db = get_db()

    # db queries for creation form
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
        "creation.html", alignments=alignments, age=age, attitudes=attitudes, bodyshape=bodyshape, classes=classes, environments=environments,
        gender=gender, looks=looks, professions=professions, prof_category=prof_category, quirk_category=quirk_category, regions=regions, 
        social_classes=social_classes, species=species, styles=styles, talent_category=talent_category, trait_category=trait_category
        )

# adapted from AI
# load image from server directory
@app.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

# get quirks from db
@app.route("/api/quirks")
@login_required
def api_quirks():
    # adapted from AI
    db = get_db()
    rows = db.execute("SELECT * FROM quirks").fetchall()
    return jsonify([dict(row) for row in rows])

# get talents from db
@app.route("/api/talents")
@login_required
def api_talents():
    db = get_db()
    rows = db.execute("SELECT * FROM talents").fetchall()
    return jsonify([dict(row) for row in rows])

# get traits from db
@app.route("/api/traits")
@login_required
def api_traits():
    db = get_db()
    rows = db.execute("SELECT * FROM traits").fetchall()
    return jsonify([dict(row) for row in rows])

# get regions from db
@app.route("/api/regions")
@login_required
def api_regions():
    db = get_db()
    rows = db.execute("SELECT * FROM regions").fetchall()
    return jsonify([dict(row) for row in rows])

# get environments from db
@app.route("/api/environments")
@login_required
def api_environments():
    db = get_db()
    rows = db.execute("SELECT * FROM environments").fetchall()
    return jsonify([dict(row) for row in rows])

# get socials from db
@app.route("/api/socials")
@login_required
def api_socials():
    db = get_db()
    rows = db.execute("SELECT * FROM social_classes").fetchall()
    print("JSON socials: ", jsonify([dict(row) for row in rows]))
    return jsonify([dict(row) for row in rows])

# save NPC
@app.route("/api/save_npc", methods=["POST"])
@login_required
def api_savenpc():
    print("Route reached")
    if request.method == "POST":
        user = session.get("user_id")
        npc = request.get_json()
        # print("npc: ", npc)
        if not npc:
            return apology("no data", 400)
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""INSERT INTO npc (
                       user_id, name, age_id, alignment_id, attitude_id, bodyshape_id, 
                       class_id, environment_id, gender_id, look_id, profession_id,
                       quirk_id, race_id, region_id, social_id, style_id, talent_id, trait1_id, 
                       trait2_id
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", 
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
                    npc["trait2"])).fetchall()
            npc_id = cursor.lastrowid
            print("npc_id: ", npc_id)
            db.commit() # nur bei Änderungen in der DB
            print("npc: ", npc)

            # save image
            if(npc.get("image")):
                print("if reached")

                # dynamic filename 
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{user}_{npc_id}_{timestamp}.png"

                # line adapted from AI copilot 
                # create dir if not exists
                os.makedirs(IMAGE_DIR, exist_ok=True) 

                # line adapted from AI copilot 
                # assemble filpath
                filepath = os.path.join(IMAGE_DIR, filename)
                
                # get image from frontend
                response = requests.get(npc["image"])
                response.status_code

                # save image
                with open(filepath, mode="wb") as file:
                    file.write(response.content)

                # path for db (without main dir)
                filepath_save = "/images/" + filename

                # add path to db
                db.execute("UPDATE npc SET image = ? WHERE user_id = ? AND id = ?;", (filepath_save, user, npc_id)).fetchall()
                db.commit()
            else:
                print("else reached")

        # TODO complete errorhandling
        except KeyError as e:
            # print("Key Error:", e)
            return apology("SQL Lite Error", 500)          
        except sqlite3.Error as e:
            # print("SQL Lite error:", e)
            return apology("SQL Lite Error", 500)
    print("return reached")
    # return response for JS 
    return jsonify({
        "Status": "success",
        "redirect": "/overview"
    })

# delete NPC
@app.route("/api/delete_npc", methods=["POST"])
@login_required
def delete():
    if request.method == "POST":
        try:
            id = request.get_json()["id"]
            print("id (delete): ", id)

            if(isInteger(id)):
                user = session.get("user_id")
                db = get_db()
                db.execute("DELETE FROM npc WHERE user_id = ? AND id = ?", (user, id)).fetchall()
                db.commit()

            return jsonify({
                "Status": "success",
                "redirect": "/overview"
            })
        # TODO complete errorhandling
        except TypeError as e:
            print("delete - TypeError: ", e,
                  "id: ", id)
            return
        except KeyError as e:
            print("delete - KeyError: ", e)
            return


# image generator - using prompt generator + API request
@app.route("/generate_image", methods=["POST"])
@login_required
def generate_image():

    # adapted from AI 
    if request.method == "POST":
        try:
            # get data from frontend
            npc = request.get_json()
            # print("npc: ", npc)

            # generate prompt
            prompt = promptBuilder(npc) 

            # API request to create image
            image = call_image_api(prompt)
            
            # return json with url 
            return jsonify({
            # adapted AI line
            "src": f"{image['data'][0]['url']}"})

        # TODO complete errorhandling
        except TypeError as e:
            print("gen_img - TypeError: ", e,
                  "image: ", image)
            return 
        except AttributeError as e:
            print("gen_img - AttributeError: ", e)
            return 
        except KeyError as e:
            print("gen_img - KeyError: ", e)
            return 


# from cs50 problemset
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
            # TODO complete errorhandling
            return apology("must provide username", 400)

        # # Ensure password was submitted
        elif not request.form.get("password"):
            # TODO complete errorhandling
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        ).fetchall()
        # print("rows: ", rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            # TODO complete errorhandling
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
# from cs50 problemset
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# list of all NPCs created
@app.route("/overview")
@login_required
def overview():
    # query parameter for previous deletion
    deleted = request.args.get("deletion")

    db = get_db()
    user = session.get("user_id")
    rows = db.execute("""
                      SELECT npc.id, npc.name, npc.image, age_category.age, alignments.alignment, attitudes.attitude,
                      attitudes.attitude_desc, bodyshape.bodyshape, bodyshape.body_desc,
                      classes.class, environments.environment, environments.env_desc, gender.gender,
                      looks.look, looks.look_desc, professions.profession, quirks.quirk, regions.region, 
                      regions.region_desc, social_classes.social, social_classes.social_desc, species.race, 
                      styles.style, styles.style_desc, talents.talent, traits.trait AS trait1, 
                      traits.trait_desc AS trait1_desc, traits2.trait AS trait2, traits2.trait_desc AS trait2_desc
                      FROM npc
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
                      JOIN traits AS traits2 ON traits2.id = npc.trait2_id
                      WHERE user_id = ?""", 
                      (user,)).fetchall()
    return render_template("overview.html", data=rows, deletion_success=bool(deleted)) # adapted bool() from AI

if __name__ == "__main__":
    app.run(debug=True)
