import os
from openai import OpenAI
from dotenv import load_dotenv
# 如果你还没安装 zhipuai，等下记得在终端 pip install zhipuai
from zhipuai import ZhipuAI
import random
import pyttsx3
import streamlit as st

def entropy_glitch_visualizer(ni_score):
    """
    根据胡说八道指数(NI)生成认知污染图注
    """
    artifacts = ["拓扑触手", "逻辑空洞", "思维坍缩点", "像素级逻辑错误", "莫比乌斯环畸变"]
    glitch_chars = ["░", "▒", "▓", "█", "▞", "🧩", "👁️", "🌀", "⚠️"]
    
    # 生成一段看起来就很“坏”的乱码图示
    visual_noise = "".join(random.choice(glitch_chars) for _ in range(20))
    
    if ni_score > 85:
        return f"""
    {visual_noise}
    图 1.4: 【紧急屏蔽】高维观测下的{random.choice(artifacts)}
    [ 备注 ]：检测到观察者效应，图像已自动进入量子模糊状态，严禁三维生物试图复原。
        """
    return "图 1.1: 一个勉强符合三维物理定律的示意图（无害）。"

load_dotenv()

class ChefAgent:
    def __init__(self, provider="deepseek"):
        self.provider = provider
        
        if provider == "deepseek":
            self.client = OpenAI(
                api_key=st.secrets["DEEPSEEK_API_KEY"],
                base_url="https://api.deepseek.com"
            )
            self.model = "deepseek-chat"
        elif provider == "gemini":
            self.client = OpenAI(
                api_key=st.secrets["GEMINI_API_KEY"],
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            self.model = "gemini-2.5-flash-lite"
        elif provider == "zhipu":
            self.client = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])
            self.model = "glm-4" # 智谱的旗舰模型


    # chef_agent.py 中 ChefAgent 类的 cook 方法内部
    def cook(self, keyword, style, raw_material):
        # 定义调味包
        style_map = {
            "经典学术原味": "请使用极致的学术词汇，保持严谨的废话风格。",
            "古典哲学": "请模仿康德或黑格尔，句式极长，充满思辨色彩。",
            "后现代主义": "请解构一切意义，语义破碎且充满混乱的隐喻。",
            "火星文": "请将学术大变产物转换成火星文，例如：o弋尐~鮇*、瓖嵌dё砑鱂。"
        }
        
        # 这里的 prompt 我们可以结合用户选的 style 动态生成
        selected_flavor = style_map.get(style, "请保持专业的学术风格。")
        
        prompt = f"""
        你是一位在'600m高空实验室'工作的赛博厨师。
        现在的任务是将以下【原始素材】进行'学术大变'。
        
        【风格要求】：{selected_flavor}
        【关键词】：{keyword}
        【风格标签】：{style}
        【原始素材】：{raw_material}
        
        请输出一段充满学术黑话、一本正经胡说八道、且排版精美的文字。
        请务必根据【风格】的要求进行创作，如果是火星文，请彻底转化字形！
        """
        
        # ... 后面的 client.chat.completions.create 逻辑保持不变 ...
    
    

