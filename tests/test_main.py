
from my_project.main import somme

def test_somme():
    """Test the somme function."""
    assert somme(1, 2) == 3
    assert somme(-1, 1) == 0
    assert somme(0, 0) == 0
    assert somme(100, 200) == 300
    assert somme(-5, -5) == -10
    assert somme(1.5, 2.5) == 4.0
    assert somme(-1.5, 1.5) == 0.0