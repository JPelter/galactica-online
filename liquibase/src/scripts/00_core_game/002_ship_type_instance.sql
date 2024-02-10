CREATE TABLE SHIP_TYPE (
    id IDENTITY PRIMARY KEY,
    [name] NVARCHAR(100) UNIQUE,

    crypto_cost INT DEFAULT 0 NOT NULL,
    crypto_production INT DEFAULT 0 NOT NULL,
    max_health INT NOT NULL,
    max_cargo_capacity INT NOT NULL,
    attack_power INT DEFAULT 0 NOT NULL,
    armor_level INT DEFAULT 0 NOT NULL,
    warp_speed_factor INT DEFAULT 100 NOT NULL,
    speed INT DEFAULT 0 NOT NULL

);

CREATE TABLE SHIP_RESOURCE_NET_MAINTENANCE_COST (
    ship_type_id REFERENCES SHIP_TYPE(id),
    resource_id REFERENCES [RESOURCE](id),
    PRIMARY KEY (ship_type_id, resource_id),

    net_cost INT NOT NULL -- NEGATIVE NUMBER IS MAINTENACE COST, POSITIVE NUMBER IS INTERPRETED AS PRODUCTION (RARE FOR SHIP PROBABLY?)!
);

CREATE TABLE SHIP (
    id IDENTITY PRIMARY KEY,
    local_time = DATETIME2 NOT NULL,
    ship_type_id REFERENCES SHIP_TYPE(id),
    system_id REFERENCES [SYSTEM](id) NOT NULL,
    health INT NOT NULL,

    warp_target_id REFERENCES [SYSTEM](id),
    warp_target_progress INT
)

CREATE TABLE SHIP_CARGO (
    ship_id REFERENCES SHIP_TYPE(id),
    resource_id REFERENCES [RESOURCE](id),
    PRIMARY KEY (ship_id, resource_id),

    trade_volume INT DEFAULT 0 NOT NULL,
    trade_value INT DEFAULT 0 NOT NULL
)