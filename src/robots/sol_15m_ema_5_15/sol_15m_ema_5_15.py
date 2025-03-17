import time
import os
import json
# Vamos supor que você queira manter esse intervalo como se fosse o "tempo de cada candle"
SLEEP_TIME = 5

def sol_15m_ema_5_15 ():
    
    base_dir = os.path.dirname(__file__)
    json_file = os.path.join(base_dir, "parameters.json")
    
    with open(json_file, "r", encoding="utf-8") as f:
        params = json.load(f)

    SLEEP_TIME    = params.get("SLEEP_TIME", 5)
    
    print("Robo SOL")
    
    while True:
        print("\nEntrou no while — aqui você pode colocar testes do robô ou prints de debug.")
        
        # Se quiser simular alguma lógica de "aguardar candle",
        # basta manter o sleep (ou até consultar a API de velas, mas não vamos usar aqui).
        time.sleep(SLEEP_TIME)

        print("Sai do while, mas ele retornará no próximo 'candle' (após o sleep).")

if __name__ == "__main__":
    sol_15m_ema_5_15 ()