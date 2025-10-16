"""
SISTEMA DE MONITORAMENTO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR
Arquivo: database.py
Descrição: Conexão e operações com Oracle Database
"""

import oracledb

# ========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ========================================

def conectar_oracle():
    """
    Estabelece conexão com Oracle Database

    Retorno:
        connection: Objeto de conexão ou None em caso de erro

    Aplicação: Conexão com banco de dados Oracle (Capítulo 6)
    """
    try:
        conn = oracledb.connect(
            user='rm568506',
            password='190294',
            dsn='oracle.fiap.com.br:1521/ORCL'
        )
        print("✅ Conectado ao Oracle Database!")
        return conn
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"❌ Erro na conexão com Oracle:")
        print(f"   Código: {error.code}")
        print(f"   Mensagem: {error.message}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado na conexão: {e}")
        return None


# ========================================
# OPERAÇÕES DDL (DATA DEFINITION LANGUAGE)
# ========================================

def criar_tabela(conn):
    """
    Cria tabela de colheitas se não existir

    Parâmetros:
        conn: Objeto de conexão Oracle

    Retorno:
        bool: True se criou/existe, False em caso de erro

    Estrutura da tabela:
        - id: Chave primária (auto incremento)
        - fazenda: Nome da fazenda
        - data_colheita: Data da colheita
        - tipo_colheita: 'manual' ou 'mecanica'
        - toneladas: Toneladas colhidas
        - perda_percentual: Percentual de perda
        - perda_toneladas: Toneladas perdidas
        - prejuizo_reais: Prejuízo em reais
    """
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        # Tenta criar a tabela
        cursor.execute("""
            CREATE TABLE colheitas_cana (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                fazenda VARCHAR2(100) NOT NULL,
                data_colheita DATE NOT NULL,
                tipo_colheita VARCHAR2(20) NOT NULL,
                toneladas NUMBER(10,2) NOT NULL,
                perda_percentual NUMBER(5,2) NOT NULL,
                perda_toneladas NUMBER(10,2) NOT NULL,
                prejuizo_reais NUMBER(12,2) NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ Tabela 'colheitas_cana' criada com sucesso!")
        return True
    except oracledb.DatabaseError as e:
        error, = e.args
        # ORA-00955: name is already used by an existing object
        if error.code == 955:
            print("⚠️  Tabela 'colheitas_cana' já existe. Prosseguindo...")
            return True
        else:
            print(f"❌ Erro ao criar tabela: {error.message}")
            return False
    finally:
        cursor.close()


def dropar_tabela(conn):
    """
    Remove a tabela de colheitas (USE COM CUIDADO!)

    Parâmetros:
        conn: Objeto de conexão Oracle

    Retorno:
        bool: True se removeu, False em caso de erro
    """
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE colheitas_cana")
        conn.commit()
        print("✅ Tabela removida com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao dropar tabela: {e}")
        return False
    finally:
        cursor.close()


# ========================================
# OPERAÇÕES DML (DATA MANIPULATION LANGUAGE)
# ========================================

def inserir_colheita(conn, colheita):
    """
    Insere uma colheita no banco de dados

    Parâmetros:
        conn: Objeto de conexão Oracle
        colheita (dict): Dicionário com dados da colheita

    Retorno:
        bool: True se inseriu, False em caso de erro

    Estrutura aplicada: DICIONÁRIO
    """
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO colheitas_cana
            (fazenda, data_colheita, tipo_colheita, toneladas,
             perda_percentual, perda_toneladas, prejuizo_reais)
            VALUES (:fazenda, TO_DATE(:data, 'DD/MM/YYYY'), :tipo,
                    :toneladas, :perda_perc, :perda_ton, :prejuizo)
        """, {
            'fazenda': colheita['fazenda'],
            'data': colheita['data'],
            'tipo': colheita['tipo_colheita'],
            'toneladas': colheita['toneladas'],
            'perda_perc': colheita['perda_percentual'],
            'perda_ton': colheita['perda_toneladas'],
            'prejuizo': colheita['prejuizo_reais']
        })
        conn.commit()
        print("✅ Colheita salva no Oracle Database!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inserir colheita: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()


def atualizar_colheita(conn, id_colheita, campo, novo_valor):
    """
    Atualiza um campo específico de uma colheita

    Parâmetros:
        conn: Objeto de conexão Oracle
        id_colheita (int): ID da colheita a atualizar
        campo (str): Nome do campo a atualizar
        novo_valor: Novo valor do campo

    Retorno:
        bool: True se atualizou, False em caso de erro
    """
    if not conn:
        return False

    campos_validos = ['fazenda', 'tipo_colheita', 'toneladas']
    if campo not in campos_validos:
        print(f"❌ Campo inválido! Use: {', '.join(campos_validos)}")
        return False

    cursor = conn.cursor()
    try:
        sql = f"UPDATE colheitas_cana SET {campo} = :valor WHERE id = :id"
        cursor.execute(sql, {'valor': novo_valor, 'id': id_colheita})
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Colheita #{id_colheita} atualizada!")
            return True
        else:
            print(f"⚠️  Colheita #{id_colheita} não encontrada.")
            return False
    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()


def deletar_colheita(conn, id_colheita):
    """
    Remove uma colheita do banco de dados

    Parâmetros:
        conn: Objeto de conexão Oracle
        id_colheita (int): ID da colheita a remover

    Retorno:
        bool: True se removeu, False em caso de erro
    """
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM colheitas_cana WHERE id = :id", {'id': id_colheita})
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Colheita #{id_colheita} removida!")
            return True
        else:
            print(f"⚠️  Colheita #{id_colheita} não encontrada.")
            return False
    except Exception as e:
        print(f"❌ Erro ao deletar: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()


# ========================================
# OPERAÇÕES DE CONSULTA (SELECT)
# ========================================

def listar_todas_colheitas(conn):
    """
    Lista todas as colheitas cadastradas no Oracle

    Parâmetros:
        conn: Objeto de conexão Oracle

    Retorno:
        list: Lista de tuplas com dados das colheitas

    Estrutura aplicada: LISTA de TUPLAS
    """
    if not conn:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, fazenda, TO_CHAR(data_colheita, 'DD/MM/YYYY'),
                   tipo_colheita, toneladas, perda_percentual,
                   perda_toneladas, prejuizo_reais
            FROM colheitas_cana
            ORDER BY id DESC
        """)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Erro ao listar colheitas: {e}")
        return []
    finally:
        cursor.close()


def buscar_colheita_por_id(conn, id_colheita):
    """
    Busca uma colheita específica por ID

    Parâmetros:
        conn: Objeto de conexão Oracle
        id_colheita (int): ID da colheita

    Retorno:
        tuple: Dados da colheita ou None

    Estrutura aplicada: TUPLA
    """
    if not conn:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, fazenda, TO_CHAR(data_colheita, 'DD/MM/YYYY'),
                   tipo_colheita, toneladas, perda_percentual,
                   perda_toneladas, prejuizo_reais
            FROM colheitas_cana
            WHERE id = :id
        """, {'id': id_colheita})
        resultado = cursor.fetchone()
        return resultado
    except Exception as e:
        print(f"❌ Erro ao buscar colheita: {e}")
        return None
    finally:
        cursor.close()


def buscar_colheitas_por_tipo(conn, tipo):
    """
    Busca colheitas por tipo (manual ou mecânica)

    Parâmetros:
        conn: Objeto de conexão Oracle
        tipo (str): 'manual' ou 'mecanica'

    Retorno:
        list: Lista de tuplas com colheitas do tipo especificado

    Estrutura aplicada: LISTA de TUPLAS
    """
    if not conn:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, fazenda, TO_CHAR(data_colheita, 'DD/MM/YYYY'),
                   tipo_colheita, toneladas, perda_percentual,
                   perda_toneladas, prejuizo_reais
            FROM colheitas_cana
            WHERE tipo_colheita = :tipo
            ORDER BY id DESC
        """, {'tipo': tipo})
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Erro ao buscar colheitas por tipo: {e}")
        return []
    finally:
        cursor.close()


def buscar_colheitas_por_fazenda(conn, nome_fazenda):
    """
    Busca colheitas de uma fazenda específica

    Parâmetros:
        conn: Objeto de conexão Oracle
        nome_fazenda (str): Nome da fazenda (busca parcial)

    Retorno:
        list: Lista de tuplas com colheitas da fazenda

    Estrutura aplicada: LISTA de TUPLAS
    """
    if not conn:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, fazenda, TO_CHAR(data_colheita, 'DD/MM/YYYY'),
                   tipo_colheita, toneladas, perda_percentual,
                   perda_toneladas, prejuizo_reais
            FROM colheitas_cana
            WHERE UPPER(fazenda) LIKE UPPER(:nome)
            ORDER BY id DESC
        """, {'nome': f'%{nome_fazenda}%'})
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Erro ao buscar colheitas por fazenda: {e}")
        return []
    finally:
        cursor.close()


