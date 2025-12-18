"""
Database update script - Deploy 2029
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def update_user_tier():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Update user plan to PRO
        result = conn.execute(
            text("UPDATE users SET plan = 'PRO' WHERE email = 'inqgmaerz48@gmail.com'")
        )
        conn.commit()
        
        if result.rowcount > 0:
            print(f"✅ Updated user to PRO tier")
        else:
            print(f"❌ User not found")

if __name__ == "__main__":
    update_user_tier()
