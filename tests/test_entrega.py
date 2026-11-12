import pytest
from scripts.preparar_entrega import recopilar, verificar_contenidos, ARCHIVOS_RAIZ


def test_lista_explicita_excluye_env_y_originales(tmp_path):
    for name in ARCHIVOS_RAIZ:
        (tmp_path / name).write_text("archivo publico")
    (tmp_path / ".env").write_text("credencial privada")
    (tmp_path / "documento_privado.pdf").write_bytes(b"privado")
    files = recopilar(tmp_path)
    assert ".env" not in files and "documento_privado.pdf" not in files
    assert ".env.example" in files


def test_rechaza_env_escondido_y_symlink(tmp_path):
    for name in ARCHIVOS_RAIZ:
        (tmp_path / name).write_text("ok")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/.env").write_text("privado")
    with pytest.raises(ValueError, match="entorno"):
        recopilar(tmp_path)
    (tmp_path / "docs/.env").unlink()
    (tmp_path / "docs/enlace.md").symlink_to(tmp_path / "README.md")
    with pytest.raises(ValueError, match="enlace"):
        recopilar(tmp_path)


def test_rechaza_credencial_sin_revelarla():
    secreto = "dato_secreto" + "_sintetico"
    with pytest.raises(ValueError) as e:
        verificar_contenidos({"README.md": secreto.encode()}, secreto)
    assert secreto not in str(e.value)


def test_rechaza_patron_clave_fuera_env():
    patron = "sk-" + "A"*40
    with pytest.raises(ValueError) as e:
        verificar_contenidos({"docs/error.txt": patron.encode()})
    assert patron not in str(e.value)
