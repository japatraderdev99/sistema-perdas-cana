"""
SISTEMA DE MONITORAMENTO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR
Arquivo: funcoes.py
Descrição: Subalgoritmos (funções e procedimentos) com passagem de parâmetros
"""

# ========================================
# FUNÇÕES DE VALIDAÇÃO DE DADOS
# ========================================

def validar_numero_positivo(mensagem):
    """
    Valida entrada de número positivo do usuário

    Parâmetros:
        mensagem (str): Mensagem a ser exibida ao usuário

    Retorno:
        float: Número validado e positivo

    Aplicação: Impede entrada de valores negativos ou tipos incorretos
    """
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("❌ Erro: Digite um valor positivo!")
                continue
            return valor
        except ValueError:
            print("❌ Erro: Digite apenas números!")


def validar_tipo_colheita(mensagem):
    """
    Valida tipo de colheita (manual ou mecânica)

    Parâmetros:
        mensagem (str): Mensagem a ser exibida ao usuário

    Retorno:
        str: 'manual' ou 'mecanica' (padronizado)

    Aplicação: Garante consistência nos dados de tipo de colheita
    """
    while True:
        tipo = input(mensagem).strip().lower()
        if tipo in ['manual', 'mecanica', 'mecânica']:
            return 'manual' if tipo == 'manual' else 'mecanica'
        print("❌ Erro: Digite 'manual' ou 'mecanica'!")


def validar_data(mensagem):
    """
    Valida formato de data DD/MM/AAAA

    Parâmetros:
        mensagem (str): Mensagem a ser exibida ao usuário

    Retorno:
        str: Data validada no formato DD/MM/AAAA

    Aplicação: Garante consistência no formato de datas
    """
    import re
    while True:
        data = input(mensagem).strip()
        # Valida formato DD/MM/AAAA
        if re.match(r'^\d{2}/\d{2}/\d{4}$', data):
            return data
        print("❌ Erro: Use o formato DD/MM/AAAA (ex: 15/10/2025)")


# ========================================
# FUNÇÕES DE CÁLCULO (COM RETORNO DE TUPLA)
# ========================================

def calcular_perda_percentual(tipo_colheita):
    """
    Retorna percentual de perda baseado no tipo de colheita

    Parâmetros:
        tipo_colheita (str): 'manual' ou 'mecanica'

    Retorno:
        float: Percentual de perda (0.05 para manual, 0.15 para mecânica)

    Base científica:
        - Manual: até 5% de perda (SOCICANA)
        - Mecânica: até 15% de perda (SOCICANA)

    Estrutura aplicada: DICIONÁRIO
    """
    perdas = {
        'manual': 0.05,     # 5% de perda
        'mecanica': 0.15    # 15% de perda
    }
    return perdas.get(tipo_colheita, 0.10)  # Default: 10%


def calcular_prejuizo(toneladas, perda_percent, preco_tonelada=150.0):
    """
    Calcula prejuízo em reais e toneladas perdidas

    Parâmetros:
        toneladas (float): Total de toneladas colhidas
        perda_percent (float): Percentual de perda (0.0 a 1.0)
        preco_tonelada (float): Preço por tonelada em reais (padrão: R$ 150)

    Retorno:
        tuple: (perda_toneladas, prejuizo_reais)

    Estrutura aplicada: TUPLA (retorno de múltiplos valores)
    """
    perda_ton = toneladas * perda_percent
    prejuizo = perda_ton * preco_tonelada
    return (perda_ton, prejuizo)  # Retorna TUPLA


def calcular_economia_potencial(colheitas):
    """
    Calcula quanto poderia ser economizado se todas fossem colheitas manuais

    Parâmetros:
        colheitas (list): Lista de dicionários com dados das colheitas

    Retorno:
        tuple: (economia_toneladas, economia_reais)

    Estrutura aplicada: LISTA e TUPLA
    """
    economia_ton = 0
    economia_reais = 0

    for colheita in colheitas:
        if colheita['tipo_colheita'] == 'mecanica':
            # Diferença entre perda mecânica (15%) e manual (5%)
            diferenca_perda = 0.15 - 0.05  # 10%
            economia_ton += colheita['toneladas'] * diferenca_perda
            economia_reais += economia_ton * 150.0

    return (economia_ton, economia_reais)


# ========================================
# PROCEDIMENTOS DE EXIBIÇÃO (SEM RETORNO)
# ========================================

