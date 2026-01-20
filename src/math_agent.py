import sympy as sp
from sympy import symbols, Eq, solve, diff, integrate, limit, series, Matrix, pretty, latex, sympify

class MathAgent:
    def __init__(self):
        self.x, self.y, self.t = symbols('x y t')

    def _latex_wrap(self, expr):
        """Envuelve en \] para display math"""
        return f"\[ {latex(expr)} \]"

    def process(self, text):
        text_lower = text.lower()
        response = "🧮 Modo Matemáticas activado.\n"

        try:
            # Detectar tipo de comando
            if any(w in text_lower for w in ["calcular", "evaluar", "resultado"]):
                expr_str = text_lower.split(maxsplit=1)[1] if len(text_lower.split()) > 1 else text_lower
                expr = sympify(expr_str)
                result = expr.evalf() if expr.is_number else expr
                response += f"Resultado:\n{self._latex_wrap(result)}"

            elif "resolver" in text_lower and "=" in text:
                eq_str = text[text.lower().find("resolver") + len("resolver"):].strip()
                lhs, rhs = eq_str.split("=", 1)
                eq = Eq(sympify(lhs.strip()), sympify(rhs.strip()))
                sol = solve(eq)
                response += f"Ecuación: {self._latex_wrap(eq)}\nSoluciones:\n"
                for s in sol:
                    response += f"{self._latex_wrap(s)}\n"

            elif any(w in text_lower for w in ["derivar", "derivada"]):
                func_str = text_lower.split("de")[-1].strip()
                func = sympify(func_str)
                deriv = diff(func, self.x)
                response += f"Derivada de {self._latex_wrap(func)}:\n{self._latex_wrap(deriv)}"

            elif any(w in text_lower for w in ["integrar", "integral"]):
                parts = text_lower.split()
                if "definida" in text_lower:
                    # Ej: integral definida de x^2 de 0 a 1
                    func_str = parts[parts.index("de") + 1:parts.index("desde") if "desde" in parts else parts.index("de") + 2][0]
                    a = sympify(parts[parts.index("a") + 1])
                    b = sympify(parts[parts.index("de") + 1] if "de" in parts else parts[-1])
                    func = sympify(func_str)
                    integ = integrate(func, (self.x, a, b))
                    response += f"Integral definida ∫ {self._latex_wrap(func)} dx de {a} a {b}:\n{self._latex_wrap(integ)}"
                else:
                    func_str = text_lower.split("de")[-1].strip()
                    func = sympify(func_str)
                    integ = integrate(func, self.x)
                    response += f"Integral indefinida:\n{self._latex_wrap(integ + sp.symbols('C'))}"

            elif any(w in text_lower for w in ["limite", "límite"]):
                parts = text_lower.split("cuando")[-1].strip().split("tiende a")
                expr_str = text_lower.split("de")[1].split("cuando")[0].strip()
                expr = sympify(expr_str)
                value = sympify(parts[1].strip())
                lim = limit(expr, self.x, value)
                response += f"Límite de {self._latex_wrap(expr)} cuando x → {value}:\n{self._latex_wrap(lim)}"

            elif any(w in text_lower for w in ["serie", "taylor"]):
                parts = text_lower.split("alrededor de")
                expr_str = text_lower.split("de")[1].split("alrededor")[0].strip()
                point = sympify(parts[1].strip().split("orden")[0]) if len(parts) > 1 else 0
                n = int(parts[1].split("orden")[1]) + 1 if "orden" in text_lower else 6
                expr = sympify(expr_str)
                ser = series(expr, self.x, point, n)
                response += f"Serie de Taylor de {self._latex_wrap(expr)} alrededor de x={point}, orden {n-1}:\n{self._latex_wrap(ser)}"

            elif "matriz" in text_lower:
                # Ejemplo simple: "operaciones con matriz [[1,2],[3,4]] + [[5,6],[7,8]]"
                # Por ahora, evalúa expresión con Matrix
                expr_str = text_lower.split("matriz")[1].strip()
                expr = sympify(expr_str, locals={'Matrix': Matrix})
                response += f"Operación con matrices:\n{self._latex_wrap(expr)}"

            else:
                response += (
                    "Comandos disponibles:\n"
                    "- calcular [expr]\n"
                    "- resolver [eq = 0]\n"
                    "- derivar [f(x)]\n"
                    "- integrar [f(x)] (o 'integral definida ... desde a hasta b')\n"
                    "- límite de [expr] cuando x tiende a [valor]\n"
                    "- serie de Taylor de [f(x)] alrededor de [punto] orden [n]\n"
                    "- operaciones con matriz [[...]]"
                )

        except Exception as e:
            response += f"Error matemático: {str(e)}"

        return response