from charades_app.extensions import app, db
from charades_app.main.routes import main
from charades_app.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)
