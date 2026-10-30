import os
import tomli as toml


def extract_dependencies_requirements(path: str) -> list[str]:
    deps: list[str] = []
    if not os.path.exists(path):
        return deps
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name = line.split("=")[0].split(">")[0].split("<")[0].strip()
            deps.append(name)
    return deps


def extract_pyproject_dependencies(path: str) -> list[str]:
    deps: list[str] = []
    if not os.path.exists(path) or toml is None:
        return deps

    with open(path, "rb") as f:
        data = toml.load(f)

        if "project" in data and "dependencies" in data["project"]:
            for dep in data["project"]["dependencies"]:
                name = dep.split("=")[0].split(">")[0].split("<")[0].strip()
                deps.append(name)
    return deps


def run_lab_experiment() -> None:
    req_path = os.path.join("ex0", "requirements.txt")
    toml_path = os.path.join("ex0", "pyproject.toml")

    deps_req = extract_dependencies_requirements(req_path)
    deps_toml = extract_pyproject_dependencies(toml_path)

    all_dependencies = sorted(list(set(deps_req + deps_toml)))

    print("REAGENT STATUS: Loading reagents...")
    print("Checking dependencies:\n")

    use_reagents = True
    missing_libs: list[str] = []

    for lib in all_dependencies:
        try:
            module = __import__(lib)
            version = getattr(module, "__version__", "unknown")

            desc = "Data manipulation ready" if lib == "pandas" \
                else "Numerical computation ready" \
                if lib == "numpy" else "Ready"
            print(f"[OK] {lib} ({version}) - {desc}")
        except ImportError:
            print(f"[FAIL] {lib} - REAGENT ABSENT")
            use_reagents = False
            missing_libs.append(lib)

    if missing_libs:
        libs_str = " ".join(missing_libs)
        print("\n💡 HELPFUL MESSAGE - HOW TO INSTALL MISSING REAGENTS:")
        print(f"  Using pip:    pip install {libs_str}")
        print(f"  Using Poetry: poetry add {libs_str}\n")

    comparative_report = f"""\npip vs Poetry:
requirements.txt declares what to install; pip resolves it at install time.
pyproject.toml declares the same constraints, and Poetry pins the resolved
versions in poetry.lock so every install is identical.
{
    "All reagents present and accounted for."
    if use_reagents else "WARNING: Missing reagents in the environment!"
}"""

    print(comparative_report)


if __name__ == "__main__":
    run_lab_experiment()
