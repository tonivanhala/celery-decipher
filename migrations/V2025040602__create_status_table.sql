CREATE TYPE decipher_status_enum AS ENUM (
    'PROCESSING',
    'COMPLETED'
);

CREATE TABLE decipher_status (
    source_text_id UUID NOT NULL,
    status decipher_status_enum NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_text_id) REFERENCES decipher_sources(source_text_id) ON DELETE CASCADE
)
