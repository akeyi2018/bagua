import tkinter as tk
import random
# 外部ファイル iching_data.py から 64卦データを読み込む
try:
    from iching_data import HEXAGRAM_DATA
except ImportError:
    # データファイルがない場合のエラーハンドリング
    HEXAGRAM_DATA = {}

class IchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("本格易占い - 運勢鑑定版")
        self.root.geometry("500x800")
        self.root.configure(bg="#1a1a2e") # 深みのあるダークブルー

        # 八卦（小成卦）の定義
        self.trigrams = {
            (1, 1, 1): "天", (0, 0, 0): "地", (1, 0, 0): "雷", (0, 1, 1): "風",
            (0, 1, 0): "水", (1, 0, 1): "火", (0, 0, 1): "山", (1, 1, 0): "澤"
        }
        
        self.hexagrams = HEXAGRAM_DATA

        # --- UI レイアウト ---
        # タイトル
        self.label_title = tk.Label(
            root, text="★ 易経・六十四卦 鑑定 ★", 
            font=("MS Gothic", 20, "bold"), bg="#1a1a2e", fg="#00d2ff"
        )
        self.label_title.pack(pady=15)

        # 卦（棒）の描画エリア
        self.canvas = tk.Canvas(
            root, width=220, height=180, bg="#1a1a2e", highlightthickness=0
        )
        self.canvas.pack(pady=5)

        # 卦名
        self.label_name = tk.Label(
            root, text="", font=("MS Gothic", 22, "bold"), 
            bg="#1a1a2e", fg="#ffd700"
        )
        self.label_name.pack(pady=5)

        # 卦辞（伝統的な一文）
        self.label_kaji = tk.Label(
            root, text="", font=("MS Gothic", 12, "italic"), 
            bg="#1a1a2e", fg="#a0e4cb", wraplength=400
        )
        self.label_kaji.pack(pady=5)

        # --- 各運勢の表示エリア ---
        # 全体運（強調表示）
        self.label_un = tk.Label(
            root, text="心を落ち着けて「得卦」を押してください", 
            font=("MS Gothic", 12, "bold"), bg="#1a1a2e", fg="#ffffff", 
            wraplength=400, justify="center"
        )
        self.label_un.pack(pady=15)

        # 結婚運
        self.label_love = tk.Label(
            root, text="", font=("MS Gothic", 11), 
            bg="#1a1a2e", fg="#ff9ff3", wraplength=400
        )
        self.label_love.pack(pady=5)

        # 財運
        self.label_money = tk.Label(
            root, text="", font=("MS Gothic", 11), 
            bg="#1a1a2e", fg="#feca57", wraplength=400
        )
        self.label_money.pack(pady=5)

        # 実行ボタン
        self.btn_draw = tk.Button(
            root, text="得 卦", command=self.perform_divination, 
            font=("MS Gothic", 16, "bold"), bg="#ff4b2b", fg="white", 
            activebackground="#ff416c", cursor="hand2", padx=60, pady=10
        )
        self.btn_draw.pack(side="bottom", pady=30)

    def draw_line(self, y_pos, is_yang):
        """陰陽の棒を描画する"""
        color = "#00d2ff" if is_yang else "#ff4b2b"
        if is_yang:
            self.canvas.create_rectangle(40, y_pos, 180, y_pos+15, fill=color, outline="")
        else:
            self.canvas.create_rectangle(40, y_pos, 100, y_pos+15, fill=color, outline="")
            self.canvas.create_rectangle(120, y_pos, 180, y_pos+15, fill=color, outline="")

    def perform_divination(self):
        """占い実行"""
        if not self.hexagrams:
            self.label_un.config(text="エラー: iching_data.py が見つかりません。")
            return

        self.canvas.delete("all")
        lines = []
        
        # 下から上へ生成
        for i in range(6):
            res = random.choice([0, 1])
            lines.append(res)
            y_pos = 150 - (i * 25)
            self.draw_line(y_pos, res == 1)

        # 内卦と外卦の判定
        inner_tuple = tuple(lines[0:3])
        outer_tuple = tuple(lines[3:6])
        inner_name = self.trigrams.get(inner_tuple)
        outer_name = self.trigrams.get(outer_tuple)
        
        # データ取得
        result = self.hexagrams.get((outer_name, inner_name))
        
        if result:
            self.label_name.config(text=result["name"])
            self.label_kaji.config(text=result.get("kaji", ""))
            self.label_un.config(text=result.get("un", ""))
            
            # 結婚運と財運のテキストを更新
            love_text = f"【結婚運】 {result.get('love', '')}" if result.get('love') else ""
            money_text = f"【財運】 {result.get('money', '')}" if result.get('money') else ""
            
            self.label_love.config(text=love_text)
            self.label_money.config(text=money_text)
        else:
            self.label_name.config(text="不明な卦")
            self.label_un.config(text="組み合わせが見つかりませんでした。")

if __name__ == "__main__":
    root = tk.Tk()
    app = IchingApp(root)
    root.mainloop()