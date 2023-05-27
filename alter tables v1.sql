alter table movimento add id_bloco int not null
CONSTRAINT `id_bloco_mov_fk` FOREIGN KEY (`id_bloco`) REFERENCES `bloco` (`id_bloco`) ON DELETE CASCADE ON UPDATE CASCADE

alter table leituras add id_bloco int not null
update leituras set id_bloco = 2 where id_leituras>=1
ALTER TABLE `leituras` ADD  CONSTRAINT `id_bloco_lei_fk` FOREIGN KEY (`id_bloco`) REFERENCES `bloco`(`id_bloco`) ON DELETE RESTRICT ON UPDATE RESTRICT;
alter table calculos  add id_bloco int not null;
update calculos set id_bloco = 2 where id_calculos>=1;
ALTER TABLE `calculos` ADD  CONSTRAINT `id_bloco_Calc_fk` FOREIGN KEY (`id_bloco`) REFERENCES `bloco`(`id_bloco`) ON DELETE RESTRICT ON UPDATE RESTRICT;
alter table movimento add situacao varchar(1) not null default 'A'
CONSTRAINT `id_bloco_lei_fk` FOREIGN KEY (`id_bloco`) REFERENCES `bloco` (`id_bloco`) ON DELETE CASCADE ON UPDATE CASCADE


select * from leituras
update leituras set id_bloco = 2 where id_leituras>=1


alter table condominio add responsavel_pix varchar(50) null
alter table condominio add chave_pix varchar(50) null
alter table condominio add txtid_pix varchar(50) null

alter table contas add leituras tinyint(1) not null default 0
update contas SET leituras=1 where id_conta = 3
#alter table movimento drop column mov_gerado tinyint(1) not null default 0

##alter table movimento drop column mensagem varchar(4000) null


create table movimento_msg
(
id_movimento_msg int(11) primary key NOT NULL AUTO_INCREMENT,
mesano varchar(6) not null,
mensagem varchar(100) not null,
CONSTRAINT `id_mov_msg_fk` FOREIGN KEY (`mesano`) REFERENCES `movimento` (`mesano`) ON DELETE CASCADE ON UPDATE CASCADE
)


CREATE TABLE `movimento` (
  `id_movimento` int(11) NOT NULL AUTO_INCREMENT,
  `mesano` varchar(6) NOT NULL,
  `id_contas` int(11) NOT NULL,
  `valor` float NOT NULL,
  `id_tipo_calculo` int(11) NOT NULL,
  `dt_lancamento` datetime NOT NULL DEFAULT current_timestamp(),
  `id_bloco` int(11) NOT NULL,
  PRIMARY KEY (`id_movimento`),
  UNIQUE KEY `idx_mesano_tipo_conta_movimento` (`mesano`,`id_contas`),
  KEY `id_contas_movimento_fk` (`id_contas`),
  KEY `id_tipocalculo_mov_fk` (`id_tipo_calculo`),
  KEY `id_bloco_mov_fk` (`id_bloco`),
  CONSTRAINT `id_bloco_mov_fk` FOREIGN KEY (`id_bloco`) REFERENCES `bloco` (`id_bloco`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `id_contas_movimento_fk` FOREIGN KEY (`id_contas`) REFERENCES `contas` (`id_conta`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_tipocalculo_mov_fk` FOREIGN KEY (`id_tipo_calculo`) REFERENCES `tipo_calculo` (`id_tipo_calculo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;