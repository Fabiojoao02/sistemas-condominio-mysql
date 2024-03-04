CREATE DEFINER=`vacom_fabiojoao`@`%` PROCEDURE `prc_calcula_movimento`(IN v_mes_ano varchar(6), v_bloco int)
BEGIN
	DECLARE done INT default FALSE;
	DECLARE v_qt, v_t_morador,v_id_morador, v_qt_moradores,v_qtMov integer;
	DECLARE v_fundo_reserva, v_taxa_condominio, v_fracao_ideal float;
    DECLARE v_mesano_ant varchar(6);
    
    -- ===================
	-- Declare o cursos
	DECLARE cur_cal CURSOR FOR
		select m.id_morador,
			b.fundo_reserva,
			b.taxa_condominio,
			b.fracao_ideal,
			m.qt_moradores
		FROM condominio c
			JOIN bloco b ON b.id_condominio = c.id_condominio
			JOIN morador m ON m.id_bloco = b.id_bloco
		where m.situacao = 'A' and b.id_bloco = v_bloco;    
    -- ===================
	-- declare NOT FOUND handler
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
		
    -- ===================
	-- cria tabela temporaria 
	CREATE TEMPORARY TABLE IF NOT EXISTS tmp_calculo AS (
		select m.id_morador,
			b.fundo_reserva,
			b.taxa_condominio,
			b.fracao_ideal,
			m.qt_moradores
		FROM condominio c
			JOIN bloco b ON b.id_condominio = c.id_condominio
			JOIN morador m ON m.id_bloco = b.id_bloco
		where m.situacao = 'A'  and b.id_bloco = v_bloco  
	);
	set v_qt = 0;
	set v_t_morador = 0;
	select count(*), SUM(qt_moradores) into v_qt, v_t_morador from tmp_calculo;
    -- ===================
    -- Limpa os calculos existentes no mes e ano corrente
    delete from calculos_morador where id_bloco = v_bloco and mesano = v_mes_ano and id_morador in(select id_morador from calculos  where  mesano = v_mes_ano and id_bloco = v_bloco);
	delete from calculos  where  mesano = v_mes_ano and id_bloco = v_bloco  and id_contas in (select id_contas from movimento where mesano = v_mes_ano and id_bloco = v_bloco);
    delete from calculos  where  mesano = v_mes_ano and id_bloco = v_bloco  and id_contas in(select id_conta from contas where leituras=1);   
	OPEN cur_cal ;
    -- ===================
    -- inicio do LOOP
	read_loop:
	LOOP
		fetch cur_cal into v_id_morador,v_fundo_reserva,v_taxa_condominio,v_fracao_ideal,v_qt_moradores;
		IF done THEN
		  LEAVE read_loop;
		END IF;
		-- ===================
		-- lança conta v_fundo_reserva-9
        if v_fundo_reserva > 0 then
			insert into calculos (mesano,id_contas, id_morador, id_bloco, valor) 
			SELECT mesano, id_contas , v_id_morador, id_bloco, ROUND(format((valor/10)*1, 2),2)
			FROM movimento where situacao <> 'F' and id_contas in(9) and id_bloco = v_bloco;            
        end if;    
		-- ===================
		-- lança conta v_taxa_condominio-10
        if v_taxa_condominio > 0 then
			insert into calculos (mesano,id_contas, id_morador, valor, id_bloco) 
			SELECT mesano, id_contas , v_id_morador, ROUND(format((valor/10)*1, 2),2), id_bloco
			FROM movimento where situacao <> 'F' and id_contas in(10) and id_bloco = v_bloco;            
        end if;    
		-- ===================
		-- lança demais contas
		insert into calculos (mesano,id_contas, id_morador, id_bloco, valor) 
		SELECT mesano, id_contas, v_id_morador, id_bloco,
		CASE WHEN id_tipo_calculo = 1 then ROUND((valor/v_qt)* v_fracao_ideal,2) 
			WHEN id_tipo_calculo = 2 then ROUND(((valor/v_t_morador) * v_qt_moradores)* v_fracao_ideal,2)    
			ELSE  ROUND(format(valor, 2),2)  END   
		FROM movimento 
		where id_contas not in(9,10) and mesano = v_mes_ano and id_bloco = v_bloco and situacao <> 'F';
        
        if not exists(select 1 from calculos_morador where id_bloco = v_bloco and mesano = v_mes_ano and id_morador = v_id_morador) then
			insert into calculos_morador (id_morador, id_bloco, mesano, qt_morador) values (v_id_morador,v_bloco,v_mes_ano,v_qt_moradores);
        end if;     
	END LOOP read_loop;
	CLOSE cur_cal ;
    -- ===================
	-- lançamento de gas
	insert into calculos (mesano,id_contas, id_morador,id_bloco, valor) 
	SELECT mesano, id_contas, id_morador,id_bloco,ROUND((leitura_final-leitura_Inicial) * valor_m3,2) as total_leituras
	from leituras l
    join contas ct on
    ct.id_conta = l.id_contas and leituras = 1
	where mesano = v_mes_ano and id_bloco = v_bloco;
    
    -- Atualiza a tabela movimenta do bloco e MesAno para em movimento de A para M
    set v_mesano_ant = concat(right(cast(cast(date_add(concat(right(v_mes_ano,4),left(v_mes_ano,2),'01'), INTERVAL -1 MONTH) as date) as char(7)),2) ,
		 left(cast(cast(date_add(concat(right(v_mes_ano,4),left(v_mes_ano,2),'01'), INTERVAL -1 MONTH) as date) as char(7)),4));
         
    #select count(*) into v_qtMov from  movimento where id_bloco = v_bloco and mesano = v_mes_ano and situacao = 'A';
        
    #set v_qtMov=0;
     if exists(select 1 from  movimento where id_bloco = v_bloco and mesano = v_mes_ano and situacao = 'A') then
		update  movimento set situacao = 'F' where id_bloco = v_bloco and mesano = v_mesano_ant;
 		update movimento set situacao = 'M' where id_bloco = v_bloco and mesano = v_mes_ano;
        insert into movimento_msg (mesano, id_bloco,  total_moradores) values (v_mes_ano,v_bloco,v_t_morador);
	else
		update movimento set situacao = 'M' where id_bloco = v_bloco and mesano = v_mes_ano;
		update movimento_msg set total_moradores = v_t_morador where id_bloco = v_bloco and mesano = v_mes_ano;
    end if;
    
    #if exists(select 1 from  movimento_msg where id_bloco = v_bloco and mesano = v_mes_ano) then
	#	delete from movimento_msg where id_bloco = v_bloco and mesano = v_mes_ano;
    #end if;
    
    #insert into movimento_msg (mesano, id_bloco,  total_moradores) values (v_mes_ano,v_bloco,v_t_morador);
   
    delete from  calculos where  mesano = v_mes_ano and id_bloco = v_bloco and valor =0;
    
    select 'Processo executado com sucesso!!!!';
END