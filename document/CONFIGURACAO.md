# 🔧 GUIA DE CONFIGURAÇÃO

## 📋 Pré-requisitos

1. **Python 3.10 ou superior**
   ```bash
   python --version
   ```

2. **Biblioteca oracledb**
   ```bash
   pip install oracledb
   ```

---

## 🗄️ Configuração do Banco de Dados Oracle

### Passo 1: Editar credenciais

Abra o arquivo [database.py](database.py) e localize a função `conectar_oracle()` (linha 23):

```python
def conectar_oracle():
    try:
        conn = oracledb.connect(
            user='SEU_RM',          # ⬅️ ALTERE AQUI
            password='SUA_SENHA',   # ⬅️ ALTERE AQUI
            dsn='oracle.fiap.com.br:1521/ORCL'
        )
```

**Substitua:**
- `SEU_RM` → Seu RM da FIAP (ex: `rm568506`)
- `SUA_SENHA` → Sua senha do Oracle

### Passo 2: Testar conexão

Execute o teste do Oracle:

```bash
python teste_oracle.py
```

**Resultado esperado:**
```
✅ Conexão estabelecida com sucesso!
✅ Tabela criada/verificada com sucesso!
✅ Colheita inserida com sucesso!
...
✅ TODOS OS TESTES DE ORACLE PASSARAM!
```

### Possíveis erros:

#### Erro ORA-01017 (usuário/senha inválidos)
```
❌ Erro: ORA-01017: invalid username/password; logon denied
```
**Solução:** Verifique se o RM e senha estão corretos em [database.py](database.py:24)

#### Erro de conexão (rede)
```
❌ Erro: Cannot connect to Oracle Database
```
**Solução:**
- Verifique se está conectado à rede FIAP (VPN se necessário)
- Teste: `ping oracle.fiap.com.br`

#### Erro ORA-00955 (tabela já existe)
```
⚠️  Tabela 'colheitas_cana' já existe. Prosseguindo...
```
**Isso é NORMAL!** A tabela foi criada anteriormente.

---

## ▶️ Executando o Sistema

### Execução normal:
```bash
python main.py
```

### Execução com validação:
```bash
# Testar cálculos e estruturas
python teste_sistema.py

# Testar banco de dados
python teste_oracle.py
```

---

## 🧪 Testes Automatizados

### 1. Teste de cálculos e estruturas
```bash
python teste_sistema.py
```

**Valida:**
- ✅ Cálculos de perda (5% manual, 15% mecânica)
- ✅ Cálculos de prejuízo
- ✅ Estruturas de dados (lista, tupla, dicionário)
- ✅ Manipulação JSON e TXT
- ✅ Funções de busca

### 2. Teste do banco Oracle
```bash
python teste_oracle.py
```

**Valida:**
- ✅ Conexão com Oracle
- ✅ Criação de tabela (DDL)
- ✅ Operações CRUD (INSERT, SELECT, UPDATE, DELETE)
- ✅ Consultas com filtros
- ✅ Estatísticas agregadas

---

## 📂 Arquivos Gerados

Durante o uso do sistema, os seguintes arquivos são criados:

### `dados_colheitas.json`
Armazena todas as colheitas localmente em formato JSON.

**Exemplo:**
```json
[
    {
        "fazenda": "Fazenda São José",
        "data": "15/10/2025",
        "tipo_colheita": "manual",
        "toneladas": 500.0,
        "perda_percentual": 0.05,
        "perda_toneladas": 25.0,
        "prejuizo_reais": 3750.0
    }
]
```

### `relatorio.txt`
Relatório detalhado gerado pela opção 5 do menu.

**Contém:**
- Resumo geral (total de colheitas, perdas, prejuízos)
- Detalhamento de cada colheita
- Comparativo manual vs mecânica

---

## 🔒 Segurança

### ⚠️ IMPORTANTE:

**NÃO comite suas credenciais no GitHub!**

Se você já commitou suas credenciais por engano:

1. **Altere a senha no Oracle imediatamente**
2. **Remova do histórico do Git:**
   ```bash
   # Edite database.py e remova as credenciais
   # Depois:
   git add database.py
   git commit --amend
   git push --force
   ```

### Boa prática:

Use variáveis de ambiente:

```python
import os

def conectar_oracle():
    user = os.getenv('ORACLE_USER', 'SEU_RM')
    password = os.getenv('ORACLE_PASS', 'SUA_SENHA')

    conn = oracledb.connect(
        user=user,
        password=password,
        dsn='oracle.fiap.com.br:1521/ORCL'
    )
```

Execute:
```bash
export ORACLE_USER='seu_rm'
export ORACLE_PASS='sua_senha'
python main.py
```

---

## 📊 Estrutura do Banco de Dados

### Tabela: `colheitas_cana`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | NUMBER | Chave primária (auto incremento) |
| `fazenda` | VARCHAR2(100) | Nome da fazenda |
| `data_colheita` | DATE | Data da colheita |
| `tipo_colheita` | VARCHAR2(20) | 'manual' ou 'mecanica' |
| `toneladas` | NUMBER(10,2) | Toneladas colhidas |
| `perda_percentual` | NUMBER(5,2) | Percentual de perda (0.05 ou 0.15) |
| `perda_toneladas` | NUMBER(10,2) | Toneladas perdidas |
| `prejuizo_reais` | NUMBER(12,2) | Prejuízo em reais |
| `data_cadastro` | TIMESTAMP | Data/hora do cadastro |

### SQL de criação:
```sql
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
);
```

---

## 🆘 Suporte

### Problemas comuns:

1. **"ModuleNotFoundError: No module named 'oracledb'"**
   ```bash
   pip install oracledb
   ```

2. **"Permission denied" no macOS**
   ```bash
   chmod +x main.py
   python3 main.py
   ```

3. **Caracteres especiais não aparecem (Windows)**
   - Use Windows Terminal ou PowerShell
   - Configure: `chcp 65001` (UTF-8)

4. **Erro ao abrir arquivo JSON**
   - Verifique se `dados_colheitas.json` existe
   - O sistema cria automaticamente se não existir

---

## 📝 Checklist de Validação

Antes de entregar o projeto, verifique:

- [ ] Python 3.10+ instalado
- [ ] Biblioteca oracledb instalada
- [ ] Credenciais Oracle configuradas em [database.py](database.py)
- [ ] Testes executados com sucesso (`teste_sistema.py`)
- [ ] Sistema principal funcionando (`python main.py`)
- [ ] Relatório TXT gerado corretamente
- [ ] Dados salvos em JSON
- [ ] README.md atualizado
- [ ] Código no GitHub
- [ ] **Credenciais NÃO commitadas no GitHub**

---

**Desenvolvido para FIAP - 2025**
