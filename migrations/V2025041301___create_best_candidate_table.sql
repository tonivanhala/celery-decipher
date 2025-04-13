CREATE TABLE best_candidates (
    source_text_id UUID NOT NULL PRIMARY KEY REFERENCES decipher_sources(source_text_id) ON DELETE CASCADE,
    candidate_id UUID NOT NULL,
    cipher_map JSONB NOT NULL,
    score FLOAT NOT NULL,
    deciphered_text TEXT NOT NULL
);
