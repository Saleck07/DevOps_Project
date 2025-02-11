from flask import Flask, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234$22@121&221$&"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///min_pro_flask.sqlite3"
db = SQLAlchemy(app)


class Intervenant(db.Model):
    __tablename__ = "intervenant"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    poste = db.Column(db.String(200), nullable=False)
    
    interventions = db.relationship("Intervention", backref="intervenant", cascade="all, delete-orphan")
    
    def __init__(self, nom,prenom, poste):
        self.nom = nom
        self.prenom = prenom
        self.poste = poste

    def getId(self):
        return f"INT-{self.id}"
    def get_intervenant(self):
        return {
            "id": self.getId(),
            "nom": self.nom,
            "prenom": self.prenom,
            "poste": self.poste,
        }
    @staticmethod
    def insert_intervenant(nom, prenom ,poste):
        try:
            new_intervenant = Intervenant(nom=nom, prenom=prenom, poste=poste)
            db.session.add(new_intervenant)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
    @staticmethod
    def update_intervenant(id, nom, prenom, poste):
        try:
            int_id = id[4:]
            intervenant = Intervenant.query.get(int_id)
            if intervenant:
                intervenant.nom = nom
                intervenant.prenom = prenom
                intervenant.poste = poste
                db.session.commit()
                return True
            else:
                return False 
        except Exception as e:
            db.session.rollback()
            return False
    @staticmethod
    def delete_intervenant(id):
        try:
            int_id = id[4:]
            intervenant = Intervenant.query.get(int_id)
            if intervenant:
                db.session.delete(intervenant)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False
        
    @staticmethod
    def select_intervenant(intervenant_id):
        int_id = intervenant_id[4:]
        intervenant = Intervenant.query.get(int_id)
        if intervenant:
            return intervenant.get_intervenant()
        return False

    @staticmethod
    def select_all_intervenants():
        intervenants = Intervenant.query.all()
        data = []
        for intervenant in intervenants:
            data.append(intervenant.get_intervenant())
        return data
    @staticmethod 
    def select_dict_Inter():
        intervenants = Intervenant.query.all()
        data = {}
        for intervenant in intervenants:
            data[intervenant.getId()]=f"{intervenant.nom} {intervenant.prenom}"
        return data
class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    direction = db.Column(db.String(200), nullable=False)
    
    interventions = db.relationship("Intervention",backref="client",cascade="all, delete-orphan")
    def __init__(self, nom, prenom,direction):
        self.nom = nom
        self.prenom = prenom
        self.direction = direction
    def getId(self):
        return f"CLI-{self.id}"
    def get_client(self):
        return {
            "id": self.getId(),
            "nom": self.nom,
            "prenom": self.prenom,
            "direction": self.direction,
        }
    def insert_client(nom, prenom, direction):
        try:
            new_client = Client(nom=nom, prenom=prenom, direction=direction )
            db.session.add(new_client)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    @staticmethod
    def update_client(id, nom, prenom, direction):
        try:
            id=id[4:]
            client = Client.query.get(id)
            if client:
                client.nom = nom
                client.prenom = prenom
                client.direction = direction
                db.session.commit()
                return True
            else:
                return False 
        except Exception as e:
            print(e)
            db.session.rollback()
            return False  
    @staticmethod
    def delete_client(client_id):
        try:
            cl_id = client_id[4:] 
            client = Client.query.get(cl_id)
            if client:
                db.session.delete(client)
                db.session.commit()
                return True
            else:
                return False 
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return False
    @staticmethod
    def select_client(client_id):
        cl_id = client_id[4:]
        client = Client.query.get(cl_id)
        if client:
            return client.get_client()
        return False
    @staticmethod
    def select_all_clients():
        clients = Client.query.all()
        data = []
        for client in clients:
            data.append(client.get_client())
        return data
    @staticmethod 
    def select_dict_cli():
        clients = Client.query.all()
        data = {}
        for client in clients:
            data[client.getId()]=f"{client.nom} {client.prenom}"
        return data
class Intervention(db.Model):
    __tablename__ = "intervention"
    id = db.Column(db.Integer, primary_key=True)
    motive = db.Column(db.String(200), nullable=False)
    type_inter = db.Column(db.String(200), nullable=False)
    etat = db.Column(db.String(200), nullable=False, default="En attente")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    idClient = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    idIntervenant = db.Column(db.Integer, db.ForeignKey("intervenant.id"), nullable=False)

    def __init__(self, motive,type_inter, idClient,idIntervenant):
        self.motive = motive
        self.type_inter = type_inter
        self.idClient = idClient
        self.idIntervenant=idIntervenant

    def getId(self):
        return f"INTER-{self.id}"

    def get_interventions(self):
        data = {
            "id": self.getId(),
            "motive": self.motive,
            "type": self.type_inter,
            "etat":self.etat,
            "client": f"CLI-{self.idClient}",
            "date":self.date.strftime("%d-%m-%Y %H:%M:%S")[:20],
            "intervenant":f"INT-{self.idIntervenant}",
        }
        return data
    @staticmethod
    def select_intervention(inter_id):
        int_id = inter_id[6:]
        intervention = Intervention.query.get(int_id)
        if intervention:
            return intervention.get_interventions()
        return False

    @staticmethod
    def delete_intervention(inter_id):
        int_id = inter_id[6:]
        try:
            intervention = Intervention.query.get(int_id)
            if intervention:
                db.session.delete(intervention)
                db.session.commit()
                return True
            return False
        except:
            db.session.rollback()
            return False
    @staticmethod
    def select_all_interventions():
        interventions = Intervention.query.all()
        data = []
        for intervention in interventions:
            data.append(intervention.get_interventions())
        return data
    @staticmethod
    
    def select_interventions_by_client(idClient):
        idClient=idClient[4:]
        interventions = Intervention.query.filter_by(idClient=idClient).all()
        data = []
        for intervention in interventions:
            data.append(intervention.get_interventions())
        return data
    @staticmethod
    def select_interventions_by_intervenant(idIntervenant):
        idIntervenant=idIntervenant[4:]
        interventions = Intervention.query.filter_by(idIntervenant=idIntervenant).all()
        data = []
        for intervention in interventions:
            data.append(intervention.get_interventions())
        return data

    @staticmethod
    def insert_intervention(motive,type_inter, idClient,idIntervenant):
        idClient=idClient[4:]
        idIntervenant=idIntervenant[4:]
        try:
            new_intervention = Intervention(motive=motive, idClient=idClient,type_inter = type_inter,idIntervenant=idIntervenant)
            db.session.add(new_intervention)
            db.session.commit()
            return True
        except :
            db.session.rollback()
            return False
    @staticmethod
    def update_intervention(id, motive, type_inter, idClient, idIntervenant):
        try:
            idClient = idClient[4:]
            idIntervenant = idIntervenant[4:]
            id_intervention = id[6:]
            intervention = Intervention.query.get(id_intervention)
            if intervention:
                intervention.motive = motive
                intervention.type_inter = type_inter
                intervention.idClient = idClient
                intervention.idIntervenant = idIntervenant
                db.session.commit()
                return True
            else:
                return False 
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def realiser(inter_id):
        int_id = inter_id[6:]
        try:
            intervention = Intervention.query.get(int_id)
            if intervention:
                intervention.etat = "Réalisé"
                db.session.commit()
                return True
            return False
        except:
            db.session.rollback()
            return False
    @staticmethod 
    def Reinitialiser(inter_id):
        int_id = inter_id[6:]
        try:
            intervention = Intervention.query.get(int_id)
            if intervention:
                intervention.etat = "En attente"
                db.session.commit()
                return True
            return False
        except:
            db.session.rollback()
            return False
    @staticmethod
    def count_interventions_by_status():
        try:
            pending_count = Intervention.query.filter_by(etat="En attente").count()
            completed_count = Intervention.query.filter_by(etat="Réalisé").count()
            return {
                "En attente": pending_count,
                "Réalisé": completed_count
            }
        except:
            return False
    @staticmethod
    def count_interventions_by_status_and_client(idClient):
        idClient=idClient[4:]
        try:
            pending_count = Intervention.query.filter_by(idClient=idClient, etat="En attente").count()
            completed_count = Intervention.query.filter_by(idClient=idClient, etat="Réalisé").count()
            return {
                "En attente": pending_count,
                "Réalisé": completed_count
            }
        except:
            return False
    @staticmethod
    def count_interventions_by_status_and_intervenant(idIntervenant):
        idIntervenant=idIntervenant[4:]
        try:
            in_progress_count = Intervention.query.filter_by(idIntervenant=idIntervenant, etat="En attente").count()
            completed_count = Intervention.query.filter_by(idIntervenant=idIntervenant, etat="Réalisé").count()
            return {
                "En attente": in_progress_count,
                "Réalisé": completed_count
            }
        except :
            return False
