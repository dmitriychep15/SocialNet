from flask_sqlalchemy import SQLAlchemy


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:jmh990@database:5432/NetUsers"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(dict(
        DATABASE="postgresql+psycopg2://postgres:jmh990@database:5432/NetUsers",
        DEBUG=False,
        SECRET_KEY='development key',
    ))

    db = SQLAlchemy(app)
    db.init_app(app)
    app.config["db"] = db

    return db
