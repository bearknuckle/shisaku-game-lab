# 試作ゲームラボ

試作ゲームを、ブラウザですぐ遊べるサイトです。

- 公開サイト：https://game-lab-oj9t.onrender.com/
- カテゴリ：株・音楽・お酒・こども・ボドゲ のゲーム

## 構成

```text
shisaku-game-lab/
├── lab/            # 公開されるサイト（Render の静的サイト game-lab）
│   ├── index.html  # ホーム画面（ゲーム一覧 GAMES・カテゴリ CATS・更新情報 UPDATES）
│   └── <ゲームID>/index.html  # 各ゲーム（1ファイル完結）
├── lab-api/        # 遊んだ回数カウンター（Render の Web サービス game-lab-api）
├── tools/          # リンクプレビュー画像などを作るスクリプト
└── docs/           # 資料
```

作業のルールは `CLAUDE.md` にまとめています。

## これまでの経緯

2026-11-26 に `bearknuckle/boardgame-tutorial` の `lab` ブランチから、変更履歴ごと移しました。
`baron-nimmt/` や `app.py` などは、そのときの残りです。