# ========================================
# ESTATÍSTICAS E ANÁLISES
# ========================================

def obter_estatisticas_oracle(conn):
    """
    Obtém estatísticas gerais do banco de dados

    Parâmetros:
        conn: Objeto de conexão Oracle

    Retorno:
        dict: Dicionário com estatísticas

    Estrutura aplicada: DICIONÁRIO
    """
    if not conn:
        return {}

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                COUNT(*) as total_colheitas,
                SUM(toneladas) as total_toneladas,
                SUM(perda_toneladas) as total_perda_toneladas,
                SUM(prejuizo_reais) as total_prejuizo,
                AVG(perda_percentual) as media_perda_percentual
            FROM colheitas_cana
        """)
        resultado = cursor.fetchone()

        estatisticas = {
            'total_colheitas': resultado[0] or 0,
            'total_toneladas': resultado[1] or 0,
            'total_perda_toneladas': resultado[2] or 0,
            'total_prejuizo': resultado[3] or 0,
            'media_perda_percentual': resultado[4] or 0
        }
        return estatisticas
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
        return {}
    finally:
        cursor.close()


def obter_comparativo_tipos_oracle(conn):
    """
    Obtém comparativo entre colheitas manuais e mecânicas

    Parâmetros:
        conn: Objeto de conexão Oracle

    Retorno:
        tuple: (dados_manual, dados_mecanica) - cada um é um dicionário

    Estrutura aplicada: TUPLA de DICIONÁRIOS
    """
    if not conn:
        return ({}, {})

    cursor = conn.cursor()
    try:
        # Dados colheita manual
        cursor.execute("""
            SELECT
                COUNT(*) as quantidade,
                SUM(toneladas) as total_toneladas,
                SUM(perda_toneladas) as total_perda,
                SUM(prejuizo_reais) as total_prejuizo
            FROM colheitas_cana
            WHERE tipo_colheita = 'manual'
        """)
        resultado_manual = cursor.fetchone()

        manual = {
            'quantidade': resultado_manual[0] or 0,
            'total_toneladas': resultado_manual[1] or 0,
            'total_perda': resultado_manual[2] or 0,
            'total_prejuizo': resultado_manual[3] or 0
        }

        # Dados colheita mecânica
        cursor.execute("""
            SELECT
                COUNT(*) as quantidade,
                SUM(toneladas) as total_toneladas,
                SUM(perda_toneladas) as total_perda,
                SUM(prejuizo_reais) as total_prejuizo
            FROM colheitas_cana
            WHERE tipo_colheita = 'mecanica'
        """)
        resultado_mecanica = cursor.fetchone()

        mecanica = {
            'quantidade': resultado_mecanica[0] or 0,
            'total_toneladas': resultado_mecanica[1] or 0,
            'total_perda': resultado_mecanica[2] or 0,
            'total_prejuizo': resultado_mecanica[3] or 0
        }

        return (manual, mecanica)  # Retorna TUPLA de DICIONÁRIOS
    except Exception as e:
        print(f"❌ Erro ao obter comparativo: {e}")
        return ({}, {})
    finally:
        cursor.close()


# ========================================
# FUNÇÃO DE FECHAMENTO
# ========================================

def fechar_conexao(conn):
    """
    Fecha a conexão com o banco de dados

    Parâmetros:
        conn: Objeto de conexão Oracle

    Retorno:
        None
    """
    if conn:
        try:
            conn.close()
            print("✅ Conexão com Oracle encerrada.")
        except Exception as e:
            print(f"❌ Erro ao fechar conexão: {e}")
