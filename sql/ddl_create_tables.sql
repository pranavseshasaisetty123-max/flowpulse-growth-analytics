-- Schema definition for FlowPulse growth analytics

CREATE TABLE customers (
    customer_id            BIGINT PRIMARY KEY,
    signup_date            DATE NOT NULL,
    country                VARCHAR(10),
    device_type            VARCHAR(20),
    segment                VARCHAR(50),
    acquisition_channel_id BIGINT,
    churned_date           DATE,
    is_active              BOOLEAN
);

CREATE TABLE marketing_channels (
    channel_id    BIGINT PRIMARY KEY,
    channel_name  VARCHAR(50),
    campaign_name VARCHAR(100),
    utm_medium    VARCHAR(50),
    utm_source    VARCHAR(50),
    cac_usd       NUMERIC(10, 2)
);

CREATE TABLE subscriptions (
    subscription_id         BIGINT PRIMARY KEY,
    customer_id             BIGINT REFERENCES customers (customer_id),
    plan_name               VARCHAR(20) NOT NULL,
    subscription_start_date DATE NOT NULL,
    subscription_end_date   DATE,
    is_active               BOOLEAN,
    billing_period          VARCHAR(20),
    trial_start_date        DATE,
    trial_end_date          DATE,
    churn_reason            VARCHAR(50)
);

CREATE TABLE payments (
    payment_id      BIGINT PRIMARY KEY,
    subscription_id BIGINT REFERENCES subscriptions (subscription_id),
    payment_date    DATE NOT NULL,
    amount_usd      NUMERIC(10, 2) NOT NULL,
    payment_status  VARCHAR(20) NOT NULL,
    payment_method  VARCHAR(20),
    invoice_id      VARCHAR(50),
    is_renewal      BOOLEAN
);

CREATE TABLE user_events (
    event_id           BIGINT PRIMARY KEY,
    customer_id        BIGINT REFERENCES customers (customer_id),
    event_timestamp    TIMESTAMP NOT NULL,
    event_type         VARCHAR(50),
    device_type        VARCHAR(20),
    plan_name_at_event VARCHAR(20),
    session_id         VARCHAR(100)
);

