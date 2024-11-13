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
  imagem VARCHAR(255),
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


DO $$ 
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;

ALTER TABLE problemas 
ALTER COLUMN imagem SET DATA TYPE BYTEA 
USING imagem::bytea;

select * from problemas;

select * from usuarios;

delete from problemas;

delete from usuarios;

ALTER TABLE problemas ADD COLUMN visualizado BOOLEAN DEFAULT FALSE;

ALTER TABLE problemas ADD COLUMN resolvido BOOLEAN DEFAULT FALSE;

ALTER TABLE problemas ADD COLUMN resolvido BOOLEAN DEFAULT FALSE;

ALTER TABLE problemas ADD COLUMN setor CHAR(1) CHECK (setor IN ('A', 'B'));

ALTER TABLE problemas ADD COLUMN verificado BOOLEAN DEFAULT FALSE;

ALTER TABLE problemas ADD COLUMN falso BOOLEAN DEFAULT FALSE;

ALTER TABLE problemas ADD COLUMN setor CHAR(1) CHECK (setor IN ('A', 'B')) NOT NULL DEFAULT 'A';

ALTER TABLE problemas ADD COLUMN visualizado BOOLEAN DEFAULT FALSE;

CREATE TABLE audios (
  id SERIAL PRIMARY KEY,
  caminho_arquivo VARCHAR(255),
  problema_id INTEGER,
  descricao_audio TEXT,  -- novo campo para armazenar a descrição do áudio
  CONSTRAINT fk_problema_audio
    FOREIGN KEY (problema_id)
    REFERENCES problemas (id)
);

ALTER TABLE problemas 
ADD COLUMN setor_id INTEGER REFERENCES setores(id);
