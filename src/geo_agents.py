import sqlite3

class GeoAgent:
    def __init__(self, db_path="hectron.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Crear tabla
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS geo_db (
                mineral TEXT PRIMARY KEY,
                description TEXT
            )
        ''')
        self.conn.commit()
        
        self.geo_db = {}
        self._load_geo_db()
        
        # Defaults si está vacía
        if not self.geo_db:
            self._load_default_geo()

    def _load_geo_db(self):
        self.cursor.execute("SELECT mineral, description FROM geo_db")
        rows = self.cursor.fetchall()
        for mineral, desc in rows:
            self.geo_db[mineral.lower()] = desc

    def _load_default_geo(self):
        defaults = {
            "silex": "Roca sedimentaria dura, usada históricamente para herramientas y encendido de fuego. Fractura concoidea.",
            "chert": "Variedad de cuarzo microcristalino, similar al sílex pero en nódulos calizos.",
            "calcita": "Mineral de carbonato de calcio (CaCO3). Reacciona con ácido. Dureza 3 en Mohs.",
            "cuarzo": "Mineral de sílice. Dureza 7. Piezoeléctrico.",
            "obsidiana": "Vidrio volcánico natural, fractura concoidea afilada. Herramientas prehistóricas.",
            "pirita": "Sulfuro de hierro (FeS2). Conocida como 'oro de tontos' por su brillo metálico."
        }
        for mineral, desc in defaults.items():
            self.add_knowledge(mineral, desc)

    def add_knowledge(self, mineral, description):
        mineral = mineral.lower()
        self.cursor.execute(
            "INSERT OR REPLACE INTO geo_db (mineral, description) VALUES (?, ?)",
            (mineral, description)
        )
        self.conn.commit()
        self.geo_db[mineral] = description

    def process(self, text):
        text_lower = text.lower()
        found = []
        for mineral, desc in self.geo_db.items():
            if mineral in text_lower:
                found.append(f"• {mineral.capitalize()}: {desc}")
        
        if found:
            return "Análisis geológico permanente 🪨:\n" + "\n".join(found)
        else:
            return "No encontrado en base permanente. Enseña con 'aprende sobre [mineral]: [descripción]'."

    def close(self):
        self.conn.close()