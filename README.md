# Baldur's Gate: Enhanced Edition 日本語翻訳用語集

Baldur's Gate: Enhanced Edition (BG1EE/BG2EE) の公式日本語翻訳から抽出した翻訳用語集リポジトリです。

## プロジェクト概要

このリポジトリは、BG:EE の公式英語/日本語 TRA (translation) ファイルから、翻訳Mod制作に活用できる包括的な用語集を自動生成するシステムです。

### 対象ゲーム

- **Baldur's Gate: Enhanced Edition (BG1EE)**: 24,547エントリ
- **Baldur's Gate II: Enhanced Edition (BG2EE)**: 80,311エントリ

合計: **104,858** 翻訳ペア（性別バリアント込み）

## 主な機能

✅ **完全自動化**: TRAファイルから用語集JSONを自動生成
✅ **性別バリアント対応**: 日本語の男性形/女性形を完全サポート
✅ **用語抽出**: 固有名詞・頻出フレーズを自動抽出（8,766語）
✅ **メタデータ**: 変数タグ・文字数等の詳細情報
✅ **統計情報**: ゲーム別の詳細統計

## ディレクトリ構成

```
bgee-vanilla-glossary-ja_JP/
├── README.md                    # このファイル
├── CLAUDE.md                    # Claude Code用ガイダンス
├── .gitignore                   # Git除外設定
│
├── source_tra/                  # 入力TRAファイル
│   ├── bg1ee/
│   │   ├── en_US/dialog.tra    # BG1EE英語 (34,000エントリ)
│   │   └── ja_JP/dialog.tra    # BG1EE日本語 (34,000エントリ)
│   └── bg2ee/
│       ├── en_US/dialog.tra    # BG2EE英語 (128,424エントリ)
│       └── ja_JP/dialog.tra    # BG2EE日本語 (128,424エントリ)
│
├── scripts/                     # 用語集生成スクリプト
│   ├── requirements.txt         # Python依存関係
│   ├── create_glossary.py       # メインスクリプト
│   └── lib/
│       ├── models.py            # データモデル定義
│       ├── tra_parser.py        # TRAファイルパーサー
│       ├── glossary_builder.py  # 用語集ビルダー
│       └── term_extractor.py    # 用語抽出エンジン
│
├── glossary.json                # 生成された用語集 (76.69 MB)
│
└── docs/                        # 設計ドキュメント
    ├── DESIGN_OVERVIEW.md       # システム設計概要
    ├── implementation_plan.md   # 実装詳細計画
    └── glossary_structure.md    # データ構造仕様
```

## 使用方法

### 環境準備

```bash
cd scripts
pip install -r requirements.txt  # tqdm のみ（オプション）
```

### 用語集生成

```bash
# 全ゲームの用語集生成（用語抽出付き）
python3 create_glossary.py --games all --extract-terms --include-stats

# BG1EEのみ
python3 create_glossary.py --games bg1ee --extract-terms

# 用語抽出なし（高速生成）
python3 create_glossary.py --games all --output ../glossary.json

# カスタム出力
python3 create_glossary.py --games bg2ee --output custom.json --indent 4
```

### コマンドラインオプション

```
--games {bg1ee,bg2ee,all}    処理するゲーム (デフォルト: all)
--output PATH                出力ファイルパス (デフォルト: ../glossary.json)
--extract-terms              用語抽出を有効化
--include-stats              詳細統計情報を含める
--indent N                   JSONインデント (デフォルト: 2)
```

## データ構造

### 用語集エントリ例

```json
{
  "id": "bg1ee:6",
  "english": "But I have done nothing wrong!",
  "japanese": {
    "default": null,
    "male": "しかし俺は何もやっちゃいない！",
    "female": "でも私は何もしていないわ！"
  },
  "metadata": {
    "game": "bg1ee",
    "tra_id": 6,
    "has_variables": false,
    "has_sound_ref": false,
    "char_count_en": 71,
    "char_count_ja": 28
  }
}
```

### 用語頻度インデックス例

