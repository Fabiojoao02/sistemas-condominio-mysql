CREATE DEFINER=`root`@`localhost` PROCEDURE `prc_calcula_movimento`(IN v_mes_ano varchar(6))
BEGIN
	DECLARE done INT default FALSE;
	DECLARE v_qt, v_t_morador,v_id_morador, v_qt_moradores integer;
	DECLARE v_fundo_reserva, v_taxa_condominio, v_fracao_ideal float;
    
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
		where m.situacao = 'A';    
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
		where m.situacao = 'A'    
	);
	set v_qt = 0;
	set v_t_morador = 0;
	select count(*), SUM(qt_moradores) into v_qt, v_t_morador from tmp_calculo;
    -- ===================
    -- Limpa os calculos existentes no mes e ano corrente
	delete from calculos  where  mesano = v_mes_ano;
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
			insert into calculos (mesano,id_contas, id_morador, valor) 
			SELECT mesano, id_contas , v_id_morador, ROUND(format((valor/10)*1, 2),2)
			FROM movimento where id_contas in(9) ;            
        end if;    
		-- ===================
		-- lança conta v_taxa_condominio-10
        if v_taxa_condominio > 0 then
			insert into calculos (mesano,id_contas, id_morador, valor) 
			SELECT mesano, id_contas , v_id_morador, ROUND(format((valor/10)*1, 2),2)
			FROM movimento where id_contas in(10) ;            
        end if;    
		-- ===================
		-- lança demais contas
		insert into calculos (mesano,id_contas, id_morador, valor) 
		SELECT mesano, id_contas, v_id_morador,
		CASE WHEN id_tipo_calculo = 1 then ROUND((valor/v_qt)* v_fracao_ideal,2) 
			WHEN id_tipo_calculo = 2 then ROUND(((valor/v_t_morador) * v_qt_moradores)* v_fracao_ideal,2)    
			ELSE  ROUND(format(valor, 2),2)  END   
		FROM movimento 
		where id_contas not in(9,10) and mesano = v_mes_ano;
	END LOOP read_loop;
	CLOSE cur_cal ;
    -- ===================
	-- lançamento de gas
	insert into calculos (mesano,id_contas, id_morador, valor) 
	SELECT mesano, id_contas, id_morador,ROUND((leitura_final-leitura_Inicial) * vl_gas_m3,2) as total_gas 
	from leituras 
	where mesano = v_mes_ano ;
    
    select 'Processo executado com sucesso!!!!';
END