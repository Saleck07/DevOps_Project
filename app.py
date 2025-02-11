from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    render_template,
    flash,
    get_flashed_messages,
)
from models import Intervenant, Intervention, Client, app, db
import matplotlib.pyplot as plt
import io
import base64

VALID_CREDENTIALS = {"admin": "admin"}

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    return response 

def get_graphe(data):
    labels = []
    donnes = []
    colors = ["#1f77b4", "#ff7f0e"]
    est_tout_none = 0
    for cle, valeur in data.items():
        labels.append(f"{cle} ({valeur})")
        if valeur == 0:
            est_tout_none += 1
        donnes.append(valeur)
    if est_tout_none == len(donnes):
        return 0
    if len(labels) > 2:
        colors.append("#2ca02c")
    plt.figure(figsize=(4, 4))
    plt.pie(donnes, labels=None, colors=colors, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    plt.legend(labels, fontsize=10, frameon=False, bbox_to_anchor=(0.5, 1.2))
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode("utf8")
    return img_base64


# @app.route("/")
# def home():
#     messages = get_flashed_messages()
#     if messages:
#         message = messages[0]
#     else:
#         message = "-1"
#     print(message)
#     if "user" not in session:
#         return redirect(url_for("login"))
#     dict_cli = Client.select_dict_cli()
#     dict_inter = Intervenant.select_dict_Inter()
#     all_intervenant = Intervenant.select_all_intervenants()
#     all_client = Client.select_all_clients()
#     all_interventions = Intervention.select_all_interventions()
#     image = get_graphe(Intervention.count_interventions_by_status())
#     return render_template(
#         "home.html",
#         dict_cli=dict_cli,
#         dict_inter=dict_inter,
#         clients=all_client,
#         intervenants=all_intervenant,
#         interventions=all_interventions,
#         image=image,
#         message=message,
#     )


# Nouveaux Foncions
@app.route("/intervenant")
def intervenant():
    messages = get_flashed_messages()
    if messages:
        message = messages[0]
    else:
        message = "-1"
    print(message)
    if "user" not in session:
        return redirect(url_for("login"))
    dict_cli = Client.select_dict_cli()
    dict_inter = Intervenant.select_dict_Inter()
    all_intervenant = Intervenant.select_all_intervenants()
    all_client = Client.select_all_clients()
    all_interventions = Intervention.select_all_interventions()
    image = get_graphe(Intervention.count_interventions_by_status())
    return render_template(
        "intervenants.html",
        dict_cli=dict_cli,
        dict_inter=dict_inter,
        clients=all_client,
        intervenants=all_intervenant,
        interventions=all_interventions,
        image=image,
        message=message,
    )


@app.route("/")
def client():
    messages = get_flashed_messages()
    if messages:
        message = messages[0]
    else:
        message = "-1"
    print(message)
    if "user" not in session:
        return redirect(url_for("login"))
    dict_cli = Client.select_dict_cli()
    dict_inter = Intervenant.select_dict_Inter()
    all_intervenant = Intervenant.select_all_intervenants()
    all_client = Client.select_all_clients()
    all_interventions = Intervention.select_all_interventions()
    image = get_graphe(Intervention.count_interventions_by_status())
    return render_template(
        "client.html",
        dict_cli=dict_cli,
        dict_inter=dict_inter,
        clients=all_client,
        intervenants=all_intervenant,
        interventions=all_interventions,
        image=image,
        message=message,
    )


@app.route("/intervantions")
def intervantion():
    messages = get_flashed_messages()
    if messages:
        message = messages[0]
    else:
        message = "-1"
    print(message)
    if "user" not in session:
        return redirect(url_for("login"))
    dict_cli = Client.select_dict_cli()
    dict_inter = Intervenant.select_dict_Inter()
    all_intervenant = Intervenant.select_all_intervenants()
    all_client = Client.select_all_clients()
    all_interventions = Intervention.select_all_interventions()
    image = get_graphe(Intervention.count_interventions_by_status())
    return render_template(
        "intervantion.html",
        dict_cli=dict_cli,
        dict_inter=dict_inter,
        clients=all_client,
        intervenants=all_intervenant,
        interventions=all_interventions,
        image=image,
        message=message,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("intervantion"))
        error = "Nom d'utilisateur ou mot de passe incorrect"
        return render_template("login.html", error=error)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/add/Intervennat", methods=["GET", "POST"])
def add_intervennant():
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        poste = request.form.get("poste")
        if Intervenant.insert_intervenant(nom, prenom, poste):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervenant"))


@app.route("/update/Intervennat", methods=["GET", "POST"])
def update_intervennant():
    if request.method == "POST":
        id = request.form.get("id")
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        poste = request.form.get("poste")
        if Intervenant.update_intervenant(id, nom, prenom, poste):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervenant"))


@app.route("/Delete/Intervenant", methods=["GET", "POST"])
def delete_intervennant():
    if request.method == "POST":
        id = request.form.get("id")
        if Intervenant.delete_intervenant(id):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervenant"))


@app.route("/add/Client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        poste = request.form.get("direction")
        if Client.insert_client(nom, prenom, poste):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("client"))


@app.route("/update/Client", methods=["GET", "POST"])
def update_client():
    if request.method == "POST":
        id = request.form.get("id")
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        poste = request.form.get("direction")
        if Client.update_client(id, nom, prenom, poste):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("client"))


