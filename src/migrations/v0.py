from yoyo import step


__depends__ = {}

steps = [
    step(
        apply="""
        CREATE TABLE IF NOT EXISTS customer (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL
        );
        """,
        rollback="""
        DROP TABLE customer;
        """,
    ),
]
