"""
CADASTRO DE COLHEITAS DE EXEMPLO
Script para popular o banco com dados realistas
"""

from funcoes import *
from database import *
import json

print("="*60)
print("🌾 CADASTRO DE COLHEITAS DE EXEMPLO")
print("="*60)

# Conectar ao Oracle
conn = conectar_oracle()
if not conn:
    print("❌ Erro na conexão!")
    exit(1)

criar_tabela(conn)

# Lista para armazenar em JSON
colheitas = []

# ========================================
# EXEMPLO 1: Colheita Manual - São José
# ========================================
print("\n📝 Cadastrando Exemplo 1...")
colheita1 = {
    'fazenda': 'Fazenda São José',
    'data': '01/10/2025',
    'tipo_colheita': 'manual',
    'toneladas': 450.0,
    'perda_percentual': 0.05,
    'perda_toneladas': 22.5,
    'prejuizo_reais': 3375.0
}
colheitas.append(colheita1)
inserir_colheita(conn, colheita1)
print(f"✅ {colheita1['fazenda']} - {colheita1['toneladas']} ton (Manual)")

# ========================================
# EXEMPLO 2: Colheita Mecânica - Santa Clara
# ========================================
print("\n📝 Cadastrando Exemplo 2...")
colheita2 = {
    'fazenda': 'Fazenda Santa Clara',
    'data': '05/10/2025',
    'tipo_colheita': 'mecanica',
    'toneladas': 1200.0,
    'perda_percentual': 0.15,
    'perda_toneladas': 180.0,
    'prejuizo_reais': 27000.0
}
colheitas.append(colheita2)
inserir_colheita(conn, colheita2)
print(f"✅ {colheita2['fazenda']} - {colheita2['toneladas']} ton (Mecânica)")

# ========================================
# EXEMPLO 3: Colheita Mecânica - Boa Vista
# ========================================
print("\n📝 Cadastrando Exemplo 3...")
colheita3 = {
    'fazenda': 'Fazenda Boa Vista',
    'data': '10/10/2025',
    'tipo_colheita': 'mecanica',
    'toneladas': 980.0,
    'perda_percentual': 0.15,
    'perda_toneladas': 147.0,
    'prejuizo_reais': 22050.0
}
colheitas.append(colheita3)
inserir_colheita(conn, colheita3)
print(f"✅ {colheita3['fazenda']} - {colheita3['toneladas']} ton (Mecânica)")

# ========================================
# EXEMPLO 4: Colheita Manual - Esperança
# ========================================
print("\n📝 Cadastrando Exemplo 4...")
colheita4 = {
    'fazenda': 'Fazenda Esperança',
    'data': '12/10/2025',
    'tipo_colheita': 'manual',
    'toneladas': 520.0,
    'perda_percentual': 0.05,
    'perda_toneladas': 26.0,
    'prejuizo_reais': 3900.0
}
colheitas.append(colheita4)
inserir_colheita(conn, colheita4)
print(f"✅ {colheita4['fazenda']} - {colheita4['toneladas']} ton (Manual)")

# ========================================
# EXEMPLO 5: Colheita Mecânica - Progresso
# ========================================
print("\n📝 Cadastrando Exemplo 5...")
colheita5 = {
    'fazenda': 'Fazenda Progresso',
    'data': '14/10/2025',
    'tipo_colheita': 'mecanica',
    'toneladas': 1550.0,
    'perda_percentual': 0.15,
    'perda_toneladas': 232.5,
    'prejuizo_reais': 34875.0
}
colheitas.append(colheita5)
inserir_colheita(conn, colheita5)
print(f"✅ {colheita5['fazenda']} - {colheita5['toneladas']} ton (Mecânica)")

# Salvar em JSON
with open('dados_colheitas.json', 'w', encoding='utf-8') as arquivo:
    json.dump(colheitas, arquivo, indent=4, ensure_ascii=False)
print("\n✅ Dados salvos em JSON!")

# Exibir estatísticas
print("\n" + "="*60)
print("📊 ESTATÍSTICAS DOS EXEMPLOS CADASTRADOS")
print("="*60)

stats = obter_estatisticas_oracle(conn)
print(f"Total de colheitas: {stats['total_colheitas']}")
print(f"Total produzido: {stats['total_toneladas']:,.2f} toneladas")
print(f"Total perdido: {stats['total_perda_toneladas']:,.2f} toneladas")
print(f"Prejuízo total: R$ {stats['total_prejuizo']:,.2f}")
print(f"Perda média: {stats['media_perda_percentual']*100:.1f}%")

# Comparativo
manual, mecanica = obter_comparativo_tipos_oracle(conn)
print("\n" + "-"*60)
print("COMPARATIVO MANUAL vs MECÂNICA:")
print("-"*60)
print(f"\n🌾 MANUAL:")
print(f"  Colheitas: {manual['quantidade']}")
print(f"  Total: {manual['total_toneladas']:,.2f} ton")
print(f"  Perda: {manual['total_perda']:,.2f} ton")
print(f"  Prejuízo: R$ {manual['total_prejuizo']:,.2f}")

print(f"\n🚜 MECÂNICA:")
print(f"  Colheitas: {mecanica['quantidade']}")
print(f"  Total: {mecanica['total_toneladas']:,.2f} ton")
print(f"  Perda: {mecanica['total_perda']:,.2f} ton")
print(f"  Prejuízo: R$ {mecanica['total_prejuizo']:,.2f}")

# Análise de economia
if mecanica['quantidade'] > 0:
    total_mecanica = mecanica['total_toneladas']
    economia_potencial_ton = total_mecanica * 0.10  # 10% de diferença
    economia_potencial_reais = economia_potencial_ton * 150

    print("\n" + "-"*60)
    print("💡 ANÁLISE DE OPORTUNIDADE:")
    print("-"*60)
    print(f"Se as colheitas mecânicas fossem manuais:")
    print(f"  Economia: {economia_potencial_ton:,.2f} toneladas")
    print(f"  Economia: R$ {economia_potencial_reais:,.2f}")
    print(f"  Redução no prejuízo: {(economia_potencial_reais/mecanica['total_prejuizo']*100):.1f}%")

fechar_conexao(conn)

print("\n" + "="*60)
print("✅ EXEMPLOS CADASTRADOS COM SUCESSO!")
print("="*60)
print("\n📝 Próximo passo: Execute 'python main.py' para usar o sistema")
