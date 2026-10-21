import os, sys, json, zipfile
from PIL import Image

CACHE_DIR = "/tmp/mc_models_cache/assets/minecraft"
TEXTURE_DIR = "/tmp/mc_textures"
MC_JAR = "/home/nightwind/.minecraftx/versions/1.21.8/1.21.8.jar"

def ensure_cache():
    if os.path.exists(os.path.join(CACHE_DIR, "models", "block")) and os.path.exists(TEXTURE_DIR):
        return
    if not os.path.exists(MC_JAR):
        return
    os.makedirs("/tmp/mc_models_cache", exist_ok=True)
    os.makedirs(TEXTURE_DIR, exist_ok=True)
    with zipfile.ZipFile(MC_JAR, 'r') as z:
        for name in z.namelist():
            if name.startswith('assets/minecraft/models/'):
                z.extract(name, "/tmp/mc_models_cache")
            elif name.startswith('assets/minecraft/textures/block/'):
                fname = os.path.basename(name)
                if fname.endswith('.png'):
                    with open(os.path.join(TEXTURE_DIR, fname), 'wb') as f:
                        f.write(z.read(name))

ensure_cache()

def clean_key(k):
    if not k:
        return ""
    if k.startswith("minecraft:"):
        k = k[len("minecraft:"):]
    return k

def resolve_model(model_name):
    clean_name = clean_key(model_name)
    if clean_name.startswith("block/"):
        clean_name = clean_name[len("block/"):]

    chain = []
    curr = clean_name
    while curr:
        p = os.path.join(CACHE_DIR, "models", "block", f"{curr}.json")
        if not os.path.exists(p):
            p = os.path.join(CACHE_DIR, "models", f"{curr}.json")
            if not os.path.exists(p):
                break
        with open(p) as f:
            data = json.load(f)
        chain.append(data)
        parent = data.get("parent")
        if parent:
            curr = clean_key(parent)
            if curr.startswith("block/"):
                curr = curr[len("block/"):]
        else:
            curr = None

    merged_textures = {}
    elements = None
    for d in reversed(chain):
        if "textures" in d:
            merged_textures.update(d["textures"])
        if "elements" in d:
            elements = d["elements"]

    def resolve_tex(t):
        visited = set()
        while t and t.startswith("#"):
            visited.add(t)
            var_name = t[1:]
            t = merged_textures.get(var_name)
            if t in visited:
                break
        if t:
            t = clean_key(t)
            if t.startswith("block/"):
                t = t[len("block/"):]
        return t

    final_elements = []
    if elements:
        for el in elements:
            el_copy = {
                "from": el["from"],
                "to": el["to"],
                "faces": {}
            }
            for face_name, face_data in el.get("faces", {}).items():
                tex_ref = face_data.get("texture")
                tex_resolved = resolve_tex(tex_ref)
                el_copy["faces"][face_name] = {
                    "texture": tex_resolved,
                    "uv": face_data.get("uv", [0, 0, 16, 16]),
                    "rotation": face_data.get("rotation", 0),
                    "cullface": face_data.get("cullface")
                }
            final_elements.append(el_copy)

    return final_elements

_tex_cache = {}
def get_texture_image(tex_name):
    if not tex_name:
        return Image.new("RGBA", (16, 16), (150, 150, 150, 255))
    if tex_name in _tex_cache:
        return _tex_cache[tex_name]
    p = os.path.join(TEXTURE_DIR, f"{tex_name}.png")
    if not os.path.exists(p):
        img = Image.new("RGBA", (16, 16), (200, 100, 200, 255))
    else:
        img = Image.open(p).convert("RGBA")
        if img.height > img.width: # animated texture, use top frame
            img = img.crop((0, 0, img.width, img.width))
    _tex_cache[tex_name] = img
    return img
