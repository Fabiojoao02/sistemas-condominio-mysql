                  select con.nome conta, 
						cast(l.dt_leitura as date) as dt_leitura ,
						valor_m3, l.leitura_final, l.leitura_inicial,
                        ROUND((l.leitura_final - l.leitura_inicial),2) consumo_m3,
                        ROUND((l.leitura_final - l.leitura_inicial)*valor_m3,2) vl_consumo
                    from leituras l
                    join morador m on
                        m.id_morador = l.id_morador
                    join cadastro cad on
                        cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end
                    join bloco b on
                        b.id_bloco = m.id_bloco
                    join condominio c on
                        c.id_condominio = b.id_condominio
                    join contas con on
                        con.id_conta = l.id_contas
                    where l.id_morador = 1 
                    and l.dt_leitura >= cast(date_add(now(), INTERVAL -12 MONTH) as date) 
                    order by l.id_morador, conta 
                    
                    
        select concat(c.nome,'-',
                        CAST(ROUND((valor/
                        (select sum(valor) from calculos c1
                            where c1.mesano = cal.mesano  and c1.id_morador = cal.id_morador)*100),0) 
                            as varchar(50)),'%') Conta,
                        ROUND(valor,2) valor
                    from calculos cal
                    join contas c on
                        c.id_conta = cal.id_contas
                where cal.mesano = 022023 and cal.id_morador = 1
                
                              
        select concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                        ROUND(valor,2) valor
                    from calculos cal
                    join contas c on
                        c.id_conta = cal.id_contas
                where cal.id_morador = 1   and
                concat(right(cal.mesano,4),left(cal.mesano,2)) >= 
                replace(left(cast(date_add(now(), INTERVAL -12 MONTH) as date),7),'-','')
                group by mesano
                select concat(right('022023',4),left('022023',2))
                select replace(left(cast(date_add(now(), INTERVAL -12 MONTH) as date),7),'-','')
                
                select 202302 >= 202205