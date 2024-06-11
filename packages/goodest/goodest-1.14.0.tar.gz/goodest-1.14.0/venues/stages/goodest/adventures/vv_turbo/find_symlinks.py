import os

def find_symlinks(folder):
    symlinks = []
    for root, dirs, files in os.walk(folder):
        for name in files + dirs:
            path = os.path.join(root, name)
            if os.path.islink(path):
                symlinks.append(path)
    return symlinks

# Example usage
folder_path = "/media/venue/water/outlets/GL/status600/treasures/goodest.1/venues/stages/goodest/adventures/vv_turbo"
symlinks = find_symlinks(folder_path)
print("Symlinks in folder:")
for symlink in symlinks:
    print(symlink)
