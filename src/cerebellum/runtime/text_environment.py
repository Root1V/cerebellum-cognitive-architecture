
# 1. El ciclo cognitivo completo (los 7 módulos)
# Las arquitecturas modernas de agentes suelen ejecutar algo muy parecido a esto:
# Perception → Attention → Memory → Planning → Reasoning → Action → Learning
# y todo ocurre dentro de un Environment.

from ..core.environment import Environment


class TextEnvironment(Environment):

    def __init__(self, text: str):
        self.text = text

    def observe(self) -> str:
        return self.text

    def update(self, action) -> None:
        print("Environment received:", action)
        