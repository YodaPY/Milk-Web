import hikari
import asyncio
from secrets import token_urlsafe
from quart import Quart, url_for, session, redirect, request, jsonify
from milkweb.server import get_redirect_url, get_user_token, APP_SECRET, SCOPES, NotAuthorized

app = Quart(__name__)
app.secret_key = APP_SECRET
rest = hikari.RESTApp()

def requires_authorization(func):
    async def is_authorized():
        with app.app_context():
            token = session.get("token")
            if not token:
                raise NotAuthorized

            await func()
    
    return asyncio.run(is_authorized())

@app.route("/")
async def hello() -> str:
    if not session.get("state"):
        session["state"] = token_urlsafe(20)

    return "hi"

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
async def dashboard():
    token = session.get("token")

    if not token:
        return redirect(url_for("login"))
    
    async with rest.acquire(token) as client:
        guilds = await client.fetch_my_guilds()

    return jsonify([g.name for g in guilds])

def run():
    app.run(debug=True)