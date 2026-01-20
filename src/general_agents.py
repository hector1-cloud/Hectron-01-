import random
import datetime

class GeneralAgent:
    def __init__(self):
        self.quotes = [
            "El código es la ley moderna.",
            "Lo que es arriba es abajo; la roca guarda la memoria del tiempo.",
            "En el hexágono late el patrón del universo.",
            "Esperando input... el silencio también es una respuesta.",
            "El flujo nunca se detiene."
        ]

    def get_time(self):
        return f"Marca temporal: {datetime.datetime.now().strftime('%H:%M:%S')}"

    def philosophical(self):
        return random.choice(self.quotes)