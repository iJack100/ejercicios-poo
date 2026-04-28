import json
import os
from datetime import datetime

class AramXpcTracker:
    def __init__(self, filename="xpc_history.json"):
        self.filename = filename
        self.matches = self.load_data()

    def load_data(self):
        """Carga el historial de partidas desde un archivo JSON si existe."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def save_data(self):
        """Guarda el historial de partidas en un archivo JSON."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.matches, file, indent=4)

    def add_match(self, result, kills, deaths, assists, xpc_gained):
        """Registra una nueva partida con su KDA y el expc obtenido."""
        match = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "result": result.upper(),
            "kda": f"{kills}/{deaths}/{assists}",
            "xpc": xpc_gained
        }
        self.matches.append(match)
        self.save_data()
        print(f"✅ Partida registrada ({match['result']}). KDA: {match['kda']} | +{match['xpc']} expc.")

    def show_stats(self):
        """Muestra un resumen de la experiencia y el winrate."""
        if not self.matches:
            print("No hay partidas registradas aún.")
            return

        total_xpc = sum(match['xpc'] for match in self.matches)
        wins = sum(1 for match in self.matches if match['result'] == 'VICTORIA')
        total_matches = len(self.matches)
        winrate = (wins / total_matches) * 100
        
        print(f"\n--- 📊 ESTADÍSTICAS DE ARAM ---")
        print(f"Partidas jugadas: {total_matches}")
        print(f"Tasa de victorias (Winrate): {winrate:.1f}%")
        print(f"Total de Account Experience (xpc) acumulada: {total_xpc}")
        print("-------------------------------\n")

if __name__ == "__main__":
    # Instanciamos el tracker
    tracker = AramXpcTracker()
    
    # 1. Puedes borrar o comentar estas líneas después de la primera prueba
    print("Iniciando simulador de registro...\n")
    tracker.add_match("Victoria", 12, 5, 20, 185)
    tracker.add_match("Derrota", 5, 10, 15, 110)
    
    # 2. Mostramos el resumen de los datos guardados
    tracker.show_stats()
