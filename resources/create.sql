CREATE TABLE Technicians (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Technicians,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Customers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE AC (
    Brand varchar(255),
    Quantity int,
    PRIMARY KEY (Brand)
);

CREATE TABLE Appointment (
    AppID int AUTO_INCREMENT,
    Customer varchar(255) REFERENCES Customers(Username),
    Time date,
    AC varchar(255) REFERENCES AirConditioners(Brand),
    Technician varchar(255) REFERENCES Technicians(Username),
    PRIMARY KEY (AppID)
);


