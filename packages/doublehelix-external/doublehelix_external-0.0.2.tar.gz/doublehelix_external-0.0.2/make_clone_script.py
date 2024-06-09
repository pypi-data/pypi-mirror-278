import sys

import requests


def print_clone_script(tag:str):
    last_slash = tag.rfind("/")
    if last_slash != -1:
        tag = tag[last_slash+1::]
    ROOT_URL = "https://api.github.com/repos/DoubleHelixApp/External/releases/tags/"

    dependencies = {
        "htslib": "git clone --depth 1 --recurse-submodules --branch {version} https://github.com/samtools/htslib",
        "samtools": "git clone --depth 1 --recurse-submodules --branch {version} https://github.com/samtools/samtools",
        "bcftools": "git clone --depth 1 --recurse-submodules --branch {version} https://github.com/samtools/bcftools",
        "bwa": "git clone --depth 1 --recurse-submodules --branch {version} https://github.com/lh3/bwa",
        "minimap2": "git clone --depth 1 --recurse-submodules --branch {version} https://github.com/lh3/minimap2",
    }

    r = requests.get(ROOT_URL + tag)
    r.raise_for_status()
    body = r.json()["body"]
    commands = []
    for line in body.split("\n"):
        for dependency in dependencies:
            if not line.startswith(dependency):
                continue
            split = line.strip().split("|")
            if len(split) < 2:
                raise RuntimeError(f"Malformed body: {body}")
            version = split[1]
            command = dependencies[dependency]
            commands.append(command.format(version=version))
            break
    if len(commands) != len(dependencies):
        raise RuntimeError(f"Malformed body. Some dependencies were not found: {body}")
    print("\n".join(commands), file=sys.stderr)
    print("\n".join(commands))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise RuntimeError("Tag not specified")

    tag = sys.argv[1]
    print_clone_script(tag)
