import base64
import html
import time

import streamlit as st

from chef_agent import ChefAgent, StampManager

try:
    from scavenger import Scavenger
except ImportError:
    Scavenger = None


st.set_page_config(
    page_title="600m Lab: Cyber-Gourmet",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_theme():
    """Give the lab a little atmosphere without depending on external assets."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #192944;
            --muted: #62718a;
            --paper: rgba(255, 255, 255, .84);
            --line: rgba(42, 72, 110, .14);
            --violet: #7258d8;
            --mint: #4fc3a7;
            --coral: #ff7866;
        }

        .stApp {
            background:
                radial-gradient(circle at 78% 7%, rgba(111, 93, 215, .17), transparent 22rem),
                radial-gradient(circle at 22% 77%, rgba(79, 195, 167, .14), transparent 26rem),
                linear-gradient(135deg, #f9fbff 0%, #f4f1ff 48%, #effaf7 100%);
            color: var(--ink);
        }
        [data-testid="stHeader"] { background: rgba(0, 0, 0, 0); }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #eef1f8, #e6f3ef);
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }
        [data-testid="stSidebar"] .stTextInput input,
        [data-testid="stSidebar"] .stTextArea textarea,
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: rgba(255,255,255,.82);
            border-radius: .75rem;
        }
        .block-container { max-width: 1280px; padding-top: 3.1rem; padding-bottom: 3rem; }
        h1, h2, h3 { color: var(--ink) !important; letter-spacing: -.025em; }
        .stButton > button {
            width: 100%; border: 0; border-radius: .8rem; padding: .65rem 1rem;
            color: white; font-weight: 700;
            background: linear-gradient(110deg, var(--violet), #8c66dc 55%, var(--coral));
            box-shadow: 0 8px 20px rgba(112, 88, 216, .26);
            transition: transform .18s ease, box-shadow .18s ease;
        }
        .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 24px rgba(112, 88, 216, .32); }
        .lab-kicker { color: var(--violet); font-size: .78rem; letter-spacing: .16em; font-weight: 800; }
        .hero-card {
            position: relative; overflow: hidden; min-height: 282px; padding: 2.25rem;
            border: 1px solid rgba(255,255,255,.85); border-radius: 1.45rem;
            background: var(--paper); box-shadow: 0 18px 45px rgba(55, 74, 109, .12);
        }
        .hero-card:after { content: "600m"; position: absolute; right: 1.4rem; bottom: -1.35rem;
            color: rgba(112, 88, 216, .10); font-size: 8rem; font-weight: 800; line-height: 1; }
        .hero-title { font-size: clamp(2rem, 4vw, 3.35rem); line-height: 1.08; font-weight: 780; margin: .5rem 0 .8rem; }
        .hero-copy { max-width: 39rem; color: var(--muted); font-size: 1.05rem; line-height: 1.75; }
        .signal { display: inline-flex; gap: .45rem; align-items: center; margin-top: 1.25rem;
            padding: .42rem .72rem; border-radius: 99px; background: rgba(79,195,167,.14); color: #237d6a; font-size: .84rem; font-weight: 700; }
        .signal-dot { height: .48rem; width: .48rem; border-radius: 50%; background: var(--mint); box-shadow: 0 0 0 .22rem rgba(79,195,167,.16); }
        .console-card { height: 100%; min-height: 282px; padding: 1.45rem; border-radius: 1.45rem;
            color: #e6edff; background: linear-gradient(150deg, #202746, #342c59); box-shadow: 0 18px 45px rgba(55, 50, 100, .22); }
        .console-top { color: #aeb7dc; font-size: .78rem; letter-spacing: .1em; }
        .console-line { display: flex; justify-content: space-between; padding: .85rem 0; border-bottom: 1px solid rgba(255,255,255,.12); }
        .console-line span:last-child { color: #7fe0c6; font-family: monospace; }
        .console-note { margin-top: 1.05rem; padding: .85rem; border-radius: .75rem; background: rgba(255,255,255,.08); color: #cbd3ee; font-size: .9rem; line-height: 1.55; }
        .section-label { margin: 2.2rem 0 .7rem; color: var(--muted); font-weight: 750; font-size: .84rem; letter-spacing: .08em; }
        .feature-card { min-height: 145px; padding: 1.2rem; border: 1px solid rgba(255,255,255,.8); border-radius: 1rem; background: rgba(255,255,255,.66); }
        .feature-card h4 { margin: .15rem 0 .45rem; color: var(--ink); }
        .feature-card p { margin: 0; color: var(--muted); font-size: .92rem; line-height: 1.6; }
        .paper-heading { margin: .7rem 0 .2rem; color: var(--ink); font-family: Georgia, serif; font-weight: 700; font-size: 1.15rem; text-align: center; }
        .paper-meta { margin-bottom: 1rem; color: var(--muted); font-size: .76rem; letter-spacing: .08em; text-align: center; }
        [data-testid="stVerticalBlockBorderWrapper"] { background: rgba(255,255,255,.74); border-color: rgba(42,72,110,.15); }
        code { border-radius: .65rem !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def paper_layout(title, content):
    """Render generated text as a readable report without injecting model HTML."""
    with st.container(border=True):
        st.markdown(f'<div class="paper-heading">{html.escape(title)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="paper-meta">600M LAB · EXPERIMENTAL REPORT · UNPEER-REVIEWED</div>', unsafe_allow_html=True)
        st.markdown(content)


def trigger_audio(file_path):
    with open(file_path, "rb") as audio_file:
        data = base64.b64encode(audio_file.read()).decode()
    st.components.v1.html(
        f'<audio autoplay="true"><source src="data:audio/mp3;base64,{data}" type="audio/mp3"></audio>',
        height=0,
    )


inject_theme()
emergency_zone = st.empty()

with st.sidebar:
    st.markdown("<div class='lab-kicker'>KITCHEN CONTROL PANEL</div>", unsafe_allow_html=True)
    st.header("🍴 厨房配置")
    keyword = st.text_input("输入今日的学术大变关键词", value="神经网络")
    user_style = st.selectbox("选择大变口味", ["经典学术原味", "古典哲学", "后现代主义", "火星文"])
    mode = st.radio("原材料来源", ["让 Scavenger 去外采", "首席执行官亲供"])
    manual_input = ""
    if mode == "首席执行官亲供":
        manual_input = st.text_area("投喂一段原材料", placeholder="可以是新闻、设定、半句梦话或任何可疑文本……", height=115)
    st.caption("三位 AI 主厨会各自端上一盘看似严谨、实则可疑的学术成果。")
    start_cooking = st.button("🔥 开始大变烹饪", type="primary")


if not start_cooking:
    hero, console = st.columns([1.35, 0.85], gap="large")
    with hero:
        st.markdown(
            """
            <section class="hero-card">
                <div class="lab-kicker">ALTITUDE 600M · REALITY ADJACENT</div>
                <div class="hero-title">把一个关键词<br>煮成一篇论文。</div>
                <p class="hero-copy">在现实之上六百米处，我们采集边角料、加入学术腔，并让三位主厨为同一个命题制造三种一本正经的胡说八道。</p>
                <div class="signal"><span class="signal-dot"></span>实验室待机中，锅已预热</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with console:
        st.markdown(
            """
            <section class="console-card">
                <div class="console-top">LIVE KITCHEN TELEMETRY</div>
                <div class="console-line"><span>现实锚点</span><span>STABLE-ish</span></div>
                <div class="console-line"><span>学术废料浓度</span><span>72.4%</span></div>
                <div class="console-line"><span>同行评议状态</span><span>AVOIDED</span></div>
                <div class="console-line"><span>本次可疑性</span><span>UNBOUNDED</span></div>
                <div class="console-note">← 在左侧投入关键词，选择口味，然后按下那枚不该按的按钮。</div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-label'>HOW THE QUESTIONABLE SCIENCE IS MADE</div>", unsafe_allow_html=True)
    guide_1, guide_2, guide_3 = st.columns(3, gap="medium")
    cards = [
        ("01 · 拾荒", "🕵️", "Scavenger 从公开网络带回一段看起来很像依据的原材料。"),
        ("02 · 变质", "🧂", "你选择调味：学院派、哲学派、后现代派，或者直接火星化。"),
        ("03 · 出餐", "🍽️", "三位主厨同时开工，附赠一个完全不可信但很有气势的 NI 指数。"),
    ]
    for column, (heading, icon, copy) in zip([guide_1, guide_2, guide_3], cards):
        with column:
            st.markdown(f"<section class='feature-card'><div>{icon}</div><h4>{heading}</h4><p>{copy}</p></section>", unsafe_allow_html=True)

else:
    if not keyword.strip():
        st.error("🚨 首席执行官，还没输入关键词呢，大厨没法开火！")
        st.stop()

    safe_keyword = html.escape(keyword)
    st.markdown("<div class='lab-kicker'>BATCH RUNNING · PLEASE KEEP HANDS OUT OF THE DIMENSIONAL OVEN</div>", unsafe_allow_html=True)
    st.title(f"🍳 正在烹饪：{safe_keyword}")
    st.caption(f"风味：{user_style} · 原料：{mode} · 三位主厨已收到同一份危险订单。")

    with st.spinner("🕵️ Scavenger 正在高维废墟中搜寻素材..."):
        if mode == "让 Scavenger 去外采":
            if Scavenger is None:
                st.error("🚨 Scavenger 正在外勤中（找不到文件），请检查现实锚点！")
                st.stop()
            raw_material = Scavenger().scrap_academic_bits(keyword)
        else:
            raw_material = manual_input.strip() or "空素材：首席执行官沉默地递来了一只空盘子。"

    st.markdown("<div class='section-label'>THREE INDEPENDENTLY QUESTIONABLE REPORTS</div>", unsafe_allow_html=True)
    chefs = [
        ("🤖 智谱大厨 (GLM)", "zhipu", "正在进行学术黑话降维..."),
        ("🐋 DeepSeek 大厨", "deepseek", "正在注入赛博熵增代码..."),
        ("🌌 Gemini 维度主厨", "gemini", "正在撕裂现实维度..."),
    ]
    results = {}
    for column, (name, provider, status_text) in zip(st.columns(3, gap="medium"), chefs):
        with column:
            st.subheader(name)
            with st.status(status_text, expanded=True):
                result = ChefAgent(provider=provider).cook(keyword, user_style, raw_material)
                ni_score = StampManager.calculate_ni(result, provider)
                paper_layout("本次实验报告", result)
                st.markdown(StampManager.get_stamp(ni_score))
                results[provider] = ni_score

    if results.get("gemini", 0) > 90:
        emergency_zone.error("🚨 检测到维度坍缩！正在启动紧急避险协议...")
        trigger_audio("tom_scream.mp3")
        for _ in range(3):
            st.toast("维度防御已离线！", icon="⚠️")
        time.sleep(2)
        emergency_zone.empty()
        st.markdown(
            """<style>.stApp { animation: lab-alert .12s linear 12; } @keyframes lab-alert {
            0%, 100% { filter: none; } 50% { filter: sepia(.4) saturate(2.5) hue-rotate(315deg); }
            }</style>""",
            unsafe_allow_html=True,
        )
