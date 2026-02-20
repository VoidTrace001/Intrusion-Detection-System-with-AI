from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./ids_database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """Admin Authentication System."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class TrafficLog(Base):
    """7️⃣ Database Design: Store structured traffic logs."""
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    src_ip = Column(String)
    dst_ip = Column(String)
    protocol = Column(String)
    length = Column(Integer)
    flags = Column(String)
    flow_duration = Column(Float)
    prediction = Column(String)
    confidence = Column(Float)
    attack_type = Column(String)
    risk_score = Column(Float)

class DetectedAttack(Base):
    """7️⃣ Database Design: Store detected attacks for quick alerts."""
    __tablename__ = "detected_attacks"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    src_ip = Column(String)
    dst_ip = Column(String)
    attack_type = Column(String)
    risk_score = Column(Float)
    confidence = Column(Float)
    alert_status = Column(String, default="unseen") # 8️⃣ Alert System

class ModelMetric(Base):
    """7️⃣ Database Design: Store model performance metrics."""
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    train_date = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
