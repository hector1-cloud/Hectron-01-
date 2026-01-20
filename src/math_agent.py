import sympy as sp
from sympy import symbols, Eq, solve, diff, integrate, simplify, sympify, pretty

class MathAgent:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def process(self, text):
        text_lower = text.lower()
        response = ""

        try:
            # 1. Cálculos simples / evaluaciones
            if any(word in text_lower for word in ["calcular", "cuanto es", "evaluar", "resultado de"]):
                # Extraer la expresión (todo después de la última palabra clave)
                parts = text_lower.split()
                expr_str = " ".join(parts[parts.index(next(w for w in ["calcular", "es", "evaluar", "de"] if w in parts)) + 1:]) if any(w in parts for w in ["calcular", "es", "evaluar", "de"]) else text_lower
                expr = sympify(expr_str)
                result = expr.evalf() if expr.is_number else simplify(expr)
                response = f"Resultado:\n{pretty(result)}"
                if expr.is_number:
                    response += f"\n\nAproximación numérica: {expr.evalf(10)}"

            # 2. Resolver ecuaciones
            elif "resolver" in text_lower and "=" in text:
                eq_str = text[text.lower().find("resolver") + len("resolver"):].strip()
                if "=" in eq_str:
                    lhs, rhs = eq_str.split("=", 1)
                    eq = Eq(sympify(lhs.strip()), sympify(rhs.strip()))
                    sol = solve(eq, self.x)
                    response = f"Soluciones para {pretty(eq)}:\n"
                    for s in sol:
                        response += f"{pretty(s)}\n"

            # 3. Derivadas
            elif any(word in text_lower for word in ["derivar", "derivada", "diferenciar"]):
                func_str = text_lower.split("de")[-1].strip() if "de" in text_lower else text_lower
                func = sympify(func_str)
                deriv = diff(func, self.x)
                response = f"Derivada de {pretty(func)} respecto a x:\n{pretty(deriv)}\n"
                response += f"Simplificada:\n{pretty(simplify(deriv))}"

            # 4. Integrales (indefinidas)
            elif any(word in text_lower for word in ["integrar", "integral"]):
                func_str = text_lower.split("de")[-1].strip() if "de" in text_lower else text_lower
                func = sympify(func_str)
                integ = integrate(func, self.x)
                response = f"Integral indefinida de {pretty(func)} dx:\n{pretty(integ + sp.symbols('C'))}\n"
                response += f"Simplificada:\n{pretty(simplify(integ))}"

            else:
                response = (
                    "🧮 Modo Matemáticas activado.\n"
                    "Comandos disponibles:\n"
                    "- 'calcular [expresión]' → Ej: calcular 2 + 2*pi\n"
                    "- 'resolver [ecuación]' → Ej: resolver x^2 - 5x + 6 = 0\n"
                    "- 'derivar [función]' → Ej: derivar x^3 + sin(x)\n"
                    "- 'integrar [función]' → Ej: integrar e^x"
                )

        except Exception as e:
            response = f"Error al procesar la expresión matemática: {str(e)}\nIntenta con una sintaxis más clara."

        return response