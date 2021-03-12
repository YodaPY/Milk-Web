import hikari
import asyncio
import functools
from secrets import token_urlsafe
from quart import Quart, url_for, session, redirect, request, jsonify, render_template
from milkweb import get_redirect_url, get_user_token, APP_SECRET, SCOPES, NotAuthorized

app = Quart(__name__)
app.secret_key = APP_SECRET
rest = hikari.RESTApp()

def requires_authorization(func):
    @functools.wraps(func)
    async def is_authorized(*args, **kwargs):
        async with app.app_context():
            token = session.get("token")
            if not token:
                raise NotAuthorized

            return await func(token, *args, **kwargs)
    
    return is_authorized

@app.errorhandler(NotAuthorized)
async def handle_authorization_error(error):
    return redirect(url_for("login"))

@app.route("/")
async def hello() -> str:
    if not session.get("state"):
        session["state"] = token_urlsafe(20)

    return await render_template("index.html")

@app.route("/login")
async def login():
    redirect_url = await get_redirect_url(
        state=session["state"]
    )

    return redirect(redirect_url)

@app.route("/callback")
async def callback():
    state = request.args.get("state")
    code = request.args.get("code")
    if state != session["state"]:
        return "Uh, what the fuck?", 403

    token = await get_user_token(
        code=code
    )

    session["token"] = token

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
@requires_authorization
async def dashboard(token):
    async with rest.acquire(token) as client:
        my_user = await client.fetch_my_user()
        guilds = await client.fetch_my_guilds()

    return await render_template("dashboard.html", user=my_user, guilds=guilds)

@app.route("/dashboard/<int:guild_id>")
@requires_authorization
async def dashboard_for_guild(token, guild_id):
    return str(guild_id)

def run():
    app.run(debug=True)