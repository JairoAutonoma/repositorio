from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
from application.use_cases.login import LoginUseCase
from application.use_cases.upload_thesis import UploadThesisUseCase
from application.use_cases.evaluate_thesis import EvaluateThesisUseCase
from application.use_cases.certify_thesis import CertifyThesisUseCase
from application.use_cases.get_theses import GetThesesUseCase
from infrastructure.persistence.json_user_repository import JsonUserRepository
from infrastructure.persistence.json_thesis_repository import JsonThesisRepository
from infrastructure.persistence.file_storage import FileStorage
from domain.services.authentication_service import AuthenticationService
from domain.services.thesis_service import ThesisService

load_dotenv()

app = Flask(__name__, static_folder= os.path.join(os.path.dirname(__file__), "../../frontend"))
CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")

# Inyección de dependencias XD
user_repository = JsonUserRepository(DATA_DIR)
thesis_repository = JsonThesisRepository(DATA_DIR)
file_storage = FileStorage(PDF_DIR)
authentication_service = AuthenticationService(user_repository)
thesis_service = ThesisService(thesis_repository)
login_use_case = LoginUseCase(authentication_service)
upload_thesis_use_case = UploadThesisUseCase(thesis_service)
evaluate_thesis_use_case = EvaluateThesisUseCase(thesis_service)
certify_thesis_use_case = CertifyThesisUseCase(thesis_service)
get_theses_use_case = GetThesesUseCase(thesis_repository)

#----------------INDEX--------------#
@app.route("/", methods = ["GET"])
def get_index():
    return send_from_directory(app.static_folder, "index.html")


#----------------LOGIN--------------#
@app.route("/login", methods=["GET"])
def get_login():
    return send_from_directory(app.static_folder, "login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")
    result = login_use_case.execute(email, password)
    status = result.pop("status",200)
    return jsonify(result), status


#------------------user--------------#
@app.route("/subir_tesis", methods=["GET"])
def get_upload_tesis():
    return send_from_directory(app.static_folder, "subir_tesis.html")

@app.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    user = get_jwt_identity()
    archivo = request.files["archivo"]
    titulo = request.form.get("titulo")
    safe_filename = f"{titulo.replace(' ', '_')}_{user.split('@')[0]}.pdf"
    file_storage.save_file(archivo, safe_filename)
    result = upload_thesis_use_case.execute(titulo, safe_filename, user)
    return jsonify(result)

@app.route("/mis_tesis")
@jwt_required()
def mis_tesis():
    user = get_jwt_identity()
    theses = get_theses_use_case.get_by_author(user)
    return jsonify([vars(t) for t in theses])



#------------------evaluador--------------#
@app.route("/evaluar_tesis", methods = ["GET"])
def get_eval_thesis():
    return send_from_directory(app.static_folder, "evaluar_tesis.html")


@app.route("/tesis/asignadas")
@jwt_required()
def asignadas():
    theses = get_theses_use_case.get_all()
    return jsonify([vars(t) for t in theses])

@app.route("/evaluar", methods=["POST"])
@jwt_required()
def evaluar():
    data = request.get_json()
    result = evaluate_thesis_use_case.execute(
        int(data["tesis_id"]), data["comentario"], data["nota"]
    )
    return jsonify(result)


#----------------certificador--------------#
@app.route("/certificar_tesis", methods = ["GET"])
def get_certificar_tesis():
    return send_from_directory(app.static_folder, "certificar_tesis.html")

@app.route("/admin/tesis-evaluadas")
@jwt_required()
def evaluadas():
    theses = get_theses_use_case.get_all()
    return jsonify([vars(t) for t in theses])

@app.route("/certificar/<int:id>", methods=["POST"])
@jwt_required()
def certificar(id):
    user = get_jwt_identity()
    result = certify_thesis_use_case.execute(id, user)
    return jsonify(result)

@app.route('/pdfs/<filename>')
def get_pdf(filename):
    return send_from_directory(PDF_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)