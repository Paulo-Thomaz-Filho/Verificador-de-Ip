# 🛡️ Guarda de Segurança Virtual

> Sistema automatizado em Python para análise de logs de servidor, detecção de IPs maliciosos e consulta de inteligência de ameaças.

## 📋 Sobre o Projeto

O Guarda de Segurança Virtual é um script autônomo projetado para monitorar atividades suspeitas em servidores. Ele analisa automaticamente os arquivos de log, identifica endereços IP que falharam repetidamente em tentativas de login e consulta uma base de dados global de segurança para avaliar o risco de cada endereço, armazenando o histórico localmente para otimizar futuras consultas.

### 🎯 Principais Funcionalidades

* **Leitura e Extração Inteligente**: Varre arquivos `.txt` na pasta de logs e utiliza Expressões Regulares (Regex) para identificar endereços IPv4.
* **Filtro de Ameaças**: Captura especificamente as linhas de log que contenham os termos "ACCESS DENIED" ou "FALHA".
* **Gestão de Cache Local (Banco de Dados)**: Verifica um arquivo `historicoIps.json` antes de realizar consultas externas. Atualiza as tentativas de erro de IPs já conhecidos, evitando o desperdício de requisições.
* **Inteligência Externa via API**: Conecta-se à API pública do AbuseIPDB para investigar IPs inéditos.
* **Classificação de Risco**: Avalia o "Confidence Score" da API. IPs com pontuação menor que 50 são catalogados como "Seguro", enquanto pontuações maiores ou iguais a 50 são marcadas como "Perigoso".

## 🚀 Tecnologias Utilizadas

### Linguagem e Bibliotecas Nativas

* **Python**: Linguagem principal de desenvolvimento.
* **re (Regular Expressions)**: Para extração e validação do padrão numérico dos IPs.
* **json**: Para manipulação, leitura e escrita do banco de dados local estruturado.
* **pathlib**: Para gerenciamento seguro e multiplataforma dos caminhos de diretórios e arquivos.

### Dependências Externas

* **requests**: Realização de requisições HTTP (`GET`) para comunicação com a API do AbuseIPDB.
* **python-dotenv**: Carregamento seguro das variáveis de ambiente e credenciais a partir do arquivo `.env`.

## 📁 Estrutura do Projeto

```text
C:/
├── exemplo.env           # Modelo de variáveis de ambiente para configuração
├── historicoIps.json     # Banco de dados local em formato JSON
├── main.py               # Script principal com toda a lógica de verificação
├── readme.md             # Documentação do projeto
└── logs/                 # Diretório contendo os arquivos brutos do servidor
    ├── log1.txt
    ├── log2.txt
    ├── log3.txt
    ├── log4.txt
    └── log5.txt

```

## 🛠️ Instalação e Configuração

### Pré-requisitos

* Python 3.x instalado
* Gerenciador de pacotes `pip`

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/Paulo-Thomaz-Filho/seu-repositorio.git
cd seu-repositorio

```

2. **Crie e ative um ambiente virtual (Recomendado)**

```bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

```

3. **Instale as dependências**

```bash
pip install requests python-dotenv

```

4. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto (utilizando o `exemplo.env` como base) e insira a sua credencial:

```env
API_KEY=seu_token_gigante_do_abuseipdb_aqui

```

5. **Execute a aplicação**
Coloque seus arquivos de texto com os registros na pasta `logs/` e rode o script:

```bash
python main.py

```

## 📡 Integração AbuseIPDB

O projeto utiliza a API RESTful V2 do AbuseIPDB para checagem de IPs.

### Como obter a chave de acesso (API Key)

1. Acesse o portal do [AbuseIPDB](https://www.abuseipdb.com/) e crie uma conta gratuita.
2. Navegue até a seção de API e gere uma nova chave de acesso.
3. Insira o código gerado na variável `API_KEY` dentro do seu arquivo `.env`[cite: 10, 11].

### Retorno de Dados

Os dados processados pela API são gravados diretamente no `historicoIps.json` contendo o status final e a pontuação técnica (`Score AbuseIPDB`), facilitando auditorias futuras[cite: 9, 10].
