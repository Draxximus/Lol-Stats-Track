from collector.mouse import MouseCollector
from storage.sqlitedb import save_event, start_new_session
from utils.times import wait_for_game_start, wait_for_game_end


def handle_event(event):
   
    save_event(event)


def track_one_game():
    wait_for_game_start(poll_seconds=2)
    start_new_session(name="LoL game")
    mouse = MouseCollector(callback=handle_event)
    mouse.start()
    wait_for_game_end(poll_seconds=2)
    mouse.stop()
    print("Sesión terminada y eventos guardados.")

def main():
    print("Tracker listo. Esperando partidas de LoL...")
    while True:
        track_one_game()
        print("Listo para la siguiente partida.\n")


if __name__ == "__main__":
    main()

