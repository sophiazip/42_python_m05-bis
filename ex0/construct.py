import importlib
import os


def _clean_dep_name(raw: str) -> str:
    raw = raw.split("#")[0].split(";")[0].split("[")[0]
    for sep in ("=", ">", "<", "~", "!", "^"):
        raw = raw.split(sep)[0]
    return raw.strip().strip('"').strip("'")


def extract_dependencies_requirements(path: str) -> list[str]:
    deps: list[str] = []
    if not os.path.exists(path):
        return deps
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name = _clean_dep_name(line)
            if name:
                deps.append(name)
    return deps


def extract_pyproject_dependencies(path: str) -> list[str]:
    deps: list[str] = []
    if not os.path.exists(path):
        return deps

    current_section = ""
    in_deps_list = False

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.split("#")[0].strip()
            if not line:
                continue

            if (
                line.startswith("[")
                and line.endswith("]")
                and not in_deps_list
            ):
                current_section = line[1:-1].strip()
                continue

            if current_section == "project":
                if not in_deps_list and line.startswith("dependencies"):
                    _, _, rest = line.partition("=")
                    rest = rest.strip()
                    if rest.startswith("["):
                        in_deps_list = True
                        rest = rest[1:]
                        if "]" in rest:
                            items_part = rest.split("]")[0]
                            in_deps_list = False
                        else:
                            items_part = rest
                        for item in items_part.split(","):
                            name = _clean_dep_name(item)
                            if name:
                                deps.append(name)
                elif in_deps_list:
                    if "]" in line:
                        items_part = line.split("]")[0]
                        in_deps_list = False
                    else:
                        items_part = line
                    for item in items_part.split(","):
                        name = _clean_dep_name(item)
                        if name:
                            deps.append(name)

            elif current_section == "tool.poetry.dependencies":
                if "=" in line:
                    pkg = line.split("=", 1)[0].strip().strip('"').strip("'")
                    if pkg and pkg.lower() != "python":
                        deps.append(pkg)

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
            module = importlib.import_module(lib)
            version = getattr(module, "__version__", "unknown")

            desc = (
                "Data manipulation ready"
                if lib == "pandas"
                else "Numerical computation ready"
                if lib == "numpy"
                else "Ready"
            )
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

    status_msg = (
        "All reagents present and accounted for."
        if use_reagents
        else "WARNING: Missing reagents in the environment!"
    )

    comparative_report = f"""\npip vs Poetry:
    requirements.txt declares what to install; pip resolves it at install time.
    pyproject.toml declares the same constraints, and Poetry pins the resolved
    versions in poetry.lock so every install is identical.
    {status_msg}"""

    print(comparative_report)


if __name__ == "__main__":
    run_lab_experiment()
