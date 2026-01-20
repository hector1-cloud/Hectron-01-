from agents.lyrics_agent import LyricsAgent
from agents.crypto_agent import CryptoAgent
from agents.geo_agent import GeoAgent
from agents.general_agent import GeneralAgent

class HectronBrain:
    def __init__(self):
        self.memory = []  # Conversaciones temporales
        self.version = "Hectron-01 (Multi-Agent Codex Build)"
        
        # Instanciar agentes especializados
        self.lyrics = LyricsAgent()
        self.crypto = CryptoAgent()
        self.geo = GeoAgent()
        self.general = GeneralAgent()

    def process_input(self, text):
        text_lower = text.lower()
        self.memory.append(f"User: {text}")

        # Comando aprender (solo geo)
        if text_lower.startswith("aprende sobre "):
            parts = text[len("aprende sobre "):].split(": ", 1)
            if len(parts) == 2:
                mineral = parts[0].strip()
                desc = parts[1].strip()
                response = self.geo.add_knowledge(mineral, desc)
                response = f"🪨 {response}"
            else:
                response = "Formato: 'aprende sobre [mineral]: [descripción]'"
        # Routing
        elif any(w in text_lower for w in ["rap", "letra", "rima", "cancion", "lirica", "lírika"]):
            response = self.lyrics.process(text)
        elif any(w in text_lower for w in ["roca", "mineral", "piedra", "geologia", "geo"]):
            response = self.geo.process(text)
        elif any(w in text_lower for w in ["hex", "bitcoin", "hash", "codigo", "cripto"]):
            response = self.crypto.process(text)
        elif "hora" in text_lower:
            response = self.general.get_time()
        elif "status" in text_lower:
            response = f"{self.version}: Operativo.\nAgentes cargados: 4\nBase geo: {len(self.geo.geo_db)} entradas\nMemoria temporal: {len(self.memory)}"
        elif "memoria" in text_lower:
            recent = self.memory[-10:]  # Últimas 10 para más contexto
            response = "Memoria reciente:\n" + "\n".join(recent) if recent else "Vacía."
        else:
            response = self.general.philosophical()

        self.memory.append(f"Hectron: {response}")
        return response

    def close(self):
        self.geo.close()

hectron = HectronBrain()