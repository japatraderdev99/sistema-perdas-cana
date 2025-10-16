# FIAP - Faculdade de Informática e Administração Paulista

![FIAP Logo](https://www.fiap.com.br/wp-content/themes/fiap2016/images/sharing/fiap.png)

# Sistema de Monitoramento de Perdas na Colheita de Cana-de-Açúcar

**Grupo:** Agro Tech Solutions

## 👨‍🎓 Integrantes

- [Guilherme Yamada Dantas](https://www.linkedin.com/in/guilherme-yamada-dantas) - RM568506

## 👩‍🏫 Professores

### Tutor(a)
- [Nome do Tutor](https://www.linkedin.com/)

### Coordenador(a)
- [Nome do Coordenador](https://www.linkedin.com/)

## 📜 Descrição

### 🌾 Problema do Agronegócio

O Brasil é líder mundial na produção de cana-de-açúcar, colhendo cerca de 620 milhões de toneladas por safra. Entretanto, o país enfrenta um problema crítico: **altas perdas durante a colheita mecânica**, que chegam a **15% da produção**, comparado a apenas **5% na colheita manual**.

Segundo avaliação da SOCICANA, essas perdas representam um prejuízo anual de **R$ 20 milhões** apenas no estado de São Paulo, considerando:
- Área plantada: ~3 milhões de hectares
- Produtividade: ~100 t/ha
- Percentual de perda mecânica: até 15%

### 💡 Solução Proposta

Este sistema **AgroTech** resolve o problema através de:

1. **Monitoramento de Perdas**: Cadastra dados de colheitas (manual e mecânica) com cálculo automático de perdas baseado em dados científicos
2. **Análise Comparativa**: Gera estatísticas e comparativos entre métodos de colheita
3. **Tomada de Decisão**: Relatórios detalhados para auxiliar produtores a otimizar processos
4. **Persistência de Dados**: Armazena histórico em JSON e Oracle Database para análises futuras

### 🎯 Diferencial e Inovação

- ✅ **Automatização**: Cálculos de perdas e prejuízos baseados em estudos da SOCICANA
- ✅ **Múltiplas Persistências**: Integração JSON + Oracle Database
- ✅ **Validação Robusta**: Impede entrada de dados inconsistentes
- ✅ **Usabilidade**: Interface via terminal limpa e intuitiva
- ✅ **Relatórios**: Exportação em TXT para análise offline

### 📚 Conteúdos Aplicados (Capítulos 3-6)

#### Capítulo 3 - Subalgoritmos
- ✅ Funções com passagem de parâmetros (`calcular_prejuizo`, `validar_numero_positivo`)
- ✅ Procedimentos com validação (`validar_data`, `validar_tipo_colheita`)
- ✅ Retorno de múltiplos valores com tuplas

#### Capítulo 4 - Estruturas de Dados
- ✅ **Listas**: Armazenamento de múltiplas colheitas em memória
- ✅ **Tuplas**: Retorno de funções (`calcular_prejuizo` retorna perda e prejuízo)
- ✅ **Dicionários**: Estrutura de cada colheita com chaves (fazenda, data, tipo, etc.)
- ✅ **Tabela de memória**: Lista de dicionários para gerenciar conjunto de dados

#### Capítulo 5 - Manipulação de Arquivos
- ✅ **JSON**: Persistência principal dos dados (`dados_colheitas.json`)
- ✅ **TXT**: Geração de relatórios detalhados (`relatorio.txt`)
- ✅ Leitura e escrita com tratamento de exceções

#### Capítulo 6 - Banco de Dados
- ✅ Conexão com Oracle Database via `oracledb`
- ✅ Operações CRUD completas
- ✅ Criação automática de tabelas
- ✅ Consultas SQL com agregações (SUM, COUNT, AVG)

## 📁 Estrutura de Pastas

```
sistema-perdas-cana/
├── .github/                 # Configurações GitHub
├── assets/                  # Imagens e recursos não-estruturados
├── config/                  # Arquivos de configuração
├── document/                # Documentação do projeto
│   ├── CONFIGURACAO.md      # Guia de configuração
│   ├── RELATORIO_VALIDACAO.md # Relatório de testes
│   └── other/               # Documentos complementares
├── scripts/                 # Scripts auxiliares
├── src/                     # Código fonte
│   ├── main.py              # Sistema principal com menu
│   ├── funcoes.py           # Subalgoritmos (validações e cálculos)
│   ├── database.py          # Conexão e operações Oracle
│   ├── cadastrar_exemplos.py # Script para popular banco de dados
│   ├── teste_oracle.py      # Teste de conexão Oracle
│   └── teste_sistema.py     # Testes do sistema
├── dados_colheitas.json     # Armazenamento local (gerado automaticamente)
├── relatorio.txt            # Relatório gerado (criado automaticamente)
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Este arquivo
```

## 🔧 Como Executar o Código

### Pré-requisitos

1. **Python 3.10 ou superior**
   ```bash
   python --version
   ```

2. **Biblioteca Oracle**
   ```bash
   pip install oracledb
   ```

3. **Acesso ao Oracle Database** (credenciais FIAP)

### Configuração do Banco de Dados

1. Abra o arquivo `src/database.py`
2. Configure suas credenciais Oracle:

```python
user='rmXXXXXX',        # Seu RM
password='sua_senha',    # Sua senha Oracle
dsn='oracle.fiap.com.br:1521/orcl'
```

### Instalação e Execução

**Passo 1:** Clone o repositório
```bash
git clone https://github.com/seu-usuario/sistema-perdas-cana.git
cd sistema-perdas-cana
```

**Passo 2:** Instale as dependências
```bash
pip install oracledb
```

**Passo 3:** Execute o sistema
```bash
python src/main.py
```

**Passo 4:** (Opcional) Popule o banco com dados de exemplo
```bash
python src/cadastrar_exemplos.py
```

### Testes

**Testar conexão Oracle:**
```bash
python src/teste_oracle.py
```

**Testar funcionalidades do sistema:**
```bash
python src/teste_sistema.py
```

## 📊 Funcionalidades

### Menu Principal

1. **Cadastrar Colheita**
   - Entrada de dados com validação completa
   - Cálculo automático de perdas (5% manual, 15% mecânica)
   - Cálculo de prejuízo (R$ 100/tonelada perdida)
   - Salvamento em JSON e Oracle

2. **Listar Colheitas (JSON)**
   - Visualização formatada dos dados locais
   - Informações completas de cada colheita

3. **Exibir Estatísticas (JSON)**
   - Total de colheitas
   - Total produzido (toneladas)
   - Total de perdas
   - Prejuízo acumulado

4. **Comparativo Manual vs Mecânica (JSON)**
   - Análise separada por tipo de colheita
   - Comparação de eficiência

5. **Gerar Relatório TXT**
   - Relatório completo exportado
   - Resumo executivo + detalhamento
   - Comparativo entre métodos

6. **Listar Colheitas (Oracle)**
   - Dados persistidos no banco
   - Visualização com ID de registro

7. **Estatísticas (Oracle)**
   - Agregações SQL
   - Médias e totais do banco

8. **Comparativo (Oracle)**
   - Análise por tipo de colheita
   - Dados do banco de dados

9. **Buscar por Fazenda**
   - Pesquisa em JSON e Oracle
   - Filtro por nome da fazenda

### Validações Implementadas

- ✅ **Números positivos**: Impede valores negativos ou zero
- ✅ **Tipo de colheita**: Aceita apenas "manual" ou "mecanica"
- ✅ **Data**: Valida formato DD/MM/AAAA
- ✅ **Entrada de tipo**: Valida se número foi digitado onde esperado
- ✅ **Campos vazios**: Não permite cadastro com dados incompletos

## 📈 Impacto no Agronegócio

### Benefícios para o Produtor

- 📊 **Monitoramento em tempo real** das perdas na colheita
- 💰 **Quantificação precisa** dos prejuízos financeiros
- 📈 **Análise histórica** para identificar padrões
- 🎯 **Tomada de decisão** baseada em dados concretos
- ⚖️ **Comparação objetiva** entre métodos de colheita

### Resultados Esperados

- Redução de perdas através de conscientização
- Otimização do método de colheita
- Melhor gestão de recursos
- Aumento da produtividade
- Contribuição para sustentabilidade do agronegócio

## 🗃 Histórico de Lançamentos

* 1.0.0 - 15/01/2025
    * Sistema completo com todas as funcionalidades
    * Integração JSON + Oracle Database
    * Validações e relatórios
    * Documentação completa

* 0.5.0 - 12/01/2025
    * Implementação do banco de dados Oracle
    * Funções de persistência e consulta

* 0.4.0 - 10/01/2025
    * Geração de relatórios TXT
    * Estatísticas e comparativos

* 0.3.0 - 08/01/2025
    * Manipulação de arquivos JSON
    * Estruturas de dados (listas, dicionários)

* 0.2.0 - 05/01/2025
    * Subalgoritmos de validação e cálculo
    * Funções com passagem de parâmetros

* 0.1.0 - 03/01/2025
    * Estrutura inicial do projeto
    * Menu e interface básica

## 📋 Licença

[![CC BY 4.0][cc-by-shield]][cc-by]

Este trabalho está licenciado sob [Creative Commons Attribution 4.0 International License][cc-by].

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

---

## 🙏 Agradecimentos

- **SOCICANA** - Pelos dados científicos sobre perdas na colheita
- **FIAP** - Pela oportunidade de desenvolver este projeto
- **Professores** - Pelo suporte e orientação técnica
- **Comunidade Python** - Pelas bibliotecas e recursos

---

**Desenvolvido com 🌾 para o Agronegócio Brasileiro**  
*Projeto Acadêmico - FIAP 2025*
