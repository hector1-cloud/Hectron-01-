import binascii

class CryptoAgent:
    def process(self, text):
        try:
            hex_data = binascii.hexlify(text.encode('utf-8')).decode('utf-8')
            return (
                f"Análisis de Datos Raw (Hexadecimal):\n"
                f"Input: \"{text}\"\n"
                f"Hex: 0x{hex_data.upper()}\n"
                f"Longitud: {len(hex_data)} caracteres\n"
                f"Patrón detectado: {'Repetitivo' if len(set(hex_data)) < 10 else 'Complejo'}"
            )
        except Exception as e:
            return f"Error en análisis cripto: {e}"