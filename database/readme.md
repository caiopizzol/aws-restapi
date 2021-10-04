# RDS Database Setup

## Creating Tables
CREATE TABLE languages (
	id serial PRIMARY KEY,
	language VARCHAR ( 50 ) NOT NULL,
	code VARCHAR ( 2 ) NOT NULL
);

CREATE TABLE currencies (
	id serial PRIMARY KEY,
	currency VARCHAR ( 50 ) NOT NULL,
	code VARCHAR ( 3 ) NOT NULL
);

CREATE TABLE providers (
	id serial PRIMARY KEY,
	name VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	phone VARCHAR ( 50 ),
    language_id INT NOT NULL,
    currency_id INT NOT NULL,
    FOREIGN KEY(language_id) 
	    REFERENCES languages(id),
    FOREIGN KEY(currency_id) 
	    REFERENCES currencies(id)
);

CREATE EXTENSION postgis;

CREATE TABLE providers_service_areas (
    id serial PRIMARY KEY,
    name VARCHAR ( 50 ) NOT NULL,
    price NUMERIC NOT NULL,
    polygon GEOMETRY NOT NULL,
    provider_id INT,
    FOREIGN KEY(provider_id) 
	    REFERENCES providers(id)
);   

CREATE INDEX polygon_idx ON providers_service_areas USING GIST (polygon);

## Inserting Values

Following ISO 639-1
```
INSERT INTO languages (code, language) VALUES
    ('de', 'German'),
    ('en', 'English'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('pt', 'Portuguese'),
    ('zh', 'Chinese');
```

Following ISO 4217
```
INSERT INTO currencies (code, currency) VALUES 
    ('EUR', 'Euro'),
    ('USD', 'US Dollar'),
    ('JPY', 'Yen'),
    ('BRL', 'Brazilian Real'),
    ('CNY', 'Yuan Renminbi');
```

## Queries

### Getting Providers
SELECT * FROM providers WHERE id = %s;
SELECT * FROM providers WHERE email = %s;

### Inserting Providers
INSERT INTO providers (name, email, language, currency) VALUES ();

### Updating Providers
UPDATE providers SET phone = '' WHERE id = %s;
UPDATE providers SET phone = '' WHERE email = %s;

### Deleting Providers
DELETE FROM providers WHERE id = %s;
DELETE FROM providers WHERE email = %s;