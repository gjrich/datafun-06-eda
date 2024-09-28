-- Start by deleting any tables if the exist already
-- We want to be able to re-run this script as needed.
-- DROP tables in reverse order of creation 
-- DROP dependent tables (with foreign keys) first

DROP TABLE IF EXISTS cardetails;


-- To create a table where a row number serves as the primary key, 
-- you can use INTEGER PRIMARY KEY AUTOINCREMENT. 
-- This allows SQLite to automatically generate a unique row number for each record. 
-- The ROW column will be renamed to a more conventional name like id

CREATE TABLE cardetails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Make TEXT,
    Model TEXT,
    Price INTEGER,
    Year INTEGER,
    Kilometer INTEGER,
    Fuel_Type TEXT,
    Transmission TEXT,
    Location TEXT,
    Color TEXT,
    Owner TEXT,
    Seller_Type TEXT,
    Engine TEXT,
    Max_Power TEXT,
    Max_Torque TEXT,
    Drivetrain TEXT,
    Length REAL,
    Width REAL,
    Height REAL,
    Seating_Capacity REAL,
    Fuel_Tank_Capacity REAL
);
