from flask import Flask, render_template, redirect, url_for, request, flash, send_file, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager, make_celery
from models import User, Scan, Finding, ApiKey
from config import Config
from datetime import datetime
from api import api_bp
import os
import secrets

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
celery = make_celery(app)

# Register API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper for generating API keys (for user UI)
def generate_api_key():
    return secrets.token_urlsafe(32)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_scans = Scan.query.filter_by(user_id=current_user.id).count()
    today_scans = Scan.query.filter(
        Scan.user_id == current_user.id,
        Scan.created_at >= datetime.utcnow().date()
    ).count()
    high_risk = Scan.query.filter(
        Scan.user_id == current_user.id,
        Scan.risk_score >= 51
    ).count()

    recent_scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.created_at.desc()).limit(10).all()

    risk_counts = {
        'Low': Scan.query.filter_by(user_id=current_user.id, risk_level='Low').count(),
        'Medium': Scan.query.filter_by(user_id=current_user.id, risk_level='Medium').count(),
        'High': Scan.query.filter_by(user_id=current_user.id, risk_level='High').count(),
        'Critical': Scan.query.filter_by(user_id=current_user.id, risk_level='Critical').count()
    }

    # API keys
    api_keys = ApiKey.query.filter_by(user_id=current_user.id, active=True).all()

    return render_template('dashboard.html',
                           total_scans=total_scans,
                           today_scans=today_scans,
                           high_risk=high_risk,
                           recent_scans=recent_scans,
                           risk_counts=risk_counts,
                           api_keys=api_keys)

@app.route('/scanner')
@login_required
def scanner():
    return render_template('scanner.html')

@app.route('/scan', methods=['POST'])
@login_required
def scan():
    target = request.form['target']
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    # Launch Celery task instead of running synchronously
    task = celery.send_task('tasks.scan_target', args=[current_user.id, target])
    return jsonify({'task_id': task.id}), 202

@app.route('/scan/<task_id>')
@login_required
def scan_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state == 'PROGRESS':
        response = {'state': task.state, 'status': task.info.get('status', '')}
    elif task.state == 'SUCCESS':
        result = task.result
        if 'scan_id' in result:
            response = {'state': task.state, 'scan_id': result['scan_id']}
        else:
            response = {'state': 'FAILURE', 'error': result.get('error', 'Unknown error')}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)

@app.route('/results/<int:scan_id>')
@login_required
def results(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    if scan.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))
    findings = Finding.query.filter_by(scan_id=scan.id).all()
    return render_template('results.html', scan=scan, findings=findings)

@app.route('/download/<int:scan_id>')
@login_required
def download_report(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    if scan.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))
    findings = Finding.query.filter_by(scan_id=scan.id).all()
    pdf_buffer = generate_pdf(scan, findings)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{scan.target.replace('https://','').replace('http://','')}-report.pdf",
        mimetype='application/pdf'
    )

@app.route('/history')
@login_required
def history():
    scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.created_at.desc()).all()
    return render_template('history.html', scans=scans)

@app.route('/generate-api-key', methods=['POST'])
@login_required
def generate_new_api_key():
    key = generate_api_key()
    new_key = ApiKey(user_id=current_user.id, key=key)
    db.session.add(new_key)
    db.session.commit()
    flash(f'New API key generated: {key}', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)