# main.py
import pdfkit as pdfkit
from flask import Blueprint, render_template, make_response, send_file
from flask_login import login_required, current_user
from markupsafe import Markup
from project import db
from project.models import Offers

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/offers')
def offers():
    return render_template('offers.html', name="twoje ofety")


@main.route('/static/<id>')
def return_files_tut(id):
    try:
        return send_file('/home/adam/Desktop/p/msrol/files/' + id, attachment_filename='python.jpg')
    except Exception as e:
        return str(e)


@main.route('/pdf/<id>', methods=['GET'])
@login_required
def pdf(id):
    a = db.session.query(Offers).filter(Offers.id == id).first()

    html = render_template("report.html", type=a.machine.adaption, description=Markup(a.machine.description),
                           machine=a.machine,
                           name=a.customer, date=a.create_date, price=a.price)
    pdf = pdfkit.from_string(html, False)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response
