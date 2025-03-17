import time
import json
import os

from src.robots.sol_15m_ema_5_15.sol_15m_ema_5_15 import sol_15m_ema_5_15
from src.robots.btc_5m_ema_5_15.btc_5m_ema_5_15 import btc_5m_ema_5_15

ROBOS = {
    "sol_15m_ema_5_15": sol_15m_ema_5_15,
    "btc_5m_ema_5_15": btc_5m_ema_5_15
}

CONFIG_FILE = "config.json"

def carregar_robo_ativo():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config.get("robo_ativo")

while True:
    # Primeiro, lê o robô ativo do config.json
    robo_ativo = carregar_robo_ativo()
    
    # Sempre que entrar no loop, imprime qual robô está configurado
    print(f"\n[LOOP] Robô ativo no config.json: {robo_ativo}")

    if robo_ativo not in ROBOS:
        print(f"[ERRO] Robô '{robo_ativo}' não encontrado.")
        time.sleep(5)
        continue

    print(f"[INFO] Executando robô: {robo_ativo}")

    # Aqui assume-se que cada robô é uma função principal com seu próprio loop interno
    try:
        ROBOS[robo_ativo]()  # Chama o robô
    except Exception as e:
        print(f"[ERRO] Falha ao executar o robô '{robo_ativo}': {str(e)}")

    # Aguarda alguns segundos antes de verificar novamente se o robô ativo mudou
    time.sleep(5)
