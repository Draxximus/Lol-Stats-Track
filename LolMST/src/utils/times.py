import time
import psutil

lol_process = [
    "League of Legends.exe",
    "Game.exe",
]
client_process = [
    "LeagueClient.exe",
    "LeagueClientUx.exe",
    "LeagueClientUxRender.exe",
]


def _is_any_running(names):
    for proc in psutil.process_iter(['name']):
        name = proc.info.get('name')
        if not name:
            continue
        if name in names:
            return True
    return False


def is_game_running() -> bool:
    """True si el proceso del juego (no solo el cliente) está corriendo."""
    return _is_any_running(lol_process)


def is_client_running() -> bool:
    """True si el cliente/launcher está abierto."""
    return _is_any_running(client_process)


def wait_for_game_start(poll_seconds: int = 2):
    """
    Espera hasta que empiece una partida (aparezca League of Legends.exe).
    """
    print("🔍 Esperando a que empiece la partida (League of Legends.exe)...")
    while True:
        if is_game_running():
            print("✅ Partida detectada, comenzando a capturar inputs.")
            return
        time.sleep(poll_seconds)


def wait_for_game_end(poll_seconds: int = 2):
    """
    Espera hasta que termine la partida (desaparezca League of Legends.exe).
    """
    print("⌛ Esperando a que termine la partida...")
    while True:
        if not is_game_running():
            print("🛑 Partida finalizada.")
            return
        time.sleep(poll_seconds)