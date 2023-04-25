          select 
				(select count(*) from bloco where id_condominio = cd.id_condominio) qde_blocos,
                (select count(*) from morador where id_bloco = bl.id_bloco and situacao='A') qde_condomonio,
                (select sum(qt_moradores) from morador where id_bloco = bl.id_bloco and situacao='A') qt_moradores,
                (select max(mesano)  from calculos) max_mesano,
                (select ROUND(sum(valor),2) from calculos ca where mesano = max(mesano)) valor_total
            from bloco bl 
            
            
            select count(*) qde_condominios from condominio;
            select count(*) qde_blocos from bloco
            select count(*) qde_morador from morador
            select sum(qt_moradores) qt_moradores from morador
            select ROUND(sum(valor),2) valor_total from movimento
            