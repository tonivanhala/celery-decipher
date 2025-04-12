CREATE TABLE candidates (
    candidate_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_text_id UUID NOT NULL,
    cipher_map JSONB NOT NULL
)
