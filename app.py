from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Disc, Company
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import os

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///discsAPI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'b3h4g5')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/api/discs")
def get_discs():
    """ Return all the discs in the directory"""

    discs = Disc.query.all()
    ser_discs = []
    for disc in discs:
        s_disc = disc.serialize()
        ser_discs.append(s_disc)
    data = {"discs": ser_discs}
    return (jsonify(data), 200)

@app.route("/api/discs/name")
def search_discs():
    """ Return all discs that match the name. Many discs have the same name but a different plastic, or a slight variation to the name """

    if request.get_json(silent=True) == None:
        data = {"Error": "Please specify disc_name as the key and a disc name as the value"}
        return (jsonify(data), 404)
    
    args = request.get_json()
    disc_name = args.get('disc_name')

    if disc_name == None:
        data = {"Error": "disc_name was not passed, or was mispelled"}
        return (jsonify(data), 404)

    discs = Disc.query.filter(Disc.name.like(f"%{disc_name.lower()}%")).all()

    if len(discs) == 0:
        data = {"Error": "Sorry but no discs similiar to this spelling were found. Please check your spelling and try again"}
        return (jsonify(data), 404)

    ser_discs = []
    for disc in discs:
        s_disc = disc.serialize()
        ser_discs.append(s_disc)

    data = {"discs": ser_discs}
    return (jsonify(data), 200)

@app.route("/api/discs/filter")
def filter_discs():
    """ Return a list of discs based on search parameters """

    if request.get_json(silent=True) == None:
        data = {"Error": "Please specify a filter parameter and a value"}
        return (jsonify(data), 404)

    filters = {k:v for k,v in request.get_json().items()}

    try:
        discs = (Disc.query.filter_by(**filters).all())
    except InvalidRequestError:
        data = {"Error": "The filter parameter was spelled incorrectly, or is not a valid parameter"}
        return (jsonify(data), 404)

    if len(discs) == 0:
        data = {"Error": "The filter value returned no results. Make sure to double check spelling"}
        return (jsonify(data), 404)
    
    ser_discs = []
    for disc in discs:
        s_disc = disc.serialize()
        ser_discs.append(s_disc)

    data = {"discs": ser_discs}
    return (jsonify(data), 200)


@app.route("/api/companies")
def get_companies():
    """ Return all the companies in the directory """

    companies = Company.query.all()
    ser_companies = []

    for c in companies:
        s_company = c.serialize()
        ser_companies.append(s_company)

    data = {"Companies": ser_companies}
    return (jsonify(data), 200)


@app.route("/api/companies/<company_name>")
def get_disc(company_name):
    """Return all the discs from a company"""

    discs = Disc.query.filter(Disc.company_name.ilike(company_name.lower())).all()
    ser_discs = []

    if len(discs) == 0:
        data = {"Error": "Sorry but this company was not found. Check your spelling and try again"}
        return (jsonify(data), 404)

    for disc in discs:
        s_disc = disc.serialize()
        ser_discs.append(s_disc)

    data = {"Company": company_name, "Discs": ser_discs}
    return (jsonify(data), 200)
