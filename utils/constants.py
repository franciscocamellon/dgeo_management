# {'Não iniciada':1,
#  'Em execução':2,
#  'Pausada':3,
#  'Finalizada':4,
#  'Não finalizada':5}

MANAGEMENT_DATABASE_NAME = 'sap2'
STAFF_PROFILE = {'Aquisitor': [], 'Revisor': [], 'Validador': [], 'Editor': [], 'Preparador': [],
                 'Revisor_Aquisitor': [], 'Revisor_PICE': []}
STAFF_PROFILE_MAPPING = ['Aquisitor', 'Revisor', 'Validador', 'Editor', 'Preparador']
YEARS = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov',
         12: 'Dez'}

ACTIVITIES = {'nao_iniciada': ['Não iniciada', 'bg-success-lighten text-success'],
              'em_execucao': ['Em execução', 'bg-success-lighten text-success'],
              'finalizada': ['Finalizada', 'bg-info-lighten text-info'],
              'pausada': ['Pausada', 'bg-warning-lighten text-warning'],
              'nao_finalizada': ['Não finalizada', 'bg-danger-lighten text-danger']}

DGEO_DATABASE_URL = 'postgresql://postgres:r4d10gr4f14@10.1.10.213:5432/'
# DGEO_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/'

STAFF_SQL = """SELECT usuario.id AS user_id, tipo_posto_grad.nome_abrev AS posto_grad, usuario.nome_guerra, usuario.nome, 
                    perfil_producao.nome AS perfil, tipo_turno.nome as turno, usuario.administrador, usuario.ativo
               FROM dgeo.usuario
               INNER JOIN dominio.tipo_posto_grad
                    ON usuario.tipo_posto_grad_id = tipo_posto_grad.code
               INNER JOIN dominio.tipo_turno
                    ON usuario.tipo_turno_id = tipo_turno.code
               INNER JOIN (
                        SELECT perfil_producao_operador.usuario_id, perfil_producao.nome  FROM macrocontrole.perfil_producao_operador
                        INNER JOIN macrocontrole.perfil_producao ON perfil_producao_operador.perfil_producao_id = perfil_producao.id
                        ORDER BY perfil_producao_operador.usuario_id ASC) AS perfil_producao
                    ON usuario.id = perfil_producao.usuario_id"""

STAFF_SQL_BY_PROFILE = """
    SELECT usuario.id AS user_id, tipo_posto_grad.nome_abrev AS posto_grad, usuario.nome_guerra, usuario.nome, 
        perfil_producao.nome AS perfil, tipo_turno.nome as turno, usuario.administrador, usuario.ativo
    FROM dgeo.usuario
    INNER JOIN dominio.tipo_posto_grad
        ON usuario.tipo_posto_grad_id = tipo_posto_grad.code
    INNER JOIN dominio.tipo_turno
        ON usuario.tipo_turno_id = tipo_turno.code
    INNER JOIN (
            SELECT perfil_producao_operador.usuario_id, perfil_producao.nome  FROM macrocontrole.perfil_producao_operador
            INNER JOIN macrocontrole.perfil_producao ON perfil_producao_operador.perfil_producao_id = perfil_producao.id
            ORDER BY perfil_producao_operador.usuario_id ASC) AS perfil_producao
        ON usuario.id = perfil_producao.usuario_id
    WHERE perfil_producao.nome = '{}'"""

SQL_TO_STAFF_PROFILE = """
SELECT tipo_posto_grad.nome_abrev AS posto_grad, usuario.nome_guerra, perfil_producao.nome AS perfil
FROM dgeo.usuario
INNER JOIN dominio.tipo_posto_grad
    ON usuario.tipo_posto_grad_id = tipo_posto_grad.code
INNER JOIN (
        SELECT perfil_producao_operador.usuario_id, perfil_producao.nome  
        FROM macrocontrole.perfil_producao_operador
        INNER JOIN macrocontrole.perfil_producao 
            ON perfil_producao_operador.perfil_producao_id = perfil_producao.id) AS perfil_producao
    ON usuario.id = perfil_producao.usuario_id
WHERE usuario_id = {};"""

