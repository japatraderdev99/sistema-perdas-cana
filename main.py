"""
SISTEMA DE MONITORAMENTO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR

Projeto Acadêmico - FIAP
Disciplina: Python
Objetivo: Aplicar conteúdos dos capítulos 3, 4, 5 e 6

Estruturas aplicadas:
- Capítulo 3: Subalgoritmos (funções e procedimentos com parâmetros)
- Capítulo 4: Estruturas de dados (listas, tuplas, dicionários)
- Capítulo 5: Manipulação de arquivos (JSON e TXT)
- Capítulo 6: Conexão com banco de dados Oracle

Autores: Gabriel Casarin & Claude AI
Data: 2025
"""

import json
import os
from datetime import datetime
from funcoes import *
from database import *

# ========================================
# MANIPULAÇÃO DE ARQUIVO JSON
# ========================================

def carregar_json():
    """
    Carrega dados do arquivo JSON

    Retorno:
        list: Lista de dicionários com colheitas

    Aplicação: Manipulação de arquivo JSON (Capítulo 5)
    Estrutura: LISTA de DICIONÁRIOS
    """
    try:
        with open('dados_colheitas.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            print(f"✅ {len(dados)} colheitas carregadas do JSON")
            return dados
    except FileNotFoundError:
        print("⚠️  Arquivo JSON não encontrado. Criando novo...")
        return []
    except json.JSONDecodeError:
        print("⚠️  Arquivo JSON corrompido. Iniciando lista vazia...")
        return []


def salvar_json(colheitas):
    """
    Salva dados no arquivo JSON

    Parâmetros:
        colheitas (list): Lista de dicionários com colheitas

    Retorno:
        None

    Aplicação: Manipulação de arquivo JSON (Capítulo 5)
    """
    try:
        with open('dados_colheitas.json', 'w', encoding='utf-8') as arquivo:
            json.dump(colheitas, arquivo, indent=4, ensure_ascii=False)
        print("✅ Dados salvos em JSON!")
    except Exception as e:
        print(f"❌ Erro ao salvar JSON: {e}")


# ========================================
# MANIPULAÇÃO DE ARQUIVO TEXTO
# ========================================

def gerar_relatorio_txt(colheitas):
    """
    Gera relatório detalhado em arquivo texto

    Parâmetros:
        colheitas (list): Lista de dicionários com colheitas

    Retorno:
        None

    Aplicação: Manipulação de arquivo TXT (Capítulo 5)
    """
    if not colheitas:
        print("⚠️  Nenhuma colheita para gerar relatório.")
        return

    try:
        with open('relatorio.txt', 'w', encoding='utf-8') as arquivo:
            # Cabeçalho
            arquivo.write("="*70 + "\n")
            arquivo.write("RELATÓRIO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR\n")
            arquivo.write("Sistema de Monitoramento - FIAP\n")
            arquivo.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            arquivo.write("="*70 + "\n\n")

            # Estatísticas gerais
            total_ton = sum(c['toneladas'] for c in colheitas)
            total_perda = sum(c['perda_toneladas'] for c in colheitas)
            total_prejuizo = sum(c['prejuizo_reais'] for c in colheitas)

            arquivo.write("RESUMO GERAL\n")
            arquivo.write("-"*70 + "\n")
            arquivo.write(f"Total de colheitas: {len(colheitas)}\n")
            arquivo.write(f"Total produzido: {total_ton:,.2f} toneladas\n")
            arquivo.write(f"Total perdido: {total_perda:,.2f} toneladas\n")
            arquivo.write(f"Prejuízo total: R$ {total_prejuizo:,.2f}\n")
            arquivo.write(f"Perda média: {(total_perda/total_ton*100):.2f}%\n")
            arquivo.write("="*70 + "\n\n")

            # Detalhamento de cada colheita
            arquivo.write("DETALHAMENTO DAS COLHEITAS\n")
            arquivo.write("="*70 + "\n\n")

            for i, col in enumerate(colheitas, 1):
                arquivo.write(f"COLHEITA #{i:03d}\n")
                arquivo.write("-"*70 + "\n")
                arquivo.write(f"Fazenda: {col['fazenda']}\n")
                arquivo.write(f"Data: {col['data']}\n")
                arquivo.write(f"Tipo de colheita: {col['tipo_colheita'].upper()}\n")
                arquivo.write(f"Toneladas colhidas: {col['toneladas']:,.2f} t\n")
                arquivo.write(f"Perda percentual: {col['perda_percentual']*100:.1f}%\n")
                arquivo.write(f"Perda em toneladas: {col['perda_toneladas']:,.2f} t\n")
                arquivo.write(f"Prejuízo estimado: R$ {col['prejuizo_reais']:,.2f}\n")
                arquivo.write("-"*70 + "\n\n")

            # Comparativo por tipo
            manuais = [c for c in colheitas if c['tipo_colheita'] == 'manual']
            mecanicas = [c for c in colheitas if c['tipo_colheita'] == 'mecanica']

            arquivo.write("COMPARATIVO: MANUAL vs MECÂNICA\n")
            arquivo.write("="*70 + "\n\n")

            if manuais:
                arquivo.write("COLHEITA MANUAL:\n")
                arquivo.write(f"  Quantidade: {len(manuais)} colheitas\n")
                arquivo.write(f"  Total produzido: {sum(c['toneladas'] for c in manuais):,.2f} t\n")
                arquivo.write(f"  Total perdido: {sum(c['perda_toneladas'] for c in manuais):,.2f} t\n")
                arquivo.write(f"  Prejuízo: R$ {sum(c['prejuizo_reais'] for c in manuais):,.2f}\n\n")

            if mecanicas:
                arquivo.write("COLHEITA MECÂNICA:\n")
                arquivo.write(f"  Quantidade: {len(mecanicas)} colheitas\n")
                arquivo.write(f"  Total produzido: {sum(c['toneladas'] for c in mecanicas):,.2f} t\n")
                arquivo.write(f"  Total perdido: {sum(c['perda_toneladas'] for c in mecanicas):,.2f} t\n")
                arquivo.write(f"  Prejuízo: R$ {sum(c['prejuizo_reais'] for c in mecanicas):,.2f}\n\n")

            # Rodapé
            arquivo.write("="*70 + "\n")
            arquivo.write("Fim do relatório\n")
            arquivo.write("Sistema desenvolvido para FIAP - 2025\n")

        print("✅ Relatório gerado: relatorio.txt")
        print(f"📄 Total de colheitas incluídas: {len(colheitas)}")

    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")


# ========================================
# FUNÇÃO DE CADASTRO (INTEGRANDO TUDO)
# ========================================

def cadastrar_colheita(colheitas, conn):
    """
    Cadastra nova colheita integrando JSON e Oracle

    Parâmetros:
        colheitas (list): Lista de dicionários (memória)
        conn: Conexão Oracle

    Retorno:
        None

    Aplicação: Integra TODOS os conteúdos (Cap 3, 4, 5, 6)
    """
    print("\n" + "="*60)
    print("🌾 CADASTRAR NOVA COLHEITA")
    print("="*60)

    # Coleta de dados com validação (Capítulo 3 - Funções)
    fazenda = input("Nome da fazenda: ").strip()
    while not fazenda:
        print("❌ Nome da fazenda não pode ser vazio!")
        fazenda = input("Nome da fazenda: ").strip()

    data = validar_data("Data da colheita (DD/MM/AAAA): ")
    tipo = validar_tipo_colheita("Tipo de colheita (manual/mecanica): ")
    toneladas = validar_numero_positivo("Toneladas colhidas: ")

    # Cálculos (Capítulo 3 - Funções com retorno de tupla)
    perda_percent = calcular_perda_percentual(tipo)
    perda_ton, prejuizo = calcular_prejuizo(toneladas, perda_percent)

    # Criando dicionário da colheita (Capítulo 4 - Dicionário)
    colheita = {
        'fazenda': fazenda,
        'data': data,
        'tipo_colheita': tipo,
        'toneladas': toneladas,
        'perda_percentual': perda_percent,
        'perda_toneladas': perda_ton,
        'prejuizo_reais': prejuizo
    }

    # Exibindo resumo
    print("\n" + "-"*60)
    print("📊 RESUMO DA COLHEITA:")
    print("-"*60)
    print(f"Fazenda: {fazenda}")
    print(f"Tipo: {tipo.upper()}")
    print(f"Toneladas: {toneladas:,.2f} t")
    print(f"Perda estimada: {perda_ton:,.2f} t ({perda_percent*100:.0f}%)")
    print(f"Prejuízo estimado: R$ {prejuizo:,.2f}")
    print("-"*60)

    confirmacao = input("\nConfirmar cadastro? (S/N): ").strip().upper()

    if confirmacao == 'S':
        # Salvando em lista (Capítulo 4 - Lista)
        colheitas.append(colheita)

        # Salvando em JSON (Capítulo 5 - Arquivo JSON)
        salvar_json(colheitas)

        # Salvando no Oracle (Capítulo 6 - Banco de dados)
        if conn:
            inserir_colheita(conn, colheita)

        print("\n✅ Colheita cadastrada com sucesso!")
    else:
        print("\n❌ Cadastro cancelado.")


# ========================================
# FUNÇÕES DE EXIBIÇÃO DO MENU
# ========================================

def listar_colheitas_json(colheitas):
    """
    Lista colheitas armazenadas em JSON
    """
    if not colheitas:
        print("\n⚠️  Nenhuma colheita cadastrada ainda.")
        return

    print("\n" + "="*60)
    print("📋 COLHEITAS CADASTRADAS (JSON)")
    print("="*60)

    for i, col in enumerate(colheitas, 1):
        print(f"\n{i}. {col['fazenda']} - {col['data']}")
        print(f"   Tipo: {col['tipo_colheita'].upper()}")
        print(f"   Toneladas: {col['toneladas']:,.2f} t")
        print(f"   Perda: {col['perda_toneladas']:,.2f} t ({col['perda_percentual']*100:.0f}%)")
        print(f"   Prejuízo: R$ {col['prejuizo_reais']:,.2f}")

    print("="*60)


def listar_colheitas_oracle_menu(conn):
    """
    Lista colheitas do Oracle de forma formatada
    """
    if not conn:
        print("❌ Não conectado ao Oracle!")
        return

    dados = listar_todas_colheitas(conn)

    if not dados:
        print("\n⚠️  Nenhuma colheita no Oracle ainda.")
        return

    print("\n" + "="*60)
    print("📊 COLHEITAS NO ORACLE DATABASE")
    print("="*60)

    for registro in dados:
        # Desempacotando tupla
        id_col, fazenda, data, tipo, ton, perda_perc, perda_ton, prejuizo = registro
        print(f"\nID: {id_col}")
        print(f"Fazenda: {fazenda}")
        print(f"Data: {data}")
        print(f"Tipo: {tipo.upper()}")
        print(f"Toneladas: {ton:,.2f} t")
        print(f"Perda: {perda_ton:,.2f} t ({perda_perc*100:.0f}%)")
        print(f"Prejuízo: R$ {prejuizo:,.2f}")
        print("-"*60)

    print(f"\n📊 Total de registros: {len(dados)}")
    print("="*60)


def exibir_estatisticas_oracle_menu(conn):
    """
    Exibe estatísticas do Oracle
    """
    if not conn:
        print("❌ Não conectado ao Oracle!")
        return

    stats = obter_estatisticas_oracle(conn)

    if not stats or stats['total_colheitas'] == 0:
        print("\n⚠️  Nenhum dado no Oracle ainda.")
        return

    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DO ORACLE DATABASE")
    print("="*60)
    print(f"Total de colheitas: {stats['total_colheitas']}")
    print(f"Total produzido: {stats['total_toneladas']:,.2f} toneladas")
    print(f"Total perdido: {stats['total_perda_toneladas']:,.2f} toneladas")
    print(f"Prejuízo total: R$ {stats['total_prejuizo']:,.2f}")
    print(f"Perda média: {stats['media_perda_percentual']*100:.1f}%")
    print("="*60)


def exibir_comparativo_oracle_menu(conn):
    """
    Exibe comparativo manual vs mecânica do Oracle
    """
    if not conn:
        print("❌ Não conectado ao Oracle!")
        return

    manual, mecanica = obter_comparativo_tipos_oracle(conn)

    print("\n" + "="*60)
    print("📊 COMPARATIVO: MANUAL vs MECÂNICA (ORACLE)")
    print("="*60)

    if manual['quantidade'] > 0:
        print("\n🌾 COLHEITA MANUAL:")
        print(f"  Quantidade: {manual['quantidade']} colheitas")
        print(f"  Total produzido: {manual['total_toneladas']:,.2f} t")
        print(f"  Total perdido: {manual['total_perda']:,.2f} t")
        print(f"  Prejuízo: R$ {manual['total_prejuizo']:,.2f}")

    if mecanica['quantidade'] > 0:
        print("\n🚜 COLHEITA MECÂNICA:")
        print(f"  Quantidade: {mecanica['quantidade']} colheitas")
        print(f"  Total produzido: {mecanica['total_toneladas']:,.2f} t")
        print(f"  Total perdido: {mecanica['total_perda']:,.2f} t")
        print(f"  Prejuízo: R$ {mecanica['total_prejuizo']:,.2f}")

    print("="*60)


# ========================================
# MENU PRINCIPAL
# ========================================

def menu_principal():
    """
    Menu principal do sistema com todas as funcionalidades

    Aplica: Todos os conteúdos dos capítulos 3, 4, 5 e 6
    """
    # Carrega dados do JSON (Capítulo 5)
    colheitas = carregar_json()

    # Conecta ao Oracle (Capítulo 6)
    print("\n🔌 Conectando ao Oracle Database...")
    conn = conectar_oracle()

    if conn:
        criar_tabela(conn)

    # Loop principal
    while True:
        print("\n" + "="*60)
        print("🌾 SISTEMA DE MONITORAMENTO - PERDAS NA COLHEITA")
        print("="*60)
        print("1 - Cadastrar colheita")
        print("2 - Listar colheitas (JSON)")
        print("3 - Exibir estatísticas (JSON)")
        print("4 - Exibir comparativo manual vs mecânica (JSON)")
        print("5 - Gerar relatório TXT")
        print("6 - Listar colheitas (Oracle)")
        print("7 - Estatísticas (Oracle)")
        print("8 - Comparativo (Oracle)")
        print("9 - Buscar colheita por fazenda")
        print("0 - Sair")
        print("="*60)

        opcao = input("Escolha uma opção: ").strip()

        # Match case (Python 3.10+)
        match opcao:
            case '1':
                cadastrar_colheita(colheitas, conn)

            case '2':
                listar_colheitas_json(colheitas)

            case '3':
                exibir_estatisticas(colheitas)

            case '4':
                exibir_comparativo_tipos(colheitas)

            case '5':
                gerar_relatorio_txt(colheitas)

            case '6':
                listar_colheitas_oracle_menu(conn)

            case '7':
                exibir_estatisticas_oracle_menu(conn)

            case '8':
                exibir_comparativo_oracle_menu(conn)

            case '9':
                nome = input("Nome da fazenda: ").strip()
                # Busca no JSON
                encontradas = buscar_colheitas_por_fazenda(colheitas, nome)
                if encontradas:
                    print(f"\n✅ {len(encontradas)} colheitas encontradas (JSON):")
                    for col in encontradas:
                        print(f"  • {col['fazenda']} - {col['data']} - {col['tipo_colheita']}")
                else:
                    print("⚠️  Nenhuma colheita encontrada no JSON.")

                # Busca no Oracle
                if conn:
                    encontradas_oracle = buscar_colheitas_por_fazenda(conn, nome)
                    if encontradas_oracle:
                        print(f"\n✅ {len(encontradas_oracle)} colheitas encontradas (Oracle):")
                        for reg in encontradas_oracle:
                            print(f"  • ID {reg[0]} - {reg[1]} - {reg[2]} - {reg[3]}")

            case '0':
                print("\n👋 Encerrando sistema...")
                if conn:
                    fechar_conexao(conn)
                print("✅ Sistema encerrado com sucesso!")
                break

            case _:
                print("❌ Opção inválida! Tente novamente.")


# ========================================
# EXECUÇÃO DO PROGRAMA
# ========================================

if __name__ == "__main__":
    print("="*60)
    print("🌾 SISTEMA DE MONITORAMENTO DE PERDAS")
    print("   Colheita de Cana-de-Açúcar")
    print("="*60)
    print("Projeto: FIAP - Disciplina Python")
    print("Autores: Gabriel Casarin & Claude AI")
    print("Ano: 2025")
    print("="*60)

    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Sistema interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        print("\n👋 Obrigado por usar o sistema!")
