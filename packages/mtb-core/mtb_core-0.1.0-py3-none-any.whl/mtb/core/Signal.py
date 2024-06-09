import sys


class MtbImportHook:
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("mtb."):
            raise ImportError(f"Cannot import {fullname} bro...")
        return None


if __name__ == "__main__":
    sys.meta_path.insert(0, MtbImportHook())

    import mtb.prout
