from sqlalchemy.orm import Session
import time
import datetime
from .settings import settings
from .models import Code
from .db import SessionLocal

last_cron = 0

def cron(db: Session = None, force: bool = False):
    global last_cron
    opened_db = False

    if not db:
        db = SessionLocal()
        opened_db = True

    if time.time() < last_cron + settings.cron_interval and not force:
        print("skip cron")
        return 
    print("CRON")

    # delete expired codes
    n = db.query(Code).filter(Code.expires < datetime.datetime.now()).delete()    
    if n:
        print(f"Cron deleted {n} expired codes")
    db.commit()

    if opened_db:
        db.close()

    last_cron = time.time()