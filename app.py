import streamlit as st
from chef_agent import ChefAgent, StampManager
import base64

# 挖一个空位，平时它什么都不显示
emergency_zone = st.empty()
# --- 输出格式排版 放在 app.py 顶部作为工具函数 ---
def paper_layout(title, content, stamp_code=""):
    st.markdown(f"""
    <div style="position: relative; border: 1px solid #ddd; padding: 20px;">
        <div style="position: absolute; top: 10px; right: 10px; font-family: monospace; color: red; opacity: 0.8;">
            {stamp_code}
        </div>
        <h3 style="text-align: center;">{title}</h3>
        <hr>
        <div style="text-align: justify;">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def trigger_audio(file_path):
    """
    这是一个魔法函数：它能把本地的 MP3 转换成网页能听懂的流，并强行播放
    """
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # 这一段 HTML/JS 就是咱们的“猫笼子”
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        # 在网页里偷偷塞进这个播放器
        st.components.v1.html(md, height=0)

        
# 导入咱们的外勤员工
try:
    from scavenger import Scavenger 
except ImportError:
    st.error("🚨 警告：Scavenger 正在外勤中（找不到文件），请检查现实锚点！")


# 1. 实验室视觉基调
st.set_page_config(page_title="600m Lab: Cyber-Gourmet", page_icon="🍳", layout="wide")

st.title("🧪 600m 实验室：Cyber-Gourmet Edition")
st.markdown("--- 在现实之上六百米处，烹饪学术的荒谬 ---")

# ... 页面配置 ...

with st.sidebar:
    st.header("🍴 厨房配置")
    keyword = st.text_input("输入今日的学术大变关键词", value="神经网络")

    # 插入我们的新调料
    user_style = st.selectbox(
        "选择大变口味：",
        ["经典学术原味", "古典哲学", "后现代主义", "火星文"]
    )
    
    # 增加一个开关：是自己输入，还是让 Scavenger 去抓？
    mode = st.radio("原材料来源", ["让 Scavenger 去外采", "首席执行官亲供"])
    start_cooking = st.button("🔥 开始大变烹饪")

    

if start_cooking:
    col1, col2, col3 = st.columns(3)
    
    if not keyword:
        st.error("🚨 首席执行官，还没输入关键词呢，大厨没法开火！")
        st.stop()

    # --- 阶段 1：Scavenger 采料 ---
    with st.spinner("🕵️ Scavenger 正在高维废墟中搜寻素材..."):
        if mode == "让 Scavenger 去外采":
            scavenger = Scavenger()
            # 假设你的 scavenger 有个抓取方法叫 fetch_data
            raw_material = scavenger.scrap_academic_bits(keyword) 
        else:
            raw_material = st.session_state.get("manual_input", "空素材")

    # --- 阶段 2：三厨对垒 ---
    # 接下来才是你刚才看到的 col1, col2, col3 的逻辑...
    # 这里的素材就会变成 Scavenger 辛苦抓回来的“学术边角料”了！
    with col1:
        st.subheader("🤖 智谱大厨 (GLM)")
        with st.status("正在进行学术黑话降维...", expanded=True):
            chef_glm = ChefAgent(provider="zhipu")
            res_glm = chef_glm.cook(keyword, user_style, raw_material)
            st.session_state['res_glm'] = res_glm # 必须存进 session_state！
            ni_glm = StampManager.calculate_ni(res_glm, "zhipu")
            # 这里的每一行 print 其实都会触发你代码里的 play_mockery TTS！            
            # 重点：在这里调用盘子（排版）
            # 把获取到的印章字符串直接传进去
            paper_layout("", res_glm)
            st.code(StampManager.get_stamp(ni_glm)) 
            

    with col2:
        st.subheader("🐋 DeepSeek大厨")
        with st.status("正在注入赛博熵增代码...", expanded=True):
            chef_ds = ChefAgent(provider="deepseek")
            res_ds = chef_ds.cook(keyword, user_style, raw_material)
            st.session_state['res_ds'] = res_ds # 必须存进 session_state！
            ni_ds = StampManager.calculate_ni(res_ds, "deepseek")            
            # 重点：在这里调用盘子（排版）
            # 把获取到的印章字符串直接传进去
            paper_layout("", res_ds)
            st.code(StampManager.get_stamp(ni_ds)) 
            

    with col3:
        st.subheader("🌌 Gemini 维度主厨")
        with st.status("正在撕裂现实维度...", expanded=True):
            chef_gem = ChefAgent(provider="gemini")
            res_gem = chef_gem.cook(keyword, user_style, raw_material)
            st.session_state['res_gem'] = res_gem # 必须存进 session_state！
            ni_gem = StampManager.calculate_ni(res_gem, "gemini")
            # 重点：在这里调用盘子（排版）
             # 把获取到的印章字符串直接传进去
            paper_layout("", res_gem)
            st.code(StampManager.get_stamp(ni_gem)) 
            
            # 这一行如果 NI 爆表，汤姆猫就会在后台“咣”地一声降临！
    


    # 检查是否有大厨的作品 NI 爆表了
    if ni_gem > 90:
        # 动态往刚才那个空位里塞进警告框
        emergency_zone.error("🚨 检测到维度坍缩！正在启动紧急避险协议...")
        
        # 汤姆猫音效依然触发
        trigger_audio("tom_scream.mp3")
        
        # 视觉震撼：连续弹出 toast
        for _ in range(3):
            st.toast("维度防御已离线！", icon="⚠️")

        # --- 关键：在这里加一个强制等待，给用户一点震撼时间 ---
        import time
        time.sleep(2) # 让警报持续 2 秒
        
        # 4. 恢复正常！
        emergency_zone.empty() 
        # 此时红光动画也应该播放完了（你设置的是 1.5秒），背景会自动回白

        st.markdown("""
            <style>
            .stApp {
                /* 初始背景设为白色 */
                background-color: white; 
                /* 运行 15 次，总计 1.5 秒 */
                animation: blinker 0.1s linear 15;
                /* 确保停在动画 100% 的状态 */
                animation-fill-mode: forwards;
            }

            @keyframes blinker {
                0% { background-color: white; }
                50% { background-color: #ff4b4b; }
                100% { background-color: white; } /* 强制终点回到白色 */
            }
            </style>
            """, unsafe_allow_html=True)
        
        # 强制等待一小会儿，然后利用 Streamlit 的 session_state 或直接刷新视觉
        # 这样用户就不需要一直盯着红光看了

            

    #st.balloons() # 庆祝三厨合体成功