```json
{
  "term_frequency": {
    "Iron Throne": {
      "count": 338,
      "translations": ["アイアンスロウン"],
      "entries": ["bg1ee:5", "bg1ee:20", "..."]
    },
    "Sarevok": {
      "count": 251,
      "translations": ["サレヴォク"],
      "entries": ["bg1ee:251", "bg2ee:1234", "..."]
    }
  }
}
```

## 生成された用語集の統計

### エントリ数
- **BG1EE**: 24,547エントリ
  - 性別バリアント: 6,200 (25.3%)
- **BG2EE**: 80,311エントリ
  - 性別バリアント: 28,395 (35.4%)
- **合計**: 104,858エントリ

### 用語抽出（--extract-terms使用時）
- **固有名詞**: 8,590語
- **頻出フレーズ**: 573語
- **合計**: 8,766用語

### 主要な固有名詞
| 英語 | 日本語 | 出現回数 |
|------|--------|----------|
| Iron Throne | アイアンスロウン | 338 |
| Sarevok | サレヴォク | 251 |
| Baldur's Gate | バルダーズ・ゲート | 231 |
| Nashkel | ナシュケル | 227 |
| Flaming Fist | フレイミング・フィスト | 175 |
| Gorion | ゴライオン | 137 |
| Beregost | ベレゴスト | 133 |
| Candlekeep | キャンドルキープ | 133 |

### ファイルサイズ
- 用語抽出なし: 57.44 MB
- 用語抽出付き: 76.69 MB

## 用語集の活用方法

### 1. 翻訳Mod制作
- 固有名詞の統一表記確認
- 性別バリアントの参照
- 既存翻訳の参考資料

### 2. 翻訳支援ツール
- Claude API等への用語集提供
- 機械翻訳の辞書データ
- 翻訳メモリとして活用

### 3. 品質チェック
- 翻訳一貫性の確認
- 同一英語への複数訳検出
- 用語統一の検証

### 4. 研究・分析
- 翻訳パターンの分析
- 文字数比率の研究
- 性別バリアントの統計

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

## 技術仕様

### システムアーキテクチャ
1. **TRAパーサー**: TRAファイルを解析し、エントリを抽出
2. **用語集ビルダー**: 英日エントリをマッピングし、メタデータを生成
3. **用語抽出器**: 固有名詞・頻出フレーズを抽出
4. **JSON出力**: 構造化されたJSONファイルを生成

### 技術スタック
- **Python 3.8+**
- **標準ライブラリ**: json, re, pathlib, argparse, logging
- **オプション**: tqdm (プログレスバー)

### パフォーマンス
- **処理時間**: 約30-40秒（全エントリ、用語抽出付き）
- **メモリ使用量**: 約100-200MB

## ドキュメント

詳細な設計情報は [docs/](docs/) ディレクトリを参照:

- [DESIGN_OVERVIEW.md](docs/DESIGN_OVERVIEW.md) - システム全体設計
- [implementation_plan.md](docs/implementation_plan.md) - 実装詳細計画
- [glossary_structure.md](docs/glossary_structure.md) - データ構造仕様

## 実装状況

### ✅ Phase 1: 基本実装（完了）
- [x] TRAパーサー実装
- [x] 性別バリアント処理
- [x] 用語集ビルダー実装
- [x] メインスクリプト実装
- [x] glossary.json生成

### ✅ Phase 2: 用語抽出（完了）
- [x] 固有名詞抽出
- [x] 頻出フレーズ検出
- [x] ストップワード除外
- [x] 用語頻度インデックス構築

### 💡 Phase 3: 将来的な拡張（オプション）
- [ ] Claude API統合（文脈分析）
- [ ] 差分更新機能
- [ ] 複数出力フォーマット（CSV, SQLite）
- [ ] Web UI（ブラウザ閲覧）
- [ ] 翻訳一貫性レポート

## ライセンス

TBD (未定)

## 注意事項

- このプロジェクトは個人の翻訳Mod制作支援を目的としています
- 公式翻訳の著作権は Beamdog/Overhaul Games に帰属します
- 生成される用語集は研究・学習目的での使用を想定しています

## リンク

- **GitHub**: https://github.com/FriendlyArmInnRegulars/bgee-vanilla-glossary-ja_JP
- **Beamdog公式**: https://www.beamdog.com/

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
