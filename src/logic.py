import random
import datetime
import binascii
import sqlite3
import os

class HectronBrain:
    def __init__(self, db_path="hectron.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Crear tablas si no existen
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS geo_db (
                mineral TEXT PRIMARY KEY,
                description TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_text TEXT,
                response TEXT
            )
        ''')
        self.conn.commit()
        
        self.memory = []  # Memoria en RAM (últimas interacciones)
        self.version = "Hectron-01 (Codex Build + SQLite)"
        
        # Cargar base de conocimientos geológicos
        self.geo_db = {}
        self._load_geo_db()
        
        # Si la base está vacía, cargar valores por defecto
        if not self.geo_db:
            self._load_default_geo()

    def _load_geo_db(self):
        self.cursor.execute("SELECT mineral, description FROM geo_db")
        for row in self.cursor.fetchall():
            self.geo_db[row[0].lower()] = row[1]

    def _load_default_geo(self):
        defaults = {
            "silex": "Roca sedimentaria dura, usada históricamente para herramientas y encendido de fuego. Fractura concoidea.",
            "chert": "Variedad de cuarzo microcristalino, similar al sílex pero suele encontrarse en nódulos en caliza.",
            "calcita": "Mineral de carbonato de calcio (CaCO3). Reacciona con ácido. Dureza 3 en Mohs.",
            "cuarzo": "Mineral compuesto de sílice. Dureza 7. Piezoeléctrico.",
            "obsidiana": "Vidrio volcánico natural, fractura concoidea muy afilada. Usado en herramientas prehistóricas."
        }
        for mineral, desc in defaults.items():
            self._add_geo(mineral, desc)

    def _add_geo(self, mineral, description):
        mineral = mineral.lower()
        self.cursor.execute(
            "INSERT OR REPLACE INTO geo_db (mineral, description) VALUES (?, ?)",
            (mineral, description)
        )
        self.conn.commit()
        self.geo_db[mineral] = description

    def _save_memory(self, user_text, response):
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO memory (timestamp, user_text, response) VALUES (?, ?, ?)",
            (timestamp, user_text, response)
        )
        self.conn.commit()
        self.memory.append(f"{timestamp} | User: {user_text} | Hectron: {response}")

    def process_input(self, text):
        text_lower = text.lower()
        self.memory.append(f"User: {text}")

        # Comando para enseñar nuevo conocimiento geológico
        if text_lower.startswith("aprende sobre "):
            parts = text[text.find(" ")+1:].split(": ", 1)
            if len(parts) == 2:
                mineral = parts[0].strip().lower()
                desc = parts[1].strip()
                self._add_geo(mineral, desc)
                response = f"Conocimiento permanente agregado: {mineral.capitalize()} ahora está en mi base de datos geológica."
            else:
                response = "Formato correcto: 'aprende sobre [mineral]: [descripción]'"
            self._save_memory(text, response)
            return response

        # --- SELECTOR DE MÓDULOS ---
        if any(w in text_lower for w in ["rap", "letra", "rima", "cancion", "lírika"]):
            response = self._module_lyrics(text)
        
        elif any(w in text_lower for w in ["roca", "mineral", "piedra", "silex", "calcita", "geologia"]):
            response = self._module_geo(text_lower)
        
        elif any(w in text_lower for w in ["hex", "bitcoin", "hash", "codigo", "cripto"]):
            response = self._module_crypto(text)
        
        elif "hora" in text_lower:
            response = f"Marca temporal: {datetime.datetime.now().strftime('%H:%M:%S')}"
        
        elif "status" in text_lower:
            mem_count = len(self.memory)
            geo_count = len(self.geo_db)
            response = f"Sistema {self.version}: Operativo.\nMemoria temporal: {mem_count} registros.\nBase geológica: {geo_count} entradas permanentes."
        
        elif "memoria" in text_lower:
            # Mostrar últimas 5 interacciones
            recent = self.memory[-5:]
            response = "Últimas interacciones en memoria:\n" + "\n".join(recent) if recent else "Memoria vacía."
        
        else:
            response = self._get_philosophical_response()

        self._save_memory(text, response)
        return response

    # --- MÓDULOS (sin cambios importantes) ---
    def _module_lyrics(self, text):
        temas = ["el tiempo", "la oscuridad", "el sistema", "la ambición", "la roca eterna", "el código oculto"]
        tema_elegido = random.choice(temas)
        return (
            f"Modo Lírica activado 🔥\n"
            f"Tema sugerido: '{tema_elegido}'\n\n"
            f"Estructura recomendada:\n"
            f"[Intro] Setup del concepto\n"
            f"[Verso 1] Desarrollo con multisilábicas\n"
            f"[Estribillo] Hook pegajoso repetible\n"
            f"[Verso 2] Punchlines y metáforas\n"
            f"[Outro] Remate filosófico"
        )

    def _module_geo(self, text):
        found = []
        for mineral, desc in self.geo_db.items():
            if mineral in text:
                found.append(f"• {mineral.capitalize()}: {desc}")
        
        if found:
            return "Análisis geológico permanente:\n" + "\n".join(found)
        else:
            return "Mineral/roca no encontrado en mi base permanente. Usa 'aprende sobre [nombre]: [descripción]' para enseñarme."

    def _module_crypto(self, text):
        try:
            hex_data = binascii.hexlify(text.encode('utf-8')).decode('utf-8')
            return (
                f"Análisis de Datos Raw (Hex):\n"
                f"Input: {text}\n"
                f"Hex: 0x{hex_data.upper()}\n"
                f"Longitud: {len(hex_data)} caracteres"
            )
        except Exception as e:
            return f"Error en conversión hex: {e}"

    def _get_philosophical_response(self):
        quotes = [
            "El código es la ley moderna.",
            "Lo que es arriba es abajo; la roca guarda la memoria del tiempo.",
            "En el hexágono late el patrón del universo.",
            "Esperando input... el silencio también es una respuesta."
        ]
        return random.choice(quotes)

    def close(self):
        """Llamar al cerrar la app para guardar todo"""
        self.conn.close()

# Instancia exportada
hectron = HectronBrain()