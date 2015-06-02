import os
import yaml


PATH_DEFINITIONS = 'paths.yaml'
TARGET_DIRECTORY = os.path.expanduser("~/")


def load_paths(filename):
    with open(filename) as f:
        paths = yaml.safe_load(f)
    assert isinstance(paths, list)
    assert all(isinstance(path, str) for path in paths)
    assert all(os.path.exists(path[1:]) for path in paths)
    return paths


def clobber_tree(src, dst):
    if os.path.isdir(src):
        if not os.path.isdir(dst):
            os.makedirs(dst)

        for name in os.listdir(src):
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            clobber_tree(srcname, dstname)

    else:
        assert os.path.exists(os.path.dirname(dst))
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                buffer = fsrc.read(1024 * 1024)
                if not buffer:
                    break
                fdst.write(buffer)


def main():
    paths = load_paths(PATH_DEFINITIONS)
    for path in paths:
        clobber_tree(path[1:], os.path.join(TARGET_DIRECTORY, path))


if __name__ == "__main__":
    main()