def exibir_estatisticas(colheitas):
    """
    Exibe estatísticas gerais do sistema

    Parâmetros:
        colheitas (list): Lista de dicionários com dados das colheitas

    Retorno:
        None (procedimento)

    Estruturas aplicadas: LISTA, DICIONÁRIO
    """
    if not colheitas:
        print("\n⚠️  Nenhuma colheita cadastrada ainda.")
        return

    # Contadores e acumuladores
    total_ton = sum(c['toneladas'] for c in colheitas)
    total_perda_ton = sum(c['perda_toneladas'] for c in colheitas)
    total_prejuizo = sum(c['prejuizo_reais'] for c in colheitas)

    # Separação por tipo
    manuais = [c for c in colheitas if c['tipo_colheita'] == 'manual']
    mecanicas = [c for c in colheitas if c['tipo_colheita'] == 'mecanica']

    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS GERAIS DO SISTEMA")
    print("="*60)
    print(f"Total de colheitas cadastradas: {len(colheitas)}")
    print(f"  • Colheitas manuais: {len(manuais)}")
    print(f"  • Colheitas mecânicas: {len(mecanicas)}")
    print("-"*60)
    print(f"Total produzido: {total_ton:,.2f} toneladas")
    print(f"Total perdido: {total_perda_ton:,.2f} toneladas ({(total_perda_ton/total_ton*100):.1f}%)")
    print(f"Prejuízo total acumulado: R$ {total_prejuizo:,.2f}")
    print("="*60)

    # Cálculo de economia potencial
    if mecanicas:
        economia_ton, economia_reais = calcular_economia_potencial(colheitas)
        print(f"\n💡 ANÁLISE DE OPORTUNIDADE:")
        print(f"Se as colheitas mecânicas fossem manuais, você economizaria:")
        print(f"  • {economia_ton:,.2f} toneladas")
        print(f"  • R$ {economia_reais:,.2f}")
        print("="*60)


def exibir_colheita_detalhada(colheita, numero):
    """
    Exibe dados detalhados de uma colheita

    Parâmetros:
        colheita (dict): Dicionário com dados da colheita
        numero (int): Número da colheita na listagem

    Retorno:
        None (procedimento)

    Estrutura aplicada: DICIONÁRIO
    """
    print(f"\n{'='*60}")
    print(f"🌾 COLHEITA #{numero}")
    print(f"{'='*60}")
    print(f"Fazenda: {colheita['fazenda']}")
    print(f"Data: {colheita['data']}")
    print(f"Tipo de colheita: {colheita['tipo_colheita'].upper()}")
    print(f"Toneladas colhidas: {colheita['toneladas']:,.2f} t")
    print(f"Perda percentual: {colheita['perda_percentual']*100:.1f}%")
    print(f"Perda em toneladas: {colheita['perda_toneladas']:,.2f} t")
    print(f"Prejuízo estimado: R$ {colheita['prejuizo_reais']:,.2f}")
    print(f"{'='*60}")


def exibir_comparativo_tipos(colheitas):
    """
    Exibe comparativo entre colheitas manuais e mecânicas

    Parâmetros:
        colheitas (list): Lista de dicionários com dados das colheitas

    Retorno:
        None (procedimento)

    Estruturas aplicadas: LISTA, DICIONÁRIO, TUPLA
    """
    if not colheitas:
        print("\n⚠️  Nenhuma colheita cadastrada ainda.")
        return

    # Separação e cálculos por tipo
    manuais = [c for c in colheitas if c['tipo_colheita'] == 'manual']
    mecanicas = [c for c in colheitas if c['tipo_colheita'] == 'mecanica']

    print("\n" + "="*60)
    print("📊 COMPARATIVO: MANUAL vs MECÂNICA")
    print("="*60)

    if manuais:
        total_manual = sum(c['toneladas'] for c in manuais)
        perda_manual = sum(c['perda_toneladas'] for c in manuais)
        prejuizo_manual = sum(c['prejuizo_reais'] for c in manuais)

        print(f"\n🌾 COLHEITA MANUAL:")
        print(f"  Quantidade: {len(manuais)} colheitas")
        print(f"  Total produzido: {total_manual:,.2f} t")
        print(f"  Total perdido: {perda_manual:,.2f} t ({(perda_manual/total_manual*100):.1f}%)")
        print(f"  Prejuízo: R$ {prejuizo_manual:,.2f}")

    if mecanicas:
        total_mecanica = sum(c['toneladas'] for c in mecanicas)
        perda_mecanica = sum(c['perda_toneladas'] for c in mecanicas)
        prejuizo_mecanica = sum(c['prejuizo_reais'] for c in mecanicas)

        print(f"\n🚜 COLHEITA MECÂNICA:")
        print(f"  Quantidade: {len(mecanicas)} colheitas")
        print(f"  Total produzido: {total_mecanica:,.2f} t")
        print(f"  Total perdido: {perda_mecanica:,.2f} t ({(perda_mecanica/total_mecanica*100):.1f}%)")
        print(f"  Prejuízo: R$ {prejuizo_mecanica:,.2f}")

    print("="*60)


# ========================================
# FUNÇÃO DE FORMATAÇÃO
# ========================================

def formatar_moeda(valor):
    """
    Formata valor para padrão monetário brasileiro

    Parâmetros:
        valor (float): Valor em reais

    Retorno:
        str: Valor formatado (ex: "R$ 1.234,56")
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ========================================
# FUNÇÃO DE BUSCA
# ========================================

def buscar_colheitas_por_fazenda(colheitas, nome_fazenda):
    """
    Busca colheitas de uma fazenda específica

    Parâmetros:
        colheitas (list): Lista de dicionários com dados das colheitas
        nome_fazenda (str): Nome da fazenda a buscar

    Retorno:
        list: Lista com colheitas da fazenda encontrada

    Estruturas aplicadas: LISTA, DICIONÁRIO
    """
    resultado = [c for c in colheitas if nome_fazenda.lower() in c['fazenda'].lower()]
    return resultado
