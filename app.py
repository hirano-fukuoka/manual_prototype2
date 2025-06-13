import streamlit as st
from PIL import Image
import os
import json
import uuid

# 保存フォルダとファイル
SCENE_FOLDER = "scenes"
MANUAL_FILE = "saved_manual.json"
os.makedirs(SCENE_FOLDER, exist_ok=True)

# マニュアルデータの読み込み/保存
def load_manual():
    if os.path.exists(MANUAL_FILE):
        with open(MANUAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_manual(data):
    with open(MANUAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# デモ用：自動説明文を模擬生成（本来はBLIP2 + ChatGPT）
def mock_ai_generate_description(image_name):
    return f"{image_name} に基づいて生成された説明文です。"

# Streamlit UI
st.set_page_config("半自動マニュアル生成システム", layout="wide")
st.title("📘 半自動マニュアル生成システム（プロトタイプ）")

# アップロードされた画像を保存（本来は動画分割による抽出）
uploaded = st.file_uploader("シーン画像（1枚ずつ）をアップロード", type=["png", "jpg", "jpeg"])
if uploaded:
    image_id = str(uuid.uuid4())[:8]
    image_path = os.path.join(SCENE_FOLDER, f"{image_id}.png")
    with open(image_path, "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("画像を保存しました ✅")

# 編集モード
manual_data = load_manual()
st.markdown("---")
st.subheader("🧩 ステップ編集・登録")

scene_images = [f for f in os.listdir(SCENE_FOLDER) if f.endswith(".png")]

for filename in sorted(scene_images):
    st.image(os.path.join(SCENE_FOLDER, filename), width=400, caption=filename)
    default_text = mock_ai_generate_description(filename)
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
