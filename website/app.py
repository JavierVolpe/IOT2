from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user
from plotter import plotter1,mapper
from databasehandler import fyld_henter, random_data, empty ,ild_check, vaelt_check, batteri_check, empty_ild_vealt_batt, random_data_ild_vealt_batt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"

db = SQLAlchemy()
 
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/info')
def info():
   return render_template('info.html')

@app.route("/Skralde Niveau", methods=['GET', 'POST'])
def skralde_niveau():
   if request.method == "POST":
      data = request.form.get('skrald')
      return render_template("skralde_niveau.html", rest_img=plotter1(data))
   else:
      return render_template("skralde_niveau.html")

@app.route("/Status", methods=['GET', 'POST'])
def skralde_status():
   if request.method == "POST":
      if request.form.get("Empty") == "empty":
         empty_ild_vealt_batt()
      elif request.form.get("Random") == "random":
         random_data_ild_vealt_batt()
   ild_txt = ""
   vaelt_txt = ""
   batteri_txt = ""
   ild = ild_check()
   vaelt = vaelt_check()
   batteri = batteri_check()
   if len(ild) > 0:
      for n in ild:
         ild_txt += n
   else:
      ild_txt = "<h3>Den er ikke gal her :)</h3>"
   if len(vaelt) > 0:
      for n in vaelt:
         vaelt_txt += n
   else:
      vaelt_txt = "<h3>Den er ikke gal her :)</h3>"
   if len(batteri) > 0:
      for n in batteri:
         batteri_txt += n
   else:
      batteri_txt = "<h3>Alle batterierne er over strøm grænsen.</h3>"
   return render_template("statusside.html", ild=ild_txt,vaelt=vaelt_txt,batteri=batteri_txt)

@app.route("/Ruteside", methods=['GET', 'POST'])
def ruteside():
   data = mapper("rest")
   if request.method == "POST":
      if request.form.get("Rest") == "rest":
         data=mapper("rest")
         return render_template("ruteside.html",data=data)
      elif request.form.get("Mad") == "mad":
         data=mapper("mad")
         return render_template("ruteside.html",data=data)
      elif request.form.get("Plast") == "plast":
         data=mapper("plast")
         return render_template("ruteside.html",data=data)
      elif request.form.get("Pap") == "pap":
         data=mapper("pap")
         return render_template("ruteside.html",data=data)
      else:
         return render_template("ruteside.html",data=data)
   return render_template("ruteside.html",data=data)

@app.route("/Afhent", methods=['GET', 'POST'])
def afhent():
   if request.method == "POST":
      if request.form.get("Empty") == "empty":
         empty()
      elif request.form.get("Random") == "random":
         random_data()
   rest = ""
   mad = ""
   plast = ""
   pap = ""
   if fyld_henter():
      y = ["""<li class="list-group-item">"""+ s + "</li>" for s in fyld_henter()]
      for n in y:
         if "Rest" in n:
            rest += n.replace("Rest","")
         if "Mad" in n:
            mad += n.replace("Mad","")
         if "Plast" in n:
            plast += n.replace("Plast","")
         if "Pap" in n:
            pap += n.replace("Pap","")
   if rest == "":
      rest = "<h3>Der er ikke noget af denne type skrald</h3>"
   if mad == "":
      mad = "<h3>Der er ikke noget af denne type skrald</h3>"
   if plast == "":
      plast = "<h3>Der er ikke noget af denne type skrald</h3>"
   if pap == "":
      pap = "<h3>Der er ikke noget af denne type skrald</h3>"
   return render_template("afhent.html",rest=rest, mad=mad, plast=plast, pap=pap)

@app.errorhandler(404)
def not_found(e):
   return render_template('404.html'), 404

app.run(debug=True, host='0.0.0.0', port=5000)