class StampManager:

    @staticmethod
    def play_mockery(ni_score):
        """
        实验室语音助手：根据 NI 指数发表锐评
        """
        engine = None  # 核心修复：先给它一个名分，防止 UnboundLocalError
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # 设置音速和音量
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)

            # 盲盒语音逻辑
            if ni_score < 30:
                # 切换到男声（通常是索引0）
                if len(voices) > 0:
                    engine.setProperty('voice', voices[0].id)
                msg = "呵。写得太像人话了。这种迷惑性行为已被收录入学术欺诈样本库。"
            elif ni_score > 90:
                # 维度崩塌：汤姆猫尖叫逻辑
                print(f"DEBUG: 当前 NI 分数 {ni_score}🚨 [实验室广播]：维度防御离线")
                # 这里直接 return，剩下的惊吓交给 app.py 里的 JS 逻辑
                return 
            else:
                # 默认女声（通常是索引1）
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
                msg = "这一堆垃圾处理得非常顺滑。垃圾桶表示很满意，并拒绝了你的访问请求。"
            
            engine.say(msg)
            engine.runAndWait()
            
        except Exception as e:
            print(f"语音系统由于维度干扰暂时离线: {e}")
        finally:
            if engine:
                engine.stop() # 优雅收尾
        
    
    @staticmethod
    def get_stamp(ni_score):
        """
        根据 NI 指数返回对应的视觉印章
        """
        # 在返回印章文字前，咱们偷偷触发一下语音
        StampManager.play_mockery(ni_score)
        
        if ni_score < 30:
            # A号章：虽然人话多，但因为太像人话所以更危险
            return """
> ```text
> ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
> ┃  🔴 PROHIBITED FOR CARBON-BASED     ┃
> ┃  ┃  【 A 号章：禁止碳基生物阅读 】  ┃
> ┃  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
> ```"""
        elif ni_score < 60:
            # B号章：平庸的极致
            return """
> ```text
> ┌─────────────────────────────────────┐
> │  ♻️ ACADEMIC WASTE RECYCLING         │
> │  │  【 B 号章：学术废品回收合格 】  │
> └─────────────────────────────────────┘
> ```"""
        elif ni_score < 85:
            # C号章：逻辑开始打结
            return """
> ```text
> 🌀 LOGIC SINGULARITY: DO NOT STARE   
> 【 C 号章：逻辑奇点：请勿直视 】     
> ```"""
        else:
            # D号章：维度崩塌（Gemini 专用）
            return """
> ```text
> ⚠️  DIMENSIONAL DEFENSE OFFLINE      
> █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
> █  【 D 号章：维度防御系统已离线 】  █
> █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
> ```"""

    @staticmethod
    def calculate_ni(text, provider):

        # --- 新加这一行保护逻辑 ---
        if text is None:
            return 10 # 如果没内容，给个保底的低分
        # -----------------------
        
        base_ni = len(text) % 100 # 现在的报错行
    
        """
        计算胡说八道指数 (NI)
        这里的逻辑我们可以玩点梗：Gemini 自动 +30，学术风自动 -20
        """
        base_ni = len(text) % 100 # 基础值
        if "gemini" in provider.lower():
            base_ni = min(99.9, base_ni + 40) # 维度主厨的加成
        elif "zhipu" in provider.lower():
            base_ni = max(10, base_ni - 20) # 智谱的矜持
        return base_ni


# --- 吵架测试 ---
if __name__ == "__main__":
    # 我们用 Scavenger 昨天捡回来的那段硬核素材
    raw_data = "神经网络是一种模仿动物神经系统特征的算法模型。1943年心理学家W.Mcculloch和数理逻辑学家W.Pitts建立了M-P模型。"
    
    print("🍳 [实验室广播]: 三厨对垒正式开始！\n")
    
    # --- 第一位：智谱大厨 (GLM) ---
    chef_zhipu = ChefAgent(provider="zhipu")
    result_zhipu = chef_zhipu.cook("神经网络", "严谨老学究风", raw_data)
    print("--- 👨‍🍳 智谱大厨 (GLM) 的作品 ---")
    ni_zhipu = StampManager.calculate_ni(result_zhipu, "zhipu")
    print(f"\n👨‍🍳 [ 智谱大厨 (GLM)评估报告 ] NI 指数: {ni_zhipu}%")
    print(StampManager.get_stamp(ni_zhipu))
    print(result_zhipu)
    print(entropy_glitch_visualizer(ni_zhipu)) # 

    
    print("\n" + "X"*60 + "\n") # 分界线

    # --- 第三位：维度主厨 (Gemini) ---
    # 既然我在你的 2026 年环境里，我们可以调用 Gemini 的 API
    chef_gemini = ChefAgent(provider="gemini") # 记得在你的适配器里处理这个 provider
    result_gemini = chef_gemini.cook("神经网络", "高维混乱克苏鲁风", raw_data)
    print("--- 🌌 维度主厨 (Gemini) 的作品 ---")
    # 示例：维度主厨 (Gemini) 的输出
    ni_gemini = StampManager.calculate_ni(result_gemini, "gemini")
    print(f"\n🌌 [ 维度主厨评估报告 ] NI 指数: {ni_gemini}%")
    print(StampManager.get_stamp(ni_gemini))
    print(result_gemini)
    print(entropy_glitch_visualizer(ni_gemini)) # 接上刚才那个坏图注

    print("\n" + "X"*60 + "\n") # 分界线

    # --- 第二位：DeepSeek大厨 ---
    chef_ds = ChefAgent(provider="deepseek")
    result_ds = chef_ds.cook("神经网络", "硬核赛博科幻风", raw_data)
    print("--- 🦾 DeepSeek 大厨 的作品 ---")
    ni_ds = StampManager.calculate_ni(result_ds, "deepseek")
    print(f"\n🦾 [ DeepSeek 大厨评估报告 ] NI 指数: {ni_ds}%")
    print(StampManager.get_stamp(ni_ds))
    print(result_ds)
    print(entropy_glitch_visualizer(ni_ds)) # 接上刚才那个坏图注


