CREATE TABLE Teams (
    ID int NOT NULL AUTO_INCREMENT, 
    Domain varchar(255) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Players (
    ID int NOT NULL AUTO_INCREMENT, 
    TeamID int NOT NULL,
    Name varchar(255) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (TeamID) REFERENCES Teams(ID)
);

CREATE TABLE Games (
    ID int NOT NULL AUTO_INCREMENT, 
    TeamID int NOT NULL,
    Name varchar(255) NOT NULL,
    Sort int NOT NULL DEFAULT 1,
    Archived bit DEFAULT 0,
    PRIMARY KEY (ID),
    FOREIGN KEY (TeamID) REFERENCES Teams(ID)
);

CREATE TABLE Scores (
    GameID int NOT NULL, 
    PlayerID int NOT NULL,
    Score DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (GameID, PlayerID),
    FOREIGN KEY (GameID) REFERENCES Games(ID),
    FOREIGN KEY (PlayerID) REFERENCES Players(ID)
);

CREATE TABLE Screenshots (
	GameID int NOT NULL, 
    PlayerID int NOT NULL,
    ImgURL varchar(255) NOT NULL,
    PRIMARY KEY (GameID, PlayerID),
    FOREIGN KEY (GameID, PlayerID) REFERENCES Scores(GameID, PlayerID)
);
