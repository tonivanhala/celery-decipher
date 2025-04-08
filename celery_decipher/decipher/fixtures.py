import json

ROT13_MISSING_LETTER = {
    k: v
    for k, v in zip(
        "abcdefghijklmopqrstuvwxy",
        "nopqrstuvwxyzabcdefghijkl",
    )
}

CHURCHILL = """
We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets,
we shall fight in the hills; we shall never surrender.
"""

CHURCHILL_ROT13 = """
Jr funyy svtug ba gur ornpurf, jr funyy svtug ba gur ynaqvat tebhaqf, jr funyy svtug va gur svryqf naq va gur fgerrgf,
jr funyy svtug va gur uvyyf; jr funyy arire fheeraqre.
"""

MANNERHEIM = """
Meillä on ylpeä tietoisuus siitä, että meillä on historiallinen tehtävä, jonka me edelleen täytämme:
länsimaisen sivistyksen suojaaminen, joka vuosisatoja on ollut meidän perintömme, mutta me tiedämme myös,
että olemme viimeistä penniä myöten maksaneet velan, mikä meillä siitä länteen on ollut.
"""

MLK = """
Let us not wallow in the valley of despair, I say to you today, my friends.

And so even though we face the difficulties of today and tomorrow, I still have a dream. It is a dream deeply rooted in the American dream.

I have a dream that one day this nation will rise up and live out the true meaning of its creed: "We hold these truths to be self-evident, that all men are created equal."

I have a dream that one day on the red hills of Georgia, the sons of former slaves and the sons of former slave owners will be able to sit down together at the table of brotherhood.

I have a dream that one day even the state of Mississippi, a state sweltering with the heat of injustice, sweltering with the heat of oppression, will be transformed into an oasis of freedom and justice.

I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.

I have a dream today!

I have a dream that one day, down in Alabama, with its vicious racists, with its governor having his lips dripping with the words of "interposition" and "nullification" -- one day right there in Alabama little black boys and black girls will be able to join hands with little white boys and white girls as sisters and brothers.

I have a dream today!

I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight; "and the glory of the Lord shall be revealed and all flesh shall see it together."
"""

most_common_english_letters: list[str] = [
    "e",
    "t",
    "a",
    "i",
    "n",
    "o",
    "s",
    "r",
    "l",
    "d",
    "h",
    "c",
    "u",
    "m",
    "f",
    "p",
    "y",
    "g",
    "w",
    "v",
    "b",
    "k",
    "x",
    "j",
    "q",
    "z",
]


most_common_english_words: list[str] = []
for line in open("./celery_decipher/decipher/dictionary.txt", "r"):
    word = line.strip().lower()
    if len(word) > 0:
        most_common_english_words.append(word)


most_common_english_bigrams: dict[str, int] = {}
with open("./celery_decipher/decipher/bigrams.json", "r") as f:
    english_bigrams = json.load(f)
    for bigram, freq in english_bigrams:
        most_common_english_bigrams[bigram] = freq
