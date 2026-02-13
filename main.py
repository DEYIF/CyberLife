import requests
import json
import os

# ================= 配置区 =================
API_KEY = os.environ.get("STEAM_API_KEY")
STEAM_ID = os.environ.get("STEAM_ID")
# ==========================================

def fetch_and_generate():
    print("开始获取 Steam 数据...")
    # 调用 Steam API 获取拥有游戏列表，include_appinfo=1 是为了获取游戏名字
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}&include_appinfo=1&format=json"
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"获取失败，状态码: {response.status_code}")
        return

    data = response.json()
    games = data.get("response", {}).get("games", [])
    
    # 按照游戏总时长降序排序
    games.sort(key=lambda x: x.get("playtime_forever", 0), reverse=True)

    print(f"成功获取！你一共拥有 {len(games)} 款游戏。开始生成 HTML...")

    # 生成极其极简的 HTML 静态网页内容
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>我的游戏足迹</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; line-height: 1.6; }
            li { margin-bottom: 10px; }
            .hours { color: #666; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>🎮 我的 Steam 游戏记录</h1>
        <h2>玩得最多的前 10 款游戏：</h2>
        <ul>
    """

    # 只提取前 10 名
    for game in games[:10]:
        name = game.get("name", "未知游戏")
        # API 返回的时长单位是分钟，我们转换为小时
        playtime_hours = round(game.get("playtime_forever", 0) / 60, 1)
        
        # 如果时长大于0才显示
        if playtime_hours > 0:
            html_content += f"<li><strong>{name}</strong> <span class='hours'>({playtime_hours} 小时)</span></li>\n"

    html_content += """
        </ul>
        <p><small>自动更新于 GitHub Actions</small></p>
    </body>
    </html>
    """

    # 把生成的 HTML 写入到 index.html 文件中
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 网页生成完毕！请在当前目录下双击打开 index.html 查看。")

if __name__ == "__main__":
    fetch_and_generate()