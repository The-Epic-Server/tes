import json
def save(savemap, file):
    with open(file, "w") as f:
        json.dump(savemap, f)
        print("Saved savemap to " + file)

def load(file):
    with open(file) as f:
        loadmap = json.load(f)
        print("Loaded " + file + " as loadmap")
        return loadmap