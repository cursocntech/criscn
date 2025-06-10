from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Agendamento
from auth import auth_bp, login_manager
import config

app = flask(__name__)
app.config.from_object(config.Config)

db.init_app(app)
app.register_blueprint(auth_bp)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def index():
    return redirect(url_for('meus_agendamentos'))

@app.route('/meus')
@login_required
def meus_agendamentos():
    ag = Agendamento.query.filter_by(professor_id=current_user.id).all()
    return render_template('meus_agendamentos.html', agendamentos=ag)

@app.route('/agendar', methods=['GET','POST'])
@login_required
def agendar():
    if request.method == 'POST':
        gabe = int(request.form['gabinete'])
        turno = request.form['turno']
        if Agendamento.query.filter_by(professor_id=current_user.id, turno=turno).first():
            flash('Você já tem um agendamento neste turno.')
            return redirect(url_for('agendar'))
        if Agendamento.query.filter_by(gabinete=gabe, turno=turno).first():
            flash('Gabinete já está ocupado neste turno.')
            return redirect(url_for('agendar'))
        novo = Agendamento(professor_id=current_user.id, gabinete=gabe, turno=turno)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('meus_agendamentos'))
    return render_template('agendar.html')

@app.route('/cancelar/<int:id>')
@login_required
def cancelar(id):
    ag = Agendamento.query.get_or_404(id)
    if ag.professor_id != current_user.id:
        flash('Operação não autorizada.')
        return redirect(url_for('index'))
    db.session.delete(ag)
    db.session.commit()
    return redirect(url_for('meus_agendamentos'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
