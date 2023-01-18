CREATE TABLE Place
(
	place_id       INT       NOT NULL,
	place_country  char(10)  NOT NULL,
	place_state    char(10)  NULL
);

CREATE TABLE Info
(
	info_id            INT        NOT NULL,
   info_style         char(100)  NULL,
   info_availability  char(100)  NULL,
   info_abv           FLOAT      NULL,
   info_notes         char(1000) NULL

);

CREATE TABLE Beers
(
	beer_id       INT  NOT NULL,
	beer_name     char(100)  NOT NULL,
	place_id      INT  NOT NULL,
   info_id       INT  NOT NULL
);


-- -------------------
-- Define primary keys
-- -------------------
ALTER TABLE Place ADD PRIMARY KEY (place_id);
ALTER TABLE Info ADD PRIMARY KEY (info_id);
ALTER TABLE Beers ADD PRIMARY KEY (beer_id);


-- -------------------
-- Define foreign keys
-- -------------------
ALTER TABLE Beers ADD CONSTRAINT FK_Beers_Place FOREIGN KEY (place_id) REFERENCES Place (place_id);
ALTER TABLE Beers ADD CONSTRAINT FK_Beers_Info FOREIGN KEY (info_id) REFERENCES Info (info_id);