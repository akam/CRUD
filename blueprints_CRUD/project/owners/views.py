from flask import Blueprint, render_template, request, redirect, url_for
from project.owners.models import Owner
from project.owners.forms import OwnerForm
from project import db

owners_blueprint = Blueprint(
	'owners',
	__name__,
	template_folder='templates'
)

@owners_blueprint.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		form = OwnerForm()
		from IPython import embed; embed()
		if form.validate():
			db.session.add(Owner(request.form['first_name'], request.form['last_name']))
			db.session.commit()
			return redirect(url_for('owners.index'))
		return render_template('owners/new.html', form=form)
	return render_template('owners/index.html', owners=Owner.query.all())

@owners_blueprint.route('/new')
def new():
	form = OwnerForm()
	return render_template('owners/new.html', form=form)

@owners_blueprint.route('/<int:id>/edit')
def edit(id):
	owner = Owner.query.get(id)
	form = OwnerForm(obj=owner)
	return render_template('owners/edit.html', form=form, owner=owner)

@owners_blueprint.route('/<int:id>', methods=["GET","PATCH","DELETE"])
def show(id):
	found_owner = Owner.query.get(id)
	if request.method == b'PATCH':
		form = OwnerForm(request.form)
		if form.validate():
			found_owner.first_name = request.form['first_name']
			found_owner.last_name = request.form['last_name']
			db.session.add(found_owner)
			db.session.commit()
			return redirect(url_for('owners.index'))
		return	render_template('owners/edit.html', form=form, owner=found_owner)
	if request.method == b'DELETE':
		db.session.delete(found_owner)
		db.session.commit()
		return redirect(url_for('owners.index'))
	return	render_template('owners/show.html', owner=found_owner)