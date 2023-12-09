-- PostgreSQL dump

CREATE DATABASE HSC;

\c HSC;

--
-- Table structure for table "Permissao"
--

DROP TABLE IF EXISTS "Permissao";
CREATE TABLE "Permissao" (
  "idPermissao" serial PRIMARY KEY,
  "tipoPermissao" varchar(45)
);

--
-- Table structure for table "Paciente"
--

DROP TABLE IF EXISTS "Paciente";
CREATE TABLE "Paciente" (
  "idPaciente" serial PRIMARY KEY,
  "nome" varchar(45),
  "sobreNome" varchar(45),
  "dataNascimento" date,
  "CPF" varchar(45) NOT NULL,
  "senha" varchar(200) NOT NULL,
  "dataCadastro" date,
  "telefone" varchar(12),
  "email" varchar(45),
  "genero" varchar(45),
  "Permissao_idPermissao" int NOT NULL REFERENCES "Permissao" ("idPermissao")
);

--
-- Table structure for table "Exame"
--

DROP TABLE IF EXISTS "Exame";
CREATE TABLE "Exame" (
  "idExame" serial PRIMARY KEY,
  "titulo" varchar(30) NOT NULL,
  "local" varchar(30),
  "protocolo" varchar(20),
  "dataExame" date,
  "medicoSolicitado" varchar(30),
  "informacoes" varchar(300),
  "Paciente_idPaciente" int REFERENCES "Paciente" ("idPaciente")
);

--
-- Table structure for table "Medico"
--

DROP TABLE IF EXISTS "Medico";
CREATE TABLE "Medico" (
  "idMedico" serial PRIMARY KEY,
  "nome" varchar(25),
  "CRM" varchar(12) NOT NULL,
  "UF" varchar(10) NOT NULL,
  "especializacao" varchar(20),
  "email" varchar(30) NOT NULL,
  "informacoes" varchar(100),
  "senha" varchar(200),
  "idPermissao_Permissao" int REFERENCES "Permissao" ("idPermissao")
);

--
-- Table structure for table "Compartilhado"
--

DROP TABLE IF EXISTS "Compartilhado";
CREATE TABLE "Compartilhado" (
  "idCompartilhado" serial PRIMARY KEY,
  "idExame_Exame" int REFERENCES "Exame" ("idExame"),
  "idMedico_Medico_Comp" int REFERENCES "Medico" ("idMedico")
);

--
-- Table structure for table "Imagem"
--

DROP TABLE IF EXISTS "Imagem";
CREATE TABLE "Imagem" (
  "id_imagem" serial PRIMARY KEY,
  "Exame_idExame" int REFERENCES "Exame" ("idExame"),
  "img" bytea NOT NULL,
  "name" varchar(100) NOT NULL,
  "mimetype" varchar(100) NOT NULL
);

--
-- Table structure for table "Endereco"
--

DROP TABLE IF EXISTS "Endereco";
CREATE TABLE "Endereco" (
  "idEndereco" serial PRIMARY KEY,
  "Logradouro" varchar(10) NOT NULL,
  "Numero" int NOT NULL,
  "CEP" varchar(8) NOT NULL,
  "complemento" varchar(45),
  "bairro" varchar(45) NOT NULL,
  "cidade" varchar(45) NOT NULL,
  "UF" varchar(2) NOT NULL,
  "endereco" varchar(60)
);

--
-- Table structure for table "Paciente_has_Endereco"
--

DROP TABLE IF EXISTS "Paciente_has_Endereco";
CREATE TABLE "Paciente_has_Endereco" (
  "Paciente_idUsuario" int REFERENCES "Paciente" ("idPaciente"),
  "Endereco_idEndereco" int REFERENCES "Endereco" ("idEndereco"),
  PRIMARY KEY ("Paciente_idUsuario", "Endereco_idEndereco")
);

--
-- Table structure for table "Paciente_has_Medico"
--

DROP TABLE IF EXISTS "Paciente_has_Medico";
CREATE TABLE "Paciente_has_Medico" (
  "idPaciHasMedico" serial PRIMARY KEY,
  "idPaciente_Paciente" int REFERENCES "Paciente" ("idPaciente"),
  "idMedico_Medico" int REFERENCES "Medico" ("idMedico")
);

--
-- Table structure for table "RX"
--

DROP TABLE IF EXISTS "RX";
CREATE TABLE "RX" (
  "idRX" serial PRIMARY KEY,
  "nomeExame" varchar(45) NOT NULL,
  "nomeMedico" varchar(45) NOT NULL,
  "dataRealizado" date NOT NULL,
  "clinica" varchar(45) NOT NULL,
  "Paciente_idPaciente" int REFERENCES "Paciente" ("idPaciente")
);

-- Dump completed on 2023-11-27 10:44:42
