import streamlit as st
from PIL import Image
import os
import json
import hashlib

# === 設定 ===
SCENE_FOLDER = "scenes"
MANUAL_FILE = "saved_manual.json"
os.makedirs(SCENE_FOLDER, exist_ok=True)

# === マニュアルデータの読み込みと保存 ===
def load_manual():
    if os.path.exists(MANUAL_FILE):
        with open(MANUAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_manual(data):
    with open(MANUAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# === ハッシュ生成：画像の内容から一意のIDを作る ===
def get_image_hash(image_bytes):
    return hashlib.md5(image_bytes).hexdigest()

# === シーン画像一覧 ===
def get_scene_images():
    return sorted([f for f in os.listdir(SCENE_FOLDER) if f.endswith(".png")])

# === アプリ開始 ===
st.set_page_config("半自動マニュアル生成システム", layout="wide")
st.title("📘 半自動マニュアル生成システム（重複排除版）")

# === 画像アップロードと重複判定 ===
uploaded = st.file_uploader("シーン画像をアップロード（重複画像は保存されません）", type=["png", "jpg", "jpeg"])
if uploaded:
    image_bytes = uploaded.getvalue()
    image_hash = get_image_hash(image_bytes)
    image_filename = f"{image_hash}.png"
    image_path = os.path.join(SCENE_FOLDER, image_filename)

    if os.path.exists(image_path):
        st.warning("⚠️ この画像はすでに登録されています。")
    else:
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        st.success("✅ 画像を保存しました。")

# === マニュアルデータ読み込み ===
manual_data = load_manual()

st.markdown("---")
st.subheader("🧩 ステップ編集・登録")

# === ステップごとに画像と説明を表示・登録 ===
for filename in get_scene_images():
    img_path = os.path.join(SCENE_FOLDER, filename)
    st.image(img_path, width=400, caption=filename)

    default_text = f"{filename} に基づいて生成された説明文です。"
    edited_text = st.text_area(f"説明文（編集可）：{filename}", value=default_text, key=filename)

    if st.button(f"このステップを登録", key="btn_"+filename):
        manual_data.append({"image": filename, "text": edited_text})
        save_manual(manual_data)
        st.success(f"{filename} をマニュアルに登録しました ✅")

st.markdown("---")
st.subheader("📑 登録済みマニュアルステップ")

if manual_data:
    for i, step in enumerate(manual_data, 1):
        st.markdown(f"### Step {i}")
        st.image(os.path.join(SCENE_FOLDER, step['image']), width=300)
        st.write(step['text'])
else:
    st.info("まだステップは登録されていません。")

if st.button("🗑️ 全ステップを初期化"):
    save_manual([])
    st.warning("マニュアルを初期化しました。")
