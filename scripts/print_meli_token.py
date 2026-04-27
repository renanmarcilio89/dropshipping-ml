from app.db.session import SessionLocal
from app.repositories.meli_credentials import MeliCredentialRepository

db = SessionLocal()

try:
    repo = MeliCredentialRepository(db)
    credential = repo.get_active()

    if credential is None:
        print("No Mercado Livre credentials found in the database.")
    else:
        print("user_id:", credential.user_id)
        print("nickname:", credential.nickname)
        print("expires_at:", credential.expires_at)
        print("access_token:", credential.access_token)
finally:
    db.close()