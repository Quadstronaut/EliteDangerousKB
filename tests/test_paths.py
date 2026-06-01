# tests/test_paths.py
import tomllib
from pathlib import Path
import pytest


def test_repo_root_is_path():
    from copilot.paths import repo_root
    root = repo_root()
    assert isinstance(root, Path)
    assert root.exists(), f"repo_root() returned non-existent path: {root}"


def test_repo_root_contains_config_toml():
    from copilot.paths import repo_root
    assert (repo_root() / "config.toml").exists(), "config.toml not found at repo root"


def test_load_config_returns_dict():
    from copilot.paths import load_config
    cfg = load_config()
    assert isinstance(cfg, dict)


def test_load_config_has_required_sections():
    from copilot.paths import load_config
    cfg = load_config()
    for section in ("ollama", "retrieval", "copilot", "paths", "loop"):
        assert section in cfg, f"Missing config section: [{section}]"


def test_load_config_ollama_values():
    from copilot.paths import load_config
    ollama = load_config()["ollama"]
    assert ollama["base_url"] == "http://localhost:11434"
    assert ollama["chat_model"] == "qwen3:8b"
    assert ollama["embed_model"] == "bge-m3"
    assert ollama["vision_model"] == "qwen3-vl:8b"
    assert ollama["loop_model"] == "qwen3-coder:30b"


def test_kb_dir_is_subdir_of_root():
    from copilot.paths import repo_root, kb_dir
    root = repo_root()
    kb = kb_dir()
    assert isinstance(kb, Path)
    # kb_dir() must be relative to repo root (not some absolute elsewhere)
    assert str(kb).startswith(str(root))


def test_embeddings_dir_exists():
    from copilot.paths import embeddings_dir
    d = embeddings_dir()
    assert isinstance(d, Path)
    assert d.exists(), f"embeddings_dir() returned non-existent path: {d}"


def test_indexes_dir_exists():
    from copilot.paths import indexes_dir
    d = indexes_dir()
    assert isinstance(d, Path)
    assert d.exists(), f"indexes_dir() returned non-existent path: {d}"


def test_paths_consistent_with_config():
    """kb_dir, embeddings_dir, indexes_dir must match config.toml [paths]."""
    from copilot.paths import repo_root, load_config, kb_dir, embeddings_dir, indexes_dir
    cfg_paths = load_config()["paths"]
    root = repo_root()
    assert kb_dir() == root / cfg_paths["kb"]
    assert embeddings_dir() == root / cfg_paths["embeddings"]
    assert indexes_dir() == root / cfg_paths["indexes"]
