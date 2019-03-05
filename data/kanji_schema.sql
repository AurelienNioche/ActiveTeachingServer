-- Drop table

-- DROP TABLE kanji

CREATE TABLE kanji (
	"id" INT not null primary key,
	"Kanji" VARCHAR(255),
	"Strokes" INT,
	"Grade" INT,
	"Kanji Classification" VARCHAR(255),
	"JLPT-test" VARCHAR(255),
	"Name of Radical" VARCHAR(255),
	"Radical Freq." INT,
	"Reading within Joyo" VARCHAR(255),
	"Reading beyond Joyo" VARCHAR(255),
	"# of On" INT,
	"On within Joyo" VARCHAR(255),
	"Kanji ID in Nelson" INT,
	"# of Meanings of On" INT,
	"Translation of On" VARCHAR(1000),
	"# of Kun within Joyo with inflections" INT,
	"# of Kun within Joyo without inflections" INT,
	"Kun within Joyo" VARCHAR(255),
	"# of Meanings of Kun" INT,
	"Translation of Kun" VARCHAR(1000),
	"Year of Inclusion" INT,
	"Kanji Frequency with Proper Nouns" INT,
	"Acc. Freq. On with Proper Nouns" INT,
	"Acc. Freq. Kun with Proper Nouns" INT,
	"On Ratio with Proper Nouns" NUMERIC,
	"Acc. Freq. On beyond Joyo with Proper Nouns" INT,
	"Acc. Freq. Kun beyond Joyo with Proper Nouns" INT,
	"Acc. On Ratio beyond Joyo with Proper Nouns" NUMERIC,
	"Kanji Frequency without Proper Nouns" INT,
	"Acc. Freq. On without Proper Nouns" INT,
	"Acc. Freq. Kun without Proper Nouns" INT,
	"On Ratio without Proper Nouns" NUMERIC,
	"Acc. Freq. On beyond Joyo without Proper Nouns" INT,
	"Acc. Freq. Kun beyond Joyo without Proper Nouns" INT,
	"On Ratio beyond Joyo without Proper Nouns" NUMERIC,
	"Left Kanji Prod." INT,
	"Right Kanji Prod." INT,
	"Acc. Freq. Left Prod." INT,
	"Acc. Freq. Right Prod." INT,
	"Symmetry" VARCHAR(255),
	"Left Entropy" NUMERIC,
	"Right Entropy" NUMERIC,
	"Left1sound" VARCHAR(255),
	"Left1freq" INT,
	"Left2sound" VARCHAR(255),
	"Left2freq" INT,
	"Left3sound" VARCHAR(255),
	"Left3freq" INT,
	"Left4sound" VARCHAR(255),
	"Left4freq" INT,
	"Left5sound" VARCHAR(255),
	"Left5freq" INT,
	"Left6sound" VARCHAR(255),
	"Left6freq" INT,
	"Right1sound" VARCHAR(255),
	"Right1freq" INT,
	"Right2sound" VARCHAR(255),
	"Right2freq" INT,
	"Right3sound" VARCHAR(255),
	"Right3freq" INT,
	"Right4sound" VARCHAR(255),
	"Right4freq" INT,
	"Right5sound" VARCHAR(255),
	"Right5freq" INT,
	"Right6sound" VARCHAR(255),
	"Right6freq" INT,
	"Right7sound" VARCHAR(255),
	"Right7freq" INT
);
