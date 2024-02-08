CREATE TABLE ACCOUNT (
    id IDENTITY PRIMARY KEY,
    agent_name NVARCHAR(100) UNIQUE,
    wallet INT DEFAULT 0,

    email NVARCHAR(100),
    last_login DATETIME2,
    current_login_token CHAR(6)
);