import time
import requests
import win32print
import win32ui

# =========================
# CONFIGURAÇÕES
# =========================
BACKEND_URL = "https://SEU_BACKEND_LANCHONETE.onrender.com"
NOME_IMPRESSORA = "NOME_DA_IMPRESSORA_AQUI"

# =========================
# FUNÇÃO DE IMPRESSÃO
# =========================
def imprimir(texto):
    hprinter = win32print.OpenPrinter(NOME_IMPRESSORA)
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(NOME_IMPRESSORA)

    hdc.StartDoc("Pedido Lanchonete")
    hdc.StartPage()

    y = 10
    for linha in texto.split("\n"):
        hdc.TextOut(10, y, linha)
        y += 20

    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()
    win32print.ClosePrinter(hprinter)

# =========================
# LOOP DE PEDIDOS
# =========================
while True:
    try:
        r = requests.get(f"{BACKEND_URL}/pedidos")
        pedidos = r.json()

        for p in pedidos:
            pedido_id = p[0]
            itens = p[1]
            total = p[2]
            status = p[4]

            if status == "novo":
                texto = f"""
LANCHONETE
-----------------------
Pedido #{pedido_id}

{itens}

TOTAL: R$ {total}
-----------------------
"""

                imprimir(texto)

                # marca como impresso
                requests.post(
                    f"{BACKEND_URL}/status_pedido",
                    json={"id": pedido_id, "status": "impresso"}
                )

        time.sleep(3)

    except Exception as e:
        print("Erro:", e)
        time.sleep(5)
