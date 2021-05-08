# models.py
from flask import url_for, redirect

from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from markupsafe import Markup

from project import db, ad
from project.models import Machine, Adaption, Customer, Offers


class CustomerView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    column_searchable_list = ['name']


ad.add_view(CustomerView(Customer, db.session, "Klienci"))


class OffersView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    column_list = ('customer', 'machine', 'price', 'create_date', 'Pdf')
    column_labels = dict(customer='Klient', machine='Maszyna', price='cena', create_date='Data oferty', Pdf='Exportuj')
    form_widget_args = {
        'create_date': {
            'readonly': True
        },
    }

    def _format_pay_now(view, context, model, name):
        # render a form with a submit button for student, include a hidden field for the student id
        # note how checkout_view method is exposed as a route below
        checkout_url = url_for('main.pdf', id=model.id)
        print(model)
        _html = '''
        <a target="_blank" href={checkout_url}>Pdf</a>
        '''.format(checkout_url=checkout_url)

        return Markup(_html)

    column_formatters = {
        'Pdf': _format_pay_now
    }


ad.add_view(OffersView(Offers, db.session, "Offers"))


class AdaptionView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    column_searchable_list = ['name']
    column_labels = dict(name='Zastosowanie')


ad.add_view(AdaptionView(Adaption, db.session, "Zastosowanie"))


class MachineView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    column_searchable_list = ['name']
    column_descriptions = dict(
        adaption='Zastosowanie maszyny rolniczej',
        name='Nazwa maszyny rolniczej',
        description='Opis maszyny rolniczej'
    )
    column_labels = dict(name='Nazwa', description='Opis', adaption="Zastosowanie")


ad.add_view(MachineView(Machine, db.session, "Urządzenia Rolnicze"))


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


class GoToHome(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


ad.add_link(GoToHome(name='Wróć', category='', url="/"))
ad.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
