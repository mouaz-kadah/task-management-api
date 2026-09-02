from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# غيّر username و password بـ الـ credentials تبعك
DATABASE_URL = "mysql+mysqlconnector://root:121538@localhost:3306/task_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()