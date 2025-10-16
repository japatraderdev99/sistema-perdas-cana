# Sistema de Monitoramento de Perdas na Colheita de Cana-de-Açúcar

## 🌾 Problema do Agronegócio

Este sistema resolve o problema das **altas perdas na colheita mecânica de cana-de-açúcar**, que chegam a **15% da produção**, causando prejuízo de **R$ 20 milhões/ano** só em São Paulo.

Segundo estudos da SOCICANA:
- **Colheita manual**: perdas de até 5%
- **Colheita mecânica**: perdas de até 15%

## 💡 Solução Proposta

Sistema AgroTech que:
- ✅ Cadastra dados de colheitas (manual e mecânica)
- ✅ Calcula perdas e prejuízos em reais automaticamente
- ✅ Gera relatórios comparativos e estatísticas
- ✅ Armazena histórico em JSON e Oracle Database
- ✅ Valida todas as entradas do usuário
- ✅ Oferece interface via terminal com usabilidade otimizada

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Oracle Database** (conexão via oracledb)
- **JSON** (armazenamento local)
- **Arquivos TXT** (relatórios)

## 📚 Conteúdos Aplicados

### Capítulo 3 - Subalgoritmos
- ✅ Funções com passagem de parâmetros
- ✅ Procedimentos com validação de dados
- ✅ Retorno de múltiplos valores (tuplas)

### Capítulo 4 - Estruturas de Dados
- ✅ **Listas**: armazenamento de colheitas
- ✅ **Tuplas**: retorno de cálculos
- ✅ **Dicionários**: estrutura de dados de colheita
- ✅ Tabela de memória (lista de dicionários)

### Capítulo 5 - Manipulação de Arquivos
- ✅ **JSON**: persistência de dados
- ✅ **TXT**: geração de relatórios

### Capítulo 6 - Banco de Dados
- ✅ Conexão com Oracle Database
- ✅ Operações CRUD
- ✅ Criação de tabelas
- ✅ Consultas SQL

## 🚀 Como Executar

### Pré-requisitos
```bash
# Instalar Python 3.10 ou superior
# Instalar biblioteca Oracle
pip install oracledb
```

### Configuração do Banco de Dados
1. Abra o arquivo `database.py`
2. Configure suas credenciais Oracle:
```python
user='rm568506',        # Altere aqui
password='ThinkAbout@1',  # Altere aqui
```

### Execução
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
sistema-perdas-cana/
├── main.py                  # Sistema principal com menu
├── funcoes.py               # Subalgoritmos (validação e cálculos)
├── database.py              # Conexão e operações Oracle
├── dados_colheitas.json     # Armazenamento local
├── relatorio.txt            # Relatório gerado (criado automaticamente)
└── README.md                # Documentação
```

## 📊 Funcionalidades

### 1. Cadastrar Colheita
- Nome da fazenda
- Data da colheita
- Tipo (manual/mecânica)
- Toneladas colhidas
- Cálculo automático de perdas e prejuízos

### 2. Listar Colheitas
- Visualização dos dados armazenados em JSON
- Informações formatadas e organizadas

### 3. Estatísticas
- Total de colheitas cadastradas
- Total de toneladas produzidas
- Prejuízo total acumulado

### 4. Relatório TXT
- Geração de relatório detalhado
- Exportação para arquivo texto

### 5. Consulta Oracle
- Visualização de dados persistidos no banco
- Total de registros armazenados

## 🎯 Diferenciais da Solução

### Validação de Dados
- ✅ Impede entrada de valores negativos
- ✅ Valida tipos de dados (números vs texto)
- ✅ Garante consistência na entrada do tipo de colheita

### Usabilidade
- ✅ Interface limpa e organizada
- ✅ Mensagens de feedback claras
- ✅ Navegação intuitiva por menu

### Inovação
- ✅ Automatiza cálculo de perdas baseado em dados científicos
- ✅ Integração de múltiplas formas de persistência (JSON + Oracle)
- ✅ Geração de relatórios para tomada de decisão

## 📈 Impacto no Agronegócio

Este sistema permite que produtores de cana-de-açúcar:
- Monitorem perdas em tempo real
- Comparem eficiência entre colheita manual e mecânica
- Tomem decisões baseadas em dados concretos
- Reduzam prejuízos através de análise histórica

## 👥 Integrantes

- **Gabriel Casarin** - Desenvolvedor
- **Claude AI** - Assistente de Desenvolvimento

## 📝 Licença

Projeto acadêmico desenvolvido para a disciplina de Python - FIAP

---

**Desenvolvido com 🌾 para o Agronegócio Brasileiro**
