import requests
from datetime import date, timedelta

def obtener_valor_dolar_bcentral():
    user = "jo.romeroc@duocuc.cl"
    password = "Joaco2005"
    fecha_hoy = date.today().strftime("%Y-%m-%d")

    for i in range(5):
        fecha = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")

        url = (
            "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
            f"?user={user}&pass={password}"
            f"&firstdate={fecha}&lastdate={fecha}"
            f"&timeseries=F073.TCO.PRE.Z.D&function=GetSeries"
        )

    response = requests.get(url)
    if response.status_code != 200:
        print("Error HTTP:", response.status_code)
        return None

    try:
        data = response.json()  # Aquí parseamos directamente JSON
    except Exception as e:
        print("Error al decodificar JSON:", e)
        return None

    if data.get("Codigo") != 0:
        print("Error en la API:", data.get("Descripcion"))
        return None

    series = data.get("Series")
    if not series:
        print("No hay series en la respuesta")
        return None

    obs = series.get("Obs", [])
    if not obs:
        print("No hay observaciones para la fecha")
        return None

    valor = obs[0].get("value")
    if valor is None:
        print("No hay valor en la observación")
        return None

    return float(valor)
