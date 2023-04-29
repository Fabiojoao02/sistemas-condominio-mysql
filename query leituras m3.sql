select  c.id_condominio, c.nome nome_condominio, b.id_bloco, b.nome nome_bloco,
m.apto_sala, cad.nome morador, l.mesano, con.id_conta, con.nome conta,
l.dt_leitura, valor_m3, l.leitura_final, l.leitura_inicial,
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