import importlib
import logging
import os
import struct
import sys
from dataclasses import dataclass


PATH = os.path.dirname(__file__)
COMMON_PACKAGE_PATH = os.path.join(PATH, "package")
RUNTIME_ROOT = os.path.abspath(os.path.join(PATH, "..", "..", "runtime"))

PYTHON_VERSION_TO_YEAR = {
	(3, 11): 2025,
	(3, 13): 2026,
}

RUNTIME_MAP = {
	2024: {
		"runtime_dir": "py311-x86",
		"python_version": (3, 11),
		"bits": 32,
	},
	2025: {
		"runtime_dir": "py311-x86",
		"python_version": (3, 11),
		"bits": 32,
	},
	2026: {
		"runtime_dir": "py313-x64",
		"python_version": (3, 13),
		"bits": 64,
	},
}

try:
	from logHandler import log as _log
except Exception:
	_log = logging.getLogger(__name__)


class RuntimeSelectionError(RuntimeError):
	pass


@dataclass(frozen=True)
class RuntimeBundle:
	year: int
	runtime_dir: str
	python_version: tuple[int, int]
	bits: int
	python_path: str
	runtime_package_path: str
	common_package_path: str
	selection_source: str


def _detect_bits():
	return struct.calcsize("P") * 8


def _infer_version_year_from_python(python_version):
	inferred_year = PYTHON_VERSION_TO_YEAR.get(python_version)
	if inferred_year is not None:
		return inferred_year

	known_versions = sorted(PYTHON_VERSION_TO_YEAR)
	if python_version <= known_versions[0]:
		return PYTHON_VERSION_TO_YEAR[known_versions[0]]
	if python_version >= known_versions[-1]:
		return PYTHON_VERSION_TO_YEAR[known_versions[-1]]

	previous_version = known_versions[0]
	for known_version in known_versions[1:]:
		if python_version < known_version:
			return PYTHON_VERSION_TO_YEAR[previous_version]
		previous_version = known_version
	return PYTHON_VERSION_TO_YEAR[known_versions[-1]]


def _log_warning(message):
	if hasattr(_log, "warning"):
		_log.warning(message)
	else:
		_log.warning("%s", message)


def _log_error(message):
	if hasattr(_log, "error"):
		_log.error(message)
	else:
		_log.error("%s", message)


def _get_version_year():
	try:
		from buildVersion import version_year
	except Exception:
		version_year = None

	if version_year is not None:
		return int(version_year), "buildVersion"

	python_version = tuple(sys.version_info[:2])
	inferred_year = _infer_version_year_from_python(python_version)
	_log_warning(
		f"buildVersion.version_year unavailable; inferred Access8Math runtime year {inferred_year} "
		f"from Python {python_version[0]}.{python_version[1]}"
	)
	return inferred_year, "inferred"


def resolve_runtime_bundle(version_year=None):
	if version_year is None:
		version_year, selection_source = _get_version_year()
	else:
		version_year = int(version_year)
		selection_source = "explicit"

	runtime = RUNTIME_MAP.get(version_year)
	if runtime is None:
		raise RuntimeSelectionError(f"Unsupported Access8Math runtime year: {version_year}")

	runtime_dir = str(runtime["runtime_dir"])
	python_path = os.path.join(RUNTIME_ROOT, runtime_dir, "python")
	runtime_package_path = os.path.join(RUNTIME_ROOT, runtime_dir, "package")
	for path in (python_path, runtime_package_path, COMMON_PACKAGE_PATH):
		if not os.path.isdir(path):
			raise RuntimeSelectionError(f"Missing Access8Math runtime path: {path}")

	return RuntimeBundle(
		year=version_year,
		runtime_dir=runtime_dir,
		python_version=runtime["python_version"],
		bits=runtime["bits"],
		python_path=python_path,
		runtime_package_path=runtime_package_path,
		common_package_path=COMMON_PACKAGE_PATH,
		selection_source=selection_source,
	)


def validate_runtime_bundle(bundle, python_version=None, bits=None):
	python_version = tuple(python_version or sys.version_info[:2])
	bits = bits if bits is not None else _detect_bits()
	if python_version != bundle.python_version or bits != bundle.bits:
		raise RuntimeSelectionError(
			"Access8Math runtime bundle mismatch: "
			f"year={bundle.year} expects Python {bundle.python_version[0]}.{bundle.python_version[1]} "
			f"{bundle.bits}-bit, got Python {python_version[0]}.{python_version[1]} {bits}-bit"
		)


def _insert_sys_path(path):
	if path in sys.path:
		sys.path.remove(path)
	sys.path.insert(0, path)


def _clear_module_family(package_name):
	prefix = f"{package_name}."
	for module_name in list(sys.modules):
		if module_name == package_name or module_name.startswith(prefix):
			sys.modules.pop(module_name, None)


def _preload_embedded_xml():
	_clear_module_family("xml")
	importlib.invalidate_caches()
	importlib.import_module("xml")
	importlib.import_module("xml.etree")


def configure_runtime(version_year=None, python_version=None, bits=None):
	bundle = resolve_runtime_bundle(version_year=version_year)
	if bundle.selection_source == "buildVersion":
		validate_runtime_bundle(bundle, python_version=python_version, bits=bits)
	else:
		python_version = tuple(python_version or sys.version_info[:2])
		bits = bits if bits is not None else _detect_bits()
		if python_version != bundle.python_version or bits != bundle.bits:
			_log_warning(
				"Access8Math runtime validation skipped outside NVDA buildVersion context: "
				f"selected year={bundle.year}, runtime Python {python_version[0]}.{python_version[1]} {bits}-bit"
			)

	for path in (bundle.common_package_path, bundle.runtime_package_path, bundle.python_path):
		_insert_sys_path(path)

	_preload_embedded_xml()
	return bundle
