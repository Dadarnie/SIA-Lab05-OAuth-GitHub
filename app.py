from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "REPLACE_WITH_A_STRONG_RANDOM_SECRET"

oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id='Ov23lizxAmB2r5qfF7YI',
    client_secret='36cf2c9f7ae34abb6c047a34bf3b1ad4f7c317ce',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@app.route('/')
def index():
    return redirect('/login')


@app.route('/hello')
def hello():
    if 'user' not in session:
        return "Unauthorized", 401
    user = session['user']
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Hello - {user.get('login')}</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                background: #0d1117;
                color: #e6edf3;
                min-height: 100vh;
            }}
            .navbar {{
                background: #161b22;
                border-bottom: 1px solid #30363d;
                padding: 12px 24px;
                display: flex;
                align-items: center;
                gap: 16px;
            }}
            .navbar svg {{ fill: #e6edf3; }}
            .navbar-links {{
                display: flex;
                gap: 16px;
                margin-left: auto;
                align-items: center;
            }}
            .navbar-links a {{
                color: #e6edf3;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
            }}
            .navbar-links a:hover {{ color: #58a6ff; }}
            .avatar-small {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: 1px solid #30363d;
            }}
            .container {{
                max-width: 600px;
                margin: 80px auto;
                padding: 0 24px;
                text-align: center;
            }}
            .avatar {{
                width: 96px;
                height: 96px;
                border-radius: 50%;
                border: 2px solid #30363d;
                margin-bottom: 24px;
            }}
            .greeting {{
                font-size: 32px;
                font-weight: 600;
                margin-bottom: 8px;
            }}
            .sub {{
                font-size: 16px;
                color: #8b949e;
                margin-bottom: 32px;
            }}
            .badge {{
                display: inline-block;
                background: #238636;
                color: #e6edf3;
                font-size: 13px;
                font-weight: 500;
                padding: 4px 12px;
                border-radius: 20px;
                margin-bottom: 32px;
            }}
            .btn {{
                display: inline-block;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                text-decoration: none;
                border: 1px solid #30363d;
                background: #21262d;
                color: #e6edf3;
                margin: 4px;
            }}
            .btn:hover {{ background: #30363d; }}
        </style>
    </head>
    <body>
        <nav class="navbar">
            <svg height="32" viewBox="0 0 16 16" width="32">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87
                2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95
                0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21
                2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04
                2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82
                2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0
                1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            <div class="navbar-links">
                <a href="/profile">Profile</a>
                <a href="/hello">Hello</a>
                <a href="/api/secure-data">Secure Data</a>
                <img class="avatar-small" src="{user.get('avatar_url')}" alt="avatar">
                <a href="/logout" style="color:#f85149;">Sign out</a>
            </div>
        </nav>

        <div class="container">
            <img class="avatar" src="{user.get('avatar_url')}" alt="avatar">
            <div class="greeting">Hello, {user.get('name') or user.get('login')}!</div>
            <div class="sub">@{user.get('login')} is successfully authenticated via GitHub OAuth 2.0.</div>
            <div><span class="badge">Session Active</span></div>
            <a class="btn" href="/profile">Back to Profile</a>
            <a class="btn" href="/api/secure-data">View Secure Data</a>
            <a class="btn" href="/logout" style="color:#f85149;">Sign out</a>
        </div>
    </body>
    </html>
    '''

@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user', token=token).json()
    session['user'] = user
    return redirect('/profile')


@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized", 401
    user = session['user']
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{user.get('login')} - Profile</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                background: #0d1117;
                color: #e6edf3;
                min-height: 100vh;
            }}
            .navbar {{
                background: #161b22;
                border-bottom: 1px solid #30363d;
                padding: 12px 24px;
                display: flex;
                align-items: center;
                gap: 16px;
            }}
            .navbar svg {{ fill: #e6edf3; }}
            .navbar-links {{
                display: flex;
                gap: 16px;
                margin-left: auto;
                align-items: center;
            }}
            .navbar-links a {{
                color: #e6edf3;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
            }}
            .navbar-links a:hover {{ color: #58a6ff; }}
            .avatar-small {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: 1px solid #30363d;
            }}
            .container {{
                max-width: 1012px;
                margin: 32px auto;
                padding: 0 24px;
                display: grid;
                grid-template-columns: 296px 1fr;
                gap: 24px;
            }}
            .sidebar {{ display: flex; flex-direction: column; gap: 16px; }}
            .avatar-large {{
                width: 100%;
                border-radius: 50%;
                border: 1px solid #30363d;
            }}
            .profile-name {{
                font-size: 26px;
                font-weight: 600;
                line-height: 1.25;
                margin-top: 16px;
            }}
            .profile-username {{
                font-size: 20px;
                font-weight: 300;
                color: #8b949e;
                margin-bottom: 16px;
            }}
            .btn {{
                display: block;
                width: 100%;
                padding: 5px 16px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                text-align: center;
                text-decoration: none;
                cursor: pointer;
                border: 1px solid #30363d;
                margin-bottom: 8px;
            }}
            .btn-default {{
                background: #21262d;
                color: #e6edf3;
            }}
            .btn-default:hover {{ background: #30363d; }}
            .btn-danger {{
                background: #21262d;
                color: #f85149;
                border-color: #30363d;
            }}
            .btn-danger:hover {{ background: #2d1b1b; border-color: #f85149; }}
            .profile-meta {{
                display: flex;
                flex-direction: column;
                gap: 8px;
                font-size: 14px;
                color: #8b949e;
                border-top: 1px solid #30363d;
                padding-top: 16px;
            }}
            .profile-meta span {{ color: #e6edf3; font-weight: 500; }}
            .main {{ display: flex; flex-direction: column; gap: 16px; }}
            .section-title {{
                font-size: 16px;
                font-weight: 600;
                padding-bottom: 8px;
                border-bottom: 1px solid #30363d;
                margin-bottom: 12px;
            }}
            .card {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 16px;
            }}
            .data-row {{
                display: flex;
                justify-content: space-between;
                font-size: 14px;
                padding: 8px 0;
                border-bottom: 1px solid #21262d;
            }}
            .data-row:last-child {{ border-bottom: none; }}
            .data-label {{ color: #8b949e; }}
            .data-value {{ color: #e6edf3; font-weight: 500; }}
            .badge-green {{
                display: inline-block;
                background: #238636;
                color: #e6edf3;
                font-size: 12px;
                font-weight: 500;
                padding: 2px 8px;
                border-radius: 20px;
            }}
        </style>
    </head>
    <body>
        <nav class="navbar">
            <svg height="32" viewBox="0 0 16 16" width="32">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87
                2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95
                0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21
                2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04
                2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82
                2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0
                1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            <div class="navbar-links">
                <a href="/profile">Profile</a>
                <a href="/hello">Hello</a>
                <a href="/api/secure-data">Secure Data</a>
                <img class="avatar-small" src="{user.get('avatar_url')}" alt="avatar">
                <a href="/logout" style="color:#f85149;">Sign out</a>
            </div>
        </nav>

        <div class="container">
            <div class="sidebar">
                <img class="avatar-large" src="{user.get('avatar_url')}" alt="Profile Photo">
                <div>
                    <div class="profile-name">{user.get('name') or user.get('login')}</div>
                    <div class="profile-username">{user.get('login')}</div>
                </div>
                <a class="btn btn-default" href="{user.get('html_url')}" target="_blank">View GitHub Profile</a>
                <a class="btn btn-default" href="/api/secure-data">View Secure Data</a>
                <a class="btn btn-default" href="/hello">Say Hello</a>
                <a class="btn btn-danger" href="/logout">Sign out</a>
                <div class="profile-meta">
                    <div>Email: <span>{user.get('email') or 'Not public'}</span></div>
                    <div>GitHub ID: <span>{user.get('id')}</span></div>
                    <div>Public Repos: <span>{user.get('public_repos', 0)}</span></div>
                    <div>Followers: <span>{user.get('followers', 0)}</span></div>
                    <div>Following: <span>{user.get('following', 0)}</span></div>
                </div>
            </div>

            <div class="main">
                <div class="card">
                    <div class="section-title">Session Info</div>
                    <div class="data-row">
                        <span class="data-label">Status</span>
                        <span class="data-value"><span class="badge-green">Authenticated</span></span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Username</span>
                        <span class="data-value">@{user.get('login')}</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Display Name</span>
                        <span class="data-value">{user.get('name') or 'N/A'}</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Email</span>
                        <span class="data-value">{user.get('email') or 'Not public'}</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Profile URL</span>
                        <span class="data-value">
                            <a href="{user.get('html_url')}" target="_blank" style="color:#58a6ff;">
                                {user.get('html_url')}
                            </a>
                        </span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Avatar URL</span>
                        <span class="data-value" style="word-break:break-all; font-size:12px; color:#8b949e;">
                            {user.get('avatar_url')}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''


@app.route('/logout')
def logout():
    session.pop('user', None)
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Signed Out</title>
        <meta http-equiv="refresh" content="3;url=/login">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                background: #0d1117;
                color: #e6edf3;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                text-align: center;
            }
            .card {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 40px 48px;
                width: 360px;
            }
            svg { fill: #e6edf3; margin-bottom: 16px; }
            .title { font-size: 20px; font-weight: 600; margin-bottom: 8px; }
            .sub { font-size: 14px; color: #8b949e; }
            a { color: #58a6ff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <svg height="40" viewBox="0 0 16 16" width="40">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87
                2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95
                0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21
                2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04
                2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82
                2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0
                1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            <div class="title">You have been signed out.</div>
            <div class="sub" style="margin-top:12px;">
                Redirecting to login in 3 seconds...<br><br>
                <a href="/login">Sign in again</a>
            </div>
        </div>
    </body>
    </html>
    '''


@app.route('/api/secure-data')
def secure_data():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized. Please log in first."}), 401
    user = session['user']
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Secure Data</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                background: #0d1117;
                color: #e6edf3;
                min-height: 100vh;
            }}
            .navbar {{
                background: #161b22;
                border-bottom: 1px solid #30363d;
                padding: 12px 24px;
                display: flex;
                align-items: center;
                gap: 16px;
            }}
            .navbar svg {{ fill: #e6edf3; }}
            .navbar-links {{
                display: flex;
                gap: 16px;
                margin-left: auto;
                align-items: center;
            }}
            .navbar-links a {{
                color: #e6edf3;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
            }}
            .navbar-links a:hover {{ color: #58a6ff; }}
            .avatar-small {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: 1px solid #30363d;
            }}
            .container {{
                max-width: 720px;
                margin: 40px auto;
                padding: 0 24px;
            }}
            .page-title {{
                font-size: 24px;
                font-weight: 600;
                margin-bottom: 4px;
            }}
            .page-sub {{
                font-size: 14px;
                color: #8b949e;
                margin-bottom: 24px;
            }}
            .card {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 0;
                overflow: hidden;
                margin-bottom: 16px;
            }}
            .card-header {{
                background: #21262d;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: 600;
                border-bottom: 1px solid #30363d;
            }}
            .data-row {{
                display: flex;
                justify-content: space-between;
                font-size: 14px;
                padding: 10px 16px;
                border-bottom: 1px solid #21262d;
            }}
            .data-row:last-child {{ border-bottom: none; }}
            .data-label {{ color: #8b949e; }}
            .data-value {{ color: #e6edf3; font-weight: 500; }}
            .badge-green {{
                display: inline-block;
                background: #238636;
                color: #e6edf3;
                font-size: 12px;
                font-weight: 500;
                padding: 2px 8px;
                border-radius: 20px;
            }}
            .btn {{
                display: inline-block;
                padding: 5px 16px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                text-decoration: none;
                border: 1px solid #30363d;
                background: #21262d;
                color: #e6edf3;
            }}
            .btn:hover {{ background: #30363d; }}
        </style>
    </head>
    <body>
        <nav class="navbar">
            <svg height="32" viewBox="0 0 16 16" width="32">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87
                2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95
                0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21
                2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04
                2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82
                2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0
                1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            <div class="navbar-links">
                <a href="/profile">Profile</a>
                <a href="/hello">Hello</a>
                <a href="/api/secure-data">Secure Data</a>
                <img class="avatar-small" src="{user.get('avatar_url')}" alt="avatar">
                <a href="/logout" style="color:#f85149;">Sign out</a>
            </div>
        </nav>

        <div class="container">
            <div class="page-title">Secure Data</div>
            <div class="page-sub">Protected endpoint — accessible only to authenticated users.</div>

            <div class="card">
                <div class="card-header">Access Details</div>
                <div class="data-row">
                    <span class="data-label">Status</span>
                    <span class="data-value"><span class="badge-green">Success</span></span>
                </div>
                <div class="data-row">
                    <span class="data-label">User</span>
                    <span class="data-value">@{user.get('login')}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Access Level</span>
                    <span class="data-value">Authenticated</span>
                </div>
            </div>

            <div class="card">
                <div class="card-header">Application Info</div>
                <div class="data-row">
                    <span class="data-label">Project</span>
                    <span class="data-value">Flask OAuth Lab</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Course</span>
                    <span class="data-value">System Integration and Architecture</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Provider</span>
                    <span class="data-value">GitHub OAuth 2.0</span>
                </div>
            </div>

            <a class="btn" href="/profile">Back to Profile</a>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)