ACTIVITY_BY_USER_SQL = """
    SELECT atividade.id, atividade.etapa_id, usuario.nome_guerra, tipo_situacao.nome as situacao, atividade.data_inicio,
        atividade.data_fim, atividade.observacao 
    FROM macrocontrole.atividade 
    INNER JOIN dgeo.usuario 
        ON usuario.id = usuario_id 
    INNER JOIN dominio.tipo_situacao 
        ON tipo_situacao.code = tipo_situacao_id 
    WHERE tipo_situacao.code = 4"""

SELECT_COUNT_ACTIVITY_BY_USER = """
    SELECT COUNT(*) FROM (
        SELECT atividade.id, atividade.etapa_id, usuario.nome_guerra, tipo_situacao.nome as situacao, 
            atividade.data_inicio, atividade.data_fim, atividade.observacao 
        FROM macrocontrole.atividade 
        INNER JOIN dgeo.usuario 
            ON usuario.id = usuario_id 
        INNER JOIN dominio.tipo_situacao 
            ON tipo_situacao.code = tipo_situacao_id 
        WHERE atividade.usuario_id = {} AND tipo_situacao.code = {}) AS foo """

CURRENT_MONTHLY_ACTIVITY_BY_USER = """
SELECT
    COUNT(CASE WHEN situacao = 'Em execução' THEN 1 END) AS em_execucao,
    COUNT(CASE WHEN situacao = 'Finalizada' THEN 1 END) AS finalizada,
    COUNT(CASE WHEN situacao = 'Pausada' THEN 1 END) AS pausada,
    COUNT(CASE WHEN situacao = 'Não finalizada' THEN 1 END) AS nao_finalizada
FROM (
    SELECT
        atividade.id,
        atividade.etapa_id,
        usuario.nome_guerra,
        tipo_situacao.nome AS situacao,
        atividade.data_inicio AS data_inicio_subquery,
        atividade.data_fim,
        atividade.observacao
    FROM
        macrocontrole.atividade
    INNER JOIN
        dgeo.usuario ON usuario.id = usuario_id
    INNER JOIN
        dominio.tipo_situacao ON tipo_situacao.code = tipo_situacao_id
    WHERE
        atividade.usuario_id = {}
) AS initial_results
WHERE EXTRACT(MONTH FROM initial_results.data_inicio_subquery) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM initial_results.data_inicio_subquery) = EXTRACT(YEAR FROM CURRENT_DATE)"""

MONTHLY_ACTIVITY_BY_USER = """
SELECT
    COUNT(CASE WHEN situacao = 'Em execução' THEN 1 END) AS em_execucao,
    COUNT(CASE WHEN situacao = 'Finalizada' THEN 1 END) AS finalizada,
    COUNT(CASE WHEN situacao = 'Pausada' THEN 1 END) AS pausada,
    COUNT(CASE WHEN situacao = 'Não finalizada' THEN 1 END) AS nao_finalizada
FROM (
    SELECT
        atividade.id,
        atividade.etapa_id,
        usuario.nome_guerra,
        tipo_situacao.nome AS situacao,
        atividade.data_inicio AS data_inicio_subquery,
        atividade.data_fim,
        atividade.observacao
    FROM
        macrocontrole.atividade
    INNER JOIN
        dgeo.usuario ON usuario.id = usuario_id
    INNER JOIN
        dominio.tipo_situacao ON tipo_situacao.code = tipo_situacao_id
    WHERE
        atividade.usuario_id = {}
) AS initial_results
WHERE EXTRACT(MONTH FROM initial_results.data_inicio_subquery) = {}
    AND EXTRACT(YEAR FROM initial_results.data_inicio_subquery) = EXTRACT(YEAR FROM CURRENT_DATE);
"""

