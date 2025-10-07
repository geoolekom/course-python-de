from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:secret@localhost:3306/python-de"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log all SQL queries
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Additional connections
)

# Test connection
with engine.connect() as connection:
    with connection.begin():
        sql = text("INSERT INTO users (username, email) VALUES (:username, :email)")
        params = {"username": "john", "email": "john@company.com"}
        result = connection.execute(sql, params)
