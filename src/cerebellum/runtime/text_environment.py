
# 1. El ciclo cognitivo completo (los 7 módulos)
# Las arquitecturas modernas de agentes suelen ejecutar algo muy parecido a esto:
# Perception → Attention → Memory → Planning → Reasoning → Action → Learning
# y todo ocurre dentro de un Environment.

class TextEnvironment:

    def __init__(self, text):
        self.text = text

    def observe(self):
        return self.text

    def update(self, action):
        print("Environment received:", action)
        