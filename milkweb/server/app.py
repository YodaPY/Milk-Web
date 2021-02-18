import hikari
from uuid import uuid4
from quart import Quart, url_for, session, redirect, request
from milkweb.server import get_redirect_url, get_user_token, APP_KEY, SCOPES

app = Quart(__name__)
app.secret_key = APP_KEY
rest = hikari.RESTApp()

@app.route("/")
async def hello() -> str:
    if not session.get("user"):
        session["user"] = {
            "cookie": str(uuid4())
        }

    return "hi"

@app.route("/login")
async def login():
    redirect_url = await get_redirect_url(
        state=session["user"]["cookie"]
    )

    return redirect(redirect_url)

@app.route("/callback")
async def callback():
    state = request.args.get("state")
    code = request.args.get("code")
    if state != session["user"]["cookie"]:
        return "Uh, what the fuck?", 403

    token = await get_user_token(
        code=code
    )

    session["user"]["token"] = token

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
async def dashboard():
    user = session.get("user")
    token = user.get("token")

    if not token:
        return redirect(url_for("login"))
    
    async with rest.acquire(token) as client:
        me = await client.fetch_my_user()
        return me

def run():
    app.run(debug=True)