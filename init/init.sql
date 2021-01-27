SET TIME ZONE -5;
CREATE USER forecaster WITH PASSWORD 'forecaster';

CREATE DATABASE spx_forecaster;
GRANT ALL PRIVILEGES ON DATABASE spx_forecaster TO forecaster;

\c spx_forecaster forecaster;

CREATE TABLE news_stock(
    date TIMESTAMP,
    headline TEXT,
    open FLOAT(24),
    high FLOAT(24),
    low FLOAT(24),
    close FLOAT(24),
    adj_close FLOAT(24),
    volume FLOAT(24),
    diff FLOAT(24),
    label SMALLINT
    );

\copy news_stock (date, headline, open, high, low, close, adj_close, volume, diff, label) from '/var/lib/postgresql_/csvs/news_stock.csv' DELIMITER ',' CSV HEADER;