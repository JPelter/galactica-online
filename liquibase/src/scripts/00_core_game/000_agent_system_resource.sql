CREATE TABLE AGENT (
    id IDENTITY PRIMARY KEY,
    [name] NVARCHAR(100) UNIQUE,
    crypto INT DEFAULT 0 NOT NULL,

    controller_email NVARCHAR(100),
    last_login DATETIME2,
    current_login_token CHAR(6)
);

CREATE TABLE SYSTEM (
    id IDENTITY PRIMARY KEY,
    local_time = DATETIME2 NOT NULL,
    [name] NVARCHAR(100) UNIQUE,
    crypto INT DEFAULT 0 NOT NULL,
    [population] INT NOT NULL,
    x_coordinate INT NOT NULL,
    y_coordinate INT NOT NULL
);

CREATE TABLE RESOURCE(
    id IDENTITY PRIMARY KEY,
    resource_name NVARCHAR(100) UNIQUE,
    population_demand INT DEFAULT 0
);

CREATE TABLE SYSTEM_RESOURCE_STOCKPILE (
    system_id REFERENCES [SYSTEM](id),
    resource_id REFERENCES RESOURCE(id),
    PRIMARY KEY (system_id, resource_id),
    quantity INT DEFAULT 0 NOT NULL,

    trade_volume INT DEFAULT 0 NOT NULL,
    trade_value INT DEFAULT 0 NOT NULL
);