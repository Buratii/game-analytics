-- Criação do banco de dados já está no docker-compose

-- Tabela para armazenar contagem de eventos por tipo
CREATE TABLE IF NOT EXISTS event_counts (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    total_events BIGINT NOT NULL,
    processed_at TIMESTAMP NOT NULL
);

-- Tabela para armazenar usuários únicos por tipo de evento
CREATE TABLE IF NOT EXISTS unique_users (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    unique_users BIGINT NOT NULL,
    processed_at TIMESTAMP NOT NULL
);

-- Tabela para armazenar tempo médio entre eventos por usuário
CREATE TABLE IF NOT EXISTS avg_time_between_events (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    avg_time_between_events_seconds DOUBLE PRECISION NOT NULL,
    processed_at TIMESTAMP NOT NULL
);

-- Índices para melhorar performance das consultas
CREATE INDEX IF NOT EXISTS idx_event_counts_event_type ON event_counts(event_type);
CREATE INDEX IF NOT EXISTS idx_unique_users_event_type ON unique_users(event_type);
CREATE INDEX IF NOT EXISTS idx_avg_time_user_id ON avg_time_between_events(user_id);