SQL_TO_CHART_DATA = """
SELECT
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 1 THEN 1 END) AS janeiro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 2 THEN 1 END) AS fevereiro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 3 THEN 1 END) AS março,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 4 THEN 1 END) AS abril,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 5 THEN 1 END) AS maio,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 6 THEN 1 END) AS junho,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 7 THEN 1 END) AS julho,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 8 THEN 1 END) AS agosto,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 9 THEN 1 END) AS setembro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 10 THEN 1 END) AS outubro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 11 THEN 1 END) AS novembro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_inicio_subquery) = 12 THEN 1 END) AS dezembro
FROM (
    SELECT
        atividade.id,
        atividade.etapa_id,
        usuario.nome_guerra,
        tipo_situacao.nome AS situacao,
        atividade.data_inicio AS data_inicio_subquery,
        atividade.data_fim,
        atividade.observacao
    FROM
        macrocontrole.atividade
    INNER JOIN
        dgeo.usuario ON usuario.id = usuario_id
    INNER JOIN
        dominio.tipo_situacao ON tipo_situacao.code = tipo_situacao_id
    WHERE
        atividade.usuario_id = {}
        AND tipo_situacao.code = {}
) AS initial_results
WHERE EXTRACT(YEAR FROM initial_results.data_inicio_subquery) = EXTRACT(YEAR FROM CURRENT_DATE);"""

SQL_TO_WEEKLY_CHART_DATA = """
SELECT
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 1 THEN 1 END) AS segunda,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 2 THEN 1 END) AS terça,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 3 THEN 1 END) AS quarta,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 4 THEN 1 END) AS quinta,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 5 THEN 1 END) AS sexta
FROM (
    SELECT
        atividade.data_fim AS data_fim_subquery
    FROM
        macrocontrole.atividade
    INNER JOIN
        dgeo.usuario ON usuario.id = usuario_id
    INNER JOIN
        dominio.tipo_situacao ON tipo_situacao.code = tipo_situacao_id
    WHERE
        atividade.usuario_id = {}
        AND tipo_situacao.code = {}
) AS initial_results
WHERE data_fim_subquery >= DATE_TRUNC('week', CURRENT_DATE)
  AND data_fim_subquery < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week';
"""

SQL_TO_CHART_AVERAGE_DATA = """
SELECT
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 1 THEN 1 END) AS janeiro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 2 THEN 1 END) AS fevereiro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 3 THEN 1 END) AS março,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 4 THEN 1 END) AS abril,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 5 THEN 1 END) AS maio,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 6 THEN 1 END) AS junho,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 7 THEN 1 END) AS julho,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 8 THEN 1 END) AS agosto,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 9 THEN 1 END) AS setembro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 10 THEN 1 END) AS outubro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 11 THEN 1 END) AS novembro,
    COUNT(CASE WHEN EXTRACT(MONTH FROM data_fim_subquery) = 12 THEN 1 END) AS dezembro
FROM (
    SELECT
        atividade.data_fim AS data_fim_subquery
    FROM
        macrocontrole.atividade
    INNER JOIN
        dominio.tipo_situacao ON tipo_situacao.code = tipo_situacao_id
    WHERE tipo_situacao.code = {}
) AS initial_results
WHERE EXTRACT(YEAR FROM initial_results.data_fim_subquery) = EXTRACT(YEAR FROM CURRENT_DATE);"""

WEEKLY_CHART_AVERAGE_DATA = """
SELECT
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 1 THEN 1 END) AS segunda,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 2 THEN 1 END) AS terça,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 3 THEN 1 END) AS quarta,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 4 THEN 1 END) AS quinta,
    COUNT(CASE WHEN EXTRACT(DOW FROM data_fim_subquery) = 5 THEN 1 END) AS sexta
FROM (
    SELECT
        atividade.data_fim AS data_fim_subquery
    FROM
        macrocontrole.atividade
    INNER JOIN
        dominio.tipo_situacao ON tipo_situacao.code = tipo_situacao_id
    WHERE tipo_situacao.code = {}
) AS initial_results
WHERE data_fim_subquery >= DATE_TRUNC('week', CURRENT_DATE)
  AND data_fim_subquery < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week';
"""

SQL_COUNT_TO_FINISHED_ACTIVITIES = """
SELECT COUNT(atividade.id)
FROM macrocontrole.atividade
WHERE data_fim >= DATE_TRUNC('year', CURRENT_DATE)
  AND data_fim <= CURRENT_DATE
  AND tipo_situacao_id = 4;
"""

SQL_TO_DONUT_CHART_DATA = """
SELECT
    COUNT(CASE WHEN situacao = 1 THEN 1 END) AS nao_iniciada,
    COUNT(CASE WHEN situacao = 2 THEN 1 END) AS em_execucao,
    COUNT(CASE WHEN situacao = 3 THEN 1 END) AS pausada,
    COUNT(CASE WHEN situacao = 4 THEN 1 END) AS finalizada
FROM (
    SELECT atividade.tipo_situacao_id AS situacao, projeto.nome, projeto.id AS projeto_id
    FROM macrocontrole.atividade
    INNER JOIN macrocontrole.unidade_trabalho 
        ON unidade_trabalho.id = unidade_trabalho_id
    INNER JOIN macrocontrole.lote 
        ON lote.id = lote_id
    INNER JOIN  macrocontrole.projeto 
        ON projeto.id = projeto_id
) AS donut_chart_data
WHERE donut_chart_data.projeto_id = {};"""


SQL_TO_WEEKLY_TASKS = """
SELECT atividade.id, tipo_etapa.nome AS etapa,tipo_fase.nome AS fase,subfase.nome AS subfase,
    atividade.unidade_trabalho_id,tipo_situacao.nome AS situacao, tipo_posto_grad.nome_abrev, usuario.nome_guerra, 
    atividade.data_inicio, atividade.data_fim
FROM macrocontrole.atividade
INNER JOIN macrocontrole.etapa
    ON etapa.id = etapa_id
INNER JOIN dominio.tipo_etapa
    ON tipo_etapa.code = etapa.id
INNER JOIN macrocontrole.subfase
    ON subfase.id = subfase_id
INNER JOIN macrocontrole.fase
    ON fase.id = fase_id
INNER JOIN dominio.tipo_fase
    ON tipo_fase.code = tipo_fase_id
INNER JOIN dominio.tipo_situacao
    ON tipo_situacao.code = tipo_situacao_id
INNER JOIN dgeo.usuario
    ON usuario.id = usuario_id
INNER JOIN dominio.tipo_posto_grad
    ON tipo_posto_grad.code = tipo_posto_grad_id
WHERE data_fim >= DATE_TRUNC('week', CURRENT_DATE)
    AND data_fim < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'
    AND usuario.id = {};
"""

SQL_TO_COUNT_ACTIVITY_TYPE = """
SELECT
    COUNT(activities_type.id) AS total,
    COUNT(CASE WHEN fase = 'Extração' THEN 1 END) AS extracao,
    COUNT(CASE WHEN fase = 'Validação' THEN 1 END) AS validacao,
    COUNT(CASE WHEN fase = 'Edição' THEN 1 END) AS edicao,
    COUNT(CASE WHEN fase = 'Disseminação' THEN 1 END) AS disseminacao
FROM (
    SELECT
        atividade.id, 
        tipo_fase.nome as fase 
    FROM 
        macrocontrole.atividade
    INNER JOIN 
        macrocontrole.etapa ON etapa.id = etapa_id
    INNER JOIN 
        dominio.tipo_etapa ON tipo_etapa.code = tipo_etapa_id
    INNER JOIN 
        dominio.tipo_situacao ON tipo_situacao.code = tipo_situacao_id
    INNER JOIN 
        macrocontrole.subfase ON subfase.id = subfase_id
    INNER JOIN 
        macrocontrole.fase ON fase.id = fase_id
    INNER JOIN 
        dominio.tipo_fase ON tipo_fase.code = tipo_fase_id
    ORDER BY etapa ASC
) AS activities_type
"""