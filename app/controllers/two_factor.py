from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from services import TwoFactorService
from models import db

two_factor_bp = Blueprint('two_factor', __name__, url_prefix='/2fa')
two_factor_service = TwoFactorService(db)

@two_factor_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    """Setup 2FA for current user"""
    if 'user_id' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('main.login'))
    
    if request.method == 'GET':
        # Start 2FA setup
        result = two_factor_service.setup_2fa(session['user_id'])
        
        if result.success:
            # Store secret key in session for later verification  
            session['temp_totp_secret'] = result.data['secret_key']
            return render_template('2fa_setup.html', 
                                 qr_code=result.data['qr_code'],
                                 secret_key=result.data['secret_key'])
        else:
            flash(result.message, 'error')
            return redirect(url_for('main.dashboard'))
    
    else:  # POST
        # Verify and enable 2FA
        totp_code = request.form.get('totp_code')
        temp_secret = session.get('temp_totp_secret')
        
        if not totp_code:
            flash('Please enter the verification code.', 'error')
            return redirect(url_for('two_factor.setup'))
        
        if not temp_secret:
            flash('Setup session expired. Please start again.', 'error')
            return redirect(url_for('two_factor.setup'))
        
        result = two_factor_service.enable_2fa(session['user_id'], totp_code, temp_secret)
        
        if result.success:
            # Clear temp secret from session
            session.pop('temp_totp_secret', None)
            flash('2FA enabled successfully! Please save your backup codes.', 'success')
            return render_template('2fa_backup_codes.html', 
                                 backup_codes=result.data['backup_codes'])
        else:
            flash(result.message, 'error')
            return redirect(url_for('two_factor.setup'))

@two_factor_bp.route('/disable', methods=['POST'])
def disable():
    """Disable 2FA for current user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})
    
    password = request.form.get('password')
    code = request.form.get('code')
    
    if not password or not code:
        return jsonify({'success': False, 'message': 'Password and verification code are required'})
    
    result = two_factor_service.disable_2fa(session['user_id'], password, code)
    
    if result.success:
        flash('2FA disabled successfully.', 'success')
        return jsonify({'success': True, 'message': result.message})
    else:
        return jsonify({'success': False, 'message': result.message})

@two_factor_bp.route('/verify', methods=['POST'])
def verify():
    """Verify 2FA code during login process"""
    account_id = request.form.get('account_id')
    totp_code = request.form.get('totp_code')
    
    if not account_id or not totp_code:
        return jsonify({'success': False, 'message': 'Missing required parameters'})
    
    result = two_factor_service.verify_2fa_login(account_id, totp_code)
    
    return jsonify({
        'success': result.success,
        'message': result.message
    })
