# Imports
from dotenv import load_dotenv
from pathlib import Path
import requests
import json
import re
import os

# Paths
pathRoot = Path(__file__).resolve().parent
pathLogs = pathRoot / "logs"
pathJson = pathRoot / "historicoIps.json"
pathIpdb = "https://api.abuseipdb.com/api/v2/check"

#carrega o .ENV
load_dotenv(pathRoot / ".env")
API_KEY = os.getenv("API_KEY")

# Verificação dos LOGS
def verificarLogs():

    # Verifica se a pasta existe
    if not pathLogs.is_dir():
        return "Pasta de logs não encontrada"

    # Pega todos os arquivos txt da pasta
    arquivosTxt = list(pathLogs.glob("*.txt"))

    # Contador dos erros por IP
    contadorIps = {}
    padraoIp = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

    # For para leitura dos arquivos
    for url in arquivosTxt:
        try:
            # lê o arquivo
            with open(url, mode="r", encoding="utf-8") as arquivo:

                for linha in arquivo:
                    if ("ACCESS DENIED" in linha.upper() or "FALHA" in linha.upper()):

                        resultadoBusca = re.search(padraoIp, linha)

                        if resultadoBusca:
                            ipEncontrado = resultadoBusca.group()
                            contadorIps[ipEncontrado] = contadorIps.get(ipEncontrado, 0) + 1
        except Exception as e:
            print(f"Erro ao processar o arquivo {url}: {e}")

            

    return contadorIps

# Compara os logs com o json
def verificarJson(Ips):

    if not pathJson.is_file():
            return "Arquivo Json não encontrada"

    # Abre o json
    with open(pathJson, mode = 'r', encoding = 'utf-8') as arquivo:
        dados = json.load(arquivo)

    # Lista dos ips a serem verificados
    verificar = {}

    for ipEncontrado, tentativasLog in Ips.items():
        try:
            if ipEncontrado in dados:
                dados[ipEncontrado]["tentativas_erro"] += tentativasLog
                print(f"IP conhecido atualizado: {ipEncontrado}")

            else:
                verificar[ipEncontrado] = tentativasLog
                print(f"IP novo detectado: {ipEncontrado}")

                resultado = checarIp(ipEncontrado)

                score = resultado.get("abuseConfidenceScore", 0)
                if score < 50:
                    dados[ipEncontrado] = {
                        "ultima_verificacao": "2026-10-13", 
                        "tentativas_erro": tentativasLog,
                        "status": "Seguro",
                        "detalhes_api": f"Score AbuseIPDB: {score}"
                    }
                    addInJson(dados)
                else:
                    dados[ipEncontrado] = {
                        "ultima_verificacao": "2026-10-13",
                        "tentativas_erro": tentativasLog,
                        "status": "Perigoso",
                        "detalhes_api": f"Score AbuseIPDB: {score}"
                    }
                    addInJson(dados)     
        except Exception as e:
            print(f"Erro ao processar o IP {ipEncontrado}: {e}")



    return verificar

# Verifica o ip usando o abuseipdb
def checarIp(ip):
    parametros = {"ipAddress": ip, "maxAgeInDays": "90"}
    headers = {"Accept": "application/json", "Key": API_KEY}

    try:
        resposta = requests.get(pathIpdb, headers = headers, params = parametros, timeout=10)

        if resposta.status_code == 200:
            dadosApi = resposta.json()
            return dadosApi.get("data", {})
    except:
        print(f"Erro na API para o IP {ip}: Código {resposta.status_code}")
        return None 

# Verifica os Ips
def addInJson(dados):

    try:
        with open(pathJson, mode='w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Erro ao salvar dados no JSON: {e}")

verificarJson(verificarLogs())