@app.route("/Delete/Client", methods=["GET", "POST"])
def delete_client():
    if request.method == "POST":
        id = request.form.get("id")
        if Client.delete_client(id):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("client"))


@app.route("/add/Intervennation", methods=["GET", "POST"])
def add_intervennantion():
    if request.method == "POST":
        motive = request.form.get("motive")
        typeIn = request.form.get("type")
        client = request.form.get("client")
        intervenant = request.form.get("intervenant")
        if Intervention.insert_intervention(motive, typeIn, client, intervenant):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervantion"))


@app.route("/update/Intervennation", methods=["GET", "POST"])
def update_intervennantion():
    if request.method == "POST":
        id = request.form.get("id")
        motive = request.form.get("motive")
        typeIn = request.form.get("type")
        client = request.form.get("client")
        intervenant = request.form.get("intervenant")
        if Intervention.update_intervention(id, motive, typeIn, client, intervenant):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervantion"))


@app.route("/Delete/Intervention", methods=["GET", "POST"])
def delete_intervention():
    if request.method == "POST":
        id = request.form.get("id")
        if Intervention.delete_intervention(id):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervantion"))


@app.route("/intervention/realiser", methods=["GET", "POST"])
def realiser():
    if request.method == "POST":
        id = request.form.get("id")
        if Intervention.realiser(id):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervantion"))


@app.route("/intervention/Reinitialiser", methods=["GET", "POST"])
def Reinitialiser():
    if request.method == "POST":
        id = request.form.get("id")
        if Intervention.Reinitialiser(id):
            flash("1")
        else:
            flash("0")
    return redirect(url_for("intervantion"))


@app.route("/client/info", methods=["GET", "POST"])
def client_info():
    if request.method == "POST":
        id = request.form.get("id")
        intervention = Intervention.select_interventions_by_client(id)
        image = get_graphe(Intervention.count_interventions_by_status_and_client(id))
        client = Client.select_client(id)
        return render_template(
            "info.html",
            interventions=intervention,
            user=client,
            image=image,
            role="client",
        )
    return redirect(url_for("client"))


@app.route("/intervenant/info", methods=["GET", "POST"])
def intervenant_info():
    if request.method == "POST":
        id = request.form.get("id")
        intervention = Intervention.select_interventions_by_intervenant(id)
        image = get_graphe(
            Intervention.count_interventions_by_status_and_intervenant(id)
        )
        intervenant = Intervenant.select_intervenant(id)
        return render_template(
            "info.html",
            interventions=intervention,
            user=intervenant,
            image=image,
            role="intervenant",
        )
    return redirect(url_for("intervenant"))


if __name__ == "__main__":
    app.run(debug=True)
