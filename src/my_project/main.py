

from my_project.config import Environnement, ExempleEnum
def somme(a, b):
    """Returns the sum of two numbers."""
    return a + b


if __name__ == "__main__":
    # Accès aux variables d'environnement
    env1 = Environnement.config("ENV_VAR_EXEMPLE")

    # Accès à l'énumération
    value1 = ExempleEnum.VALUE1.value