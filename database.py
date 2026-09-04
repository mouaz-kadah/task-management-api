from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# غيّر username و password بـ الـ credentials تبعك
DATABASE_URL = "postgresql://admin:PASSWORD@dpg-dadk3cn40uj673bq8uv0-a:5432/task_management_joq5"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()