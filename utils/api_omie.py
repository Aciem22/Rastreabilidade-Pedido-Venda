import streamlit as st
import requests
import json
import calendar
from datetime import date, datetime
import time
import re

APP_KEY = st.secrets["APP_KEY"]
APP_SECRET = st.secrets["APP_SECRET"]

def consultar_pedido(numero_pedido, tentativas=5):
    url = "https://app.omie.com.br/api/v1/produtos/pedido/"
    payload = {
        "call": "ConsultarPedido",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [
            {"numero_pedido": numero_pedido}
        ]
    }
    for tentativa in range(1, tentativas + 1):
        print(f"🔹 Tentativa {tentativa} de {tentativas} para consultar pedido {numero_pedido}")
        response = requests.post(url, json=payload)
        resultado = response.json()

        fault = resultado.get("faultstring", "")
        if fault.startswith("ERROR: Consumo redundante"):
            match = re.search(r"(\d+) segundos", fault)
            segundos = int(match.group(1)) if match else 6
            print(f"⚠️ Consumo redundante detectado. Aguardando {segundos}s antes da próxima tentativa...")
            time.sleep(segundos)
        else:
            return resultado

    print("❌ Todas as tentativas foram usadas, retornando último resultado")
    return resultado

def alterar_pedido(codigo_pedido, novos_produtos, quantidade_caixas, tentativas=3):
    url = "https://app.omie.com.br/api/v1/produtos/pedido/"
    payload = {
        "call": "AlterarPedidoVenda",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": {
            "cabecalho": {
                "codigo_pedido": codigo_pedido
            },
            "frete": {
                "quantidade_volumes": quantidade_caixas,
                "especie_volumes": "CAIXAS"
            },
            "det": novos_produtos
        }
    }

    for tentativa in range(1, tentativas + 1):
        print(f"🔹 Tentativa {tentativa} de {tentativas} para alterar pedido {codigo_pedido}")
        response = requests.post(url, json=payload)
        resultado = response.json()

        fault = resultado.get("faultstring", "")
        if fault.startswith("ERROR: Consumo redundante"):
            match = re.search(r"(\d+) segundos", fault)
            segundos = int(match.group(1)) if match else 6
            print(f"⚠️ Consumo redundante detectado. Aguardando {segundos}s antes da próxima tentativa...")
            time.sleep(segundos)
        else:
            print("===== RETORNO DA API =====")
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
            print("===========================")
            return resultado

    print("❌ Todas as tentativas foram usadas, retornando último resultado")
    return resultado


def listar_remessas(data_formatada):
    URL = "https://app.omie.com.br/api/v1/produtos/remessa/"
    pagina = 1
    ha_mais_paginas = True
    remessas_dict = {}

    while ha_mais_paginas:
        payload = {
            "call": "ListarRemessas",
            "app_key": APP_KEY,
            "app_secret": APP_SECRET,
            "param": [
                {
                    "nPagina": pagina,
                    "nRegistrosPorPagina": 300,
                    "cExibirDetalhes": "N",
                    "dtAltDe": data_formatada
                }
            ]
        }

        response = requests.post(URL, json=payload)
        data = response.json()

        # Extrai as remessas da página atual
        remessas = data.get("remessas", [])
        if not remessas:
            ha_mais_paginas = False
            break

        for remessa in remessas:
            cabec = remessa.get("cabec", {})
            numero = cabec.get("cNumeroRemessa")
            codigo = cabec.get("nCodRem")
            if numero and codigo:
                remessas_dict[str(numero)] = codigo

        # Verifica se ainda há mais páginas
        total_paginas = data.get("nTotPaginas", 1)
        if pagina >= total_paginas:
            ha_mais_paginas = False
        else:
            pagina += 1

    # Log pra debug
    print("\n===== MAPA COMPLETO DE REMESSAS =====")
    for numero, codigo in remessas_dict.items():
        print(f"Remessa Nº {numero}  |  Código: {codigo}")
    print(f"Total de remessas coletadas: {len(remessas_dict)}")
    print("=====================================\n")

    return remessas_dict

