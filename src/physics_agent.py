import sympy as sp
from sympy.physics.units import g, m, s, km, hour
from sympy import symbols, Eq, solve, latex

class PhysicsAgent:
    def __init__(self):
        self.t, self.v0, self.h = symbols('t v0 h')

    def _latex_wrap(self, expr):
        return f"\[ {latex(expr)} \]"

    def process(self, text):
        text_lower = text.lower()
        response = "⚡ Modo Física activado.\n"

        try:
            if "caída libre" in text_lower or "gravedad" in text_lower:
                if "altura" in text_lower:
                    h_val = sp.sympify(text_lower.split("altura")[-1].split()[0])
                    eq = Eq(self.h, (1/2)*g*t**2)
                    t_sol = solve(eq.subs(self.h, h_val), self.t)[1]  # positiva
                    v_sol = g * t_sol
                    response += f"Caída libre desde {h_val} m:\n"
                    response += f"Tiempo de caída: {self._latex_wrap(t_sol.evalf())} s\n"
                    response += f"Velocidad final: {self._latex_wrap(v_sol.evalf())} m/s"
                else:
                    response += f"Aceleración gravitacional: {self._latex_wrap(g)}"

            elif "movimiento parabólico" in text_lower or "proyectil" in text_lower:
                # Ejemplo simple: v0 y ángulo
                response += "Movimiento parabólico básico (próximamente más parámetros). Ejemplo simbólico:\n"
                response += f"Alcance máximo: {self._latex_wrap((v0**2 * sp.sin(2*sp.symbols('theta')))/g)}\n"
                response += f"Altura máxima: {self._latex_wrap((v0**2 * sp.sin(sp.symbols('theta'))**2)/(2*g))}"

            elif "energía" in text_lower:
                response += "Fórmulas de energía:\n"
                response += f"Cinética: {self._latex_wrap(sp.Rational(1,2)*symbols('m')*symbols('v')**2)}\n"
                response += f"Potencial gravitatoria: {self._latex_wrap(symbols('m')*g*symbols('h'))}"

            else:
                response += (
                    "Comandos disponibles:\n"
                    "- caída libre altura [valor] m\n"
                    "- movimiento parabólico [parámetros]\n"
                    "- energía cinética/potencial\n"
                    "- gravedad"
                )

        except Exception as e:
            response += f"Error físico: {str(e)}"

        return response