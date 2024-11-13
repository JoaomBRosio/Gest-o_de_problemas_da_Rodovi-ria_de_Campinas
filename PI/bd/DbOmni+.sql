CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  senha VARCHAR(255) NOT NULL
);

CREATE TABLE funcionarios (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  cargo VARCHAR(50) NOT NULL
);

CREATE TABLE problemas (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(255) NOT NULL,
  descricao TEXT NOT NULL,
  status VARCHAR(50),
  data_reportado TIMESTAMP,
  data_verificado TIMESTAMP,
  local VARCHAR(255),
  imagem VARCHAR(255),  -- campo para armazenar o caminho da imagem
  usuario_id INTEGER,
  funcionario_id INTEGER,
  CONSTRAINT fk_usuario
    FOREIGN KEY (usuario_id)
    REFERENCES usuarios (id),
  CONSTRAINT fk_funcionario
    FOREIGN KEY (funcionario_id)
    REFERENCES funcionarios (id)
);

CREATE TABLE notificacoes (
  id SERIAL PRIMARY KEY,
  problema_id INTEGER,
  funcionario_id INTEGER,
  data_notificacao TIMESTAMP,
  status VARCHAR(50),
  CONSTRAINT fk_problema
    FOREIGN KEY (problema_id)
    REFERENCES problemas (id),
  CONSTRAINT fk_funcionario_notif
    FOREIGN KEY (funcionario_id)
    REFERENCES funcionarios (id)
);

CREATE TABLE audios (
  id SERIAL PRIMARY KEY,
  caminho_arquivo VARCHAR(255),
  problema_id INTEGER,
  CONSTRAINT fk_problema_audio
    FOREIGN KEY (problema_id)
    REFERENCES problemas (id)
);

ALTER TABLE usuarios 
ADD COLUMN tipo_usuario VARCHAR(50) NOT NULL;


-- Desabilitar temporariamente a checagem de constraints de chave estrangeira
DO $$ 
DECLARE
    r RECORD;
BEGIN
    -- Excluir todas as tabelas
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;

ALTER TABLE problemas 
ALTER COLUMN imagem SET DATA TYPE BYTEA 
USING imagem::bytea;








