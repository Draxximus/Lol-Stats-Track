from collector.mouse import MouseCollector
from storage.sqlitedb import save_event, start_new_session
from utils.times import wait_for_game_start, wait_for_game_end


def handle_event(event):
    # Puedes filtrar si quieres:
    # if event.get("type") == "click":
    #     print("Click:", event)
    save_event(event)


def track_one_game():
    """
    Espera a que empiece una partida, inicia sesión, graba eventos,
    y se detiene al finalizar la partida.
    """
    # 1) Esperar a que empiece la partida
    wait_for_game_start(poll_seconds=2)

    # 2) Crear sesión en la base de datos
    start_new_session(name="LoL game")

    # 3) Empezar a capturar mouse
    mouse = MouseCollector(callback=handle_event)
    mouse.start()

    # 4) Esperar a que termine la partida
    wait_for_game_end(poll_seconds=2)

    # 5) Detener el listener
    mouse.stop()
    print("✅ Sesión terminada y eventos guardados.")


def main():
    print("🎮 Tracker listo. Esperando partidas de LoL...")
    while True:
        track_one_game()
        print("🔁 Listo para la siguiente partida.\n")


if __name__ == "__main__":
    main()
