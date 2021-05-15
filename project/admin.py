# models.py
import os
import random

from flask import url_for, redirect
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_ckeditor import CKEditorField
from flask_login import current_user
from markupsafe import Markup

from project import db, ad
from project.models import Machine, Adaption, Customer, Offers, Storage


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
    form_overrides = dict(description=CKEditorField)
    column_labels = dict(name='Nazwa', description='Opis', adaption="Zastosowanie")

    create_template = 'machine/edit.html'
    edit_template = 'machine/edit.html'


ad.add_view(MachineView(Machine, db.session, "Urządzenia Rolnicze"))


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


class GoToHome(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


ad.add_link(GoToHome(name='Wróć', category='', url="/"))
ad.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))


class StorageView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        url = url_for('static', filename=os.path.join(model.path))
        print(url)
        if model.type in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            return Markup('<img src="%s" width="100">' % url)

        if model.type in ['mp3']:
            return Markup('<audio controls="controls"><source src="%s" type="audio/mpeg" /></audio>' % url)

        if model.type in ['mp4']:
            return Markup(
                '<video controls="controls"><source src="%s" width="320" height="240" type="video/mp4" /></video>' % url)

    column_formatters = {
        'path': _list_thumbnail
    }

    form_extra_fields = {
        'file': form.FileUploadField('file')
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                path = '%s.%s' % (hash, ext)

                storage_file.save(
                    os.path.join("/home/adam/Desktop/p/msrol/files/", path)
                )

                _form.name.data = _form.name.data or storage_file.filename
                _form.path.data = path
                _form.type.data = ext

                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(StorageView, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(StorageView, self).create_form(obj)
        )


ad.add_view(StorageView(Storage, db.session, "Załączniki"))
