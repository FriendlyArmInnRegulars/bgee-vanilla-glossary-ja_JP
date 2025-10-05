# Baldur's Gate: Enhanced Edition 日本語翻訳用語集

Baldur's Gate: Enhanced Edition (BG1EE/BG2EE) の公式日本語翻訳から抽出した翻訳用語集リポジトリです。

## プロジェクト概要

このリポジトリは、BG:EE の公式英語/日本語 TRA (translation) ファイルから、翻訳Mod制作に活用できる包括的な用語集を自動生成することを目的としています。

### 対象ゲーム

- **Baldur's Gate: Enhanced Edition (BG1EE)**: 34,000翻訳エントリ
- **Baldur's Gate II: Enhanced Edition (BG2EE)**: 128,424翻訳エントリ

合計: **162,424** 翻訳ペア

## ディレクトリ構成

```
bgee-vanilla-glossary-ja_JP/
├── README.md                    # このファイル
├── CLAUDE.md                    # Claude Code用ガイダンス
├── memo.md                      # プロジェクト計画メモ
│
├── source_tra/                  # 入力TRAファイル
│   ├── bg1ee/
│   │   ├── en_US/dialog.tra    # BG1EE英語
│   │   └── ja_JP/dialog.tra    # BG1EE日本語
│   └── bg2ee/
│       ├── en_US/dialog.tra    # BG2EE英語
│       └── ja_JP/dialog.tra    # BG2EE日本語
│
├── scripts/                     # 用語集生成スクリプト (実装予定)
│   ├── requirements.txt
│   ├── create_glossary.py
│   └── lib/
│       ├── tra_parser.py
│       ├── glossary_builder.py
│       ├── term_extractor.py
│       └── models.py
│
├── glossary.json                # 生成される用語集 (予定)
│
└── docs/                        # 設計ドキュメント
    ├── DESIGN_OVERVIEW.md       # システム設計概要
    ├── implementation_plan.md   # 実装計画
    └── glossary_structure.md    # データ構造仕様
```

## データ構造

生成される `glossary.json` の構造:

```json
{
  "metadata": {
    "version": "1.0",
    "generated_at": "2025-10-05T12:00:00Z",
    "source_games": ["bg1ee", "bg2ee"],
    "total_entries": 162424
  },
  "entries": [
    {
      "id": "bg1ee:1",
      "english": "Why hast thou disturbed me here?",
      "japanese": {
        "default": "何故に私の邪魔をしに来たのだ？",
        "male": null,
        "female": null
      },
      "metadata": {
        "game": "bg1ee",
        "tra_id": 1,
        "has_variables": false,
        "char_count_en": 32,
        "char_count_ja": 18
      }
    }
  ],
  "term_frequency": {
    "Gorion": {
      "count": 45,
      "translations": ["ゴライオン"],
      "entries": ["bg1ee:15", "bg1ee:112"]
    }
  }
}
```

### 性別バリアント対応

日本語翻訳では、プレイヤーキャラクターの性別により異なる訳文が存在します:

```json
{
  "id": "bg1ee:6",
  "english": "But I have done nothing wrong!",
  "japanese": {
    "default": null,
    "male": "しかし俺は何もやっちゃいない！",
    "female": "でも私は何もしていないわ！"
  }
}
```

## 現在のステータス

### ✅ 完了
- [x] TRAファイル収集 (BG1EE/BG2EE)
- [x] データ構造設計
- [x] システムアーキテクチャ設計
- [x] 実装計画策定

### 🚧 実装予定
- [ ] TRAパーサー実装
- [ ] 用語集ビルダー実装
- [ ] 用語抽出器実装
- [ ] メインスクリプト実装
- [ ] glossary.json生成

## 使用予定方法

```bash
# 環境準備
cd scripts
pip install -r requirements.txt

# 全ゲームの用語集生成
python create_glossary.py --games all --output ../glossary.json

# BG1EEのみ
python create_glossary.py --games bg1ee --output ../glossary_bg1ee.json

# 統計情報を含める
python create_glossary.py --games all --include-stats
```

## 用語集の活用方法

### 1. 翻訳Mod制作
- 固有名詞の統一表記確認
- 定型句の再利用
- 既存翻訳の参考

### 2. 翻訳支援ツール
- 機械翻訳の辞書データ
- Claude API等への用語集提供
- 翻訳メモリとして活用

### 3. 品質チェック
- 翻訳一貫性の確認
- 同一英語への複数訳検出
- 訳抜け・誤訳候補の発見

## TRAファイルフォーマット

Infinity Engineのゲームで使用される翻訳ファイル形式:

```
@0     = ~<NO TEXT>~
@1     = ~Why hast thou disturbed me here?~
@6     = ~しかし俺は何もやっちゃいない！~ ~でも私は何もしていないわ！~
```

- `@数字`: エントリID（英日で対応）
- `~...~`: テキスト（チルダで囲む）
- 日本語では `~男性形~ ~女性形~` の形式で性別バリアント

## 技術スタック

- **Python 3.8+**
- **標準ライブラリ**: json, re, pathlib, argparse
- **推奨ライブラリ**: tqdm (プログレスバー)

## ドキュメント

詳細な設計情報は [docs/](docs/) ディレクトリを参照:

- [DESIGN_OVERVIEW.md](docs/DESIGN_OVERVIEW.md) - システム全体設計
- [implementation_plan.md](docs/implementation_plan.md) - 実装詳細計画
- [glossary_structure.md](docs/glossary_structure.md) - データ構造仕様

## ライセンス

TBD (未定)

## 貢献

TBD (未定)

## 注意事項

- このプロジェクトは個人の翻訳Mod制作支援を目的としています
- 公式翻訳の著作権は Beamdog/Overhaul Games に帰属します
- 生成される用語集は研究・学習目的での使用を想定しています
