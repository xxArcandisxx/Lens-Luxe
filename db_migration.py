from app import app, db
from sqlalchemy import text

with app.app_context():
    db.session.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS bio VARCHAR(500) DEFAULT \'\';'))
    db.session.commit()
    print('Database altered successfully!')
