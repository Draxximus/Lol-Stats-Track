import os

from storage.sqlitedb import load_events, get_latest_session_id, DB_PATH
from processors.heatmap import create_mouse_heatmap


def main():
    print(f"[HEATMAP] Usando base de datos SQLite: {DB_PATH}")

    # 1) Obtener la última sesión (última partida)
    session_id = get_latest_session_id()
    if session_id is None:
        print("⚠ No hay sesiones registradas todavía. Juega una partida primero.")
        return

    print(f"[HEATMAP] Usando la sesión más reciente: id={session_id}")

    # 2) Cargar eventos SOLO de esa sesión
    events = load_events(session_id=session_id)
    if not events:
        print("⚠ La sesión no tiene eventos. ¿Se grabó bien el tracker?")
        return

    # 3) Carpeta de salida dentro del proyecto
    base_dir = os.path.dirname(os.path.dirname(__file__))  # carpeta LolMST
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    output_path = os.path.join(
        processed_dir,
        f"mouse_heatmap_session_{session_id}.png"
    )

    print(f"[HEATMAP] Guardando heatmap en: {output_path}")

    # 4) Generar heatmap solo con clicks (como antes)
    create_mouse_heatmap(
        events,
        output_path=output_path,
        only_click = True,
        bins=120,
    )


if __name__ == "__main__":
    main()
