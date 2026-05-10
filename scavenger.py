import requests
from bs4 import BeautifulSoup

class Scavenger:
    def __init__(self):
        # 我们用百度百科作为国内最稳的原材料库
        self.base_url = "https://baike.baidu.com/item/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrap_academic_bits(self, keyword):
        """去百度百科抓取一些看起来很硬核的段落"""
        try:
            response = requests.get(self.base_url + keyword, headers=self.headers, timeout=5)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 抓取词条开头的摘要部分（通常这部分废话最专业）
            summary = soup.find('meta', {'name': 'description'})
            if summary:
                return summary['content']
            return f"未能找到关于 {keyword} 的正经描述，看来此物已超脱三界之外。"
        except Exception as e:
            return f"拾荒途中遇到阻碍：{str(e)}"



# 测试一下
if __name__ == "__main__":
    bot = Scavenger()
    print(bot.scrap_academic_bits("神经网络"))


try:
    import requests
except ModuleNotFoundError:
    print("""
    🚨 [ 600m 实验室：紧急避险协议启动 ]
    
    检测到现实锚点丢失：模块 'requests' 已被高维存在抹除。
    当前的逻辑流无法在缺乏该依赖的情况下维持三维投影。
    
    [ 修复指南 ]：
    请在终端执行 'pip install requests' 以重新锚定现实。
    否则，实验室将在 3 秒后陷入逻辑虚无...
    """)
    exit(1)