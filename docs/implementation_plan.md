# 用語集生成システム実装計画

## 1. システム概要

Baldur's Gate Enhanced Edition (BG1EE/BG2EE) のTRAファイルから翻訳用語集を自動生成するPythonシステム。

## 2. 技術スタック

- **言語**: Python 3.8+
- **必須ライブラリ**:
  - `json`: 用語集出力
  - `re`: 正規表現パース
  - `pathlib`: ファイルパス操作
  - `argparse`: CLIインターフェース
  - `typing`: 型ヒント
- **推奨ライブラリ**:
  - `tqdm`: プログレスバー（大量エントリ処理時）
  - `pydantic`: データ検証（オプション）

## 3. ディレクトリ構成

```
bgee-vanilla-glossary-ja_JP/
├── scripts/
│   ├── requirements.txt          # 依存ライブラリ
│   ├── create_glossary.py        # メインスクリプト
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── tra_parser.py         # TRAパーサー
│   │   ├── glossary_builder.py  # 用語集ビルダー
│   │   ├── term_extractor.py    # 用語抽出器
│   │   └── models.py             # データモデル
│   └── tests/                    # ユニットテスト（オプション）
├── glossary.json                 # 生成される用語集
├── source_tra/                   # 入力TRAファイル
└── docs/                         # ドキュメント
```

## 4. コンポーネント設計

### 4.1 TRAパーサー (`tra_parser.py`)

**責務**: TRAファイルを読み込み、エントリをパース

```python
class TRAEntry:
    """単一のTRAエントリ"""
    tra_id: int
    text: str

class TRAParser:
    """TRAファイルパーサー"""

    def parse_file(self, filepath: Path) -> Dict[int, TRAEntry]:
        """TRAファイルをパースしてエントリ辞書を返す"""

    def parse_japanese_variants(self, text: str) -> Tuple[str, str, str]:
        """日本語の性別バリアントを分離
        Returns: (default, male, female)
        """
```

**パース処理のポイント**:

1. **正規表現パターン**:
   ```python
   ENTRY_PATTERN = r'^@(\d+)\s*=\s*~(.*)~\s*$'
   MULTILINE_PATTERN = r'^@(\d+)\s*=\s*~(.*)~.*~(.*)~\s*$'
   ```

2. **性別バリアント検出**:
   - 行に`~`が3つ以上ある場合、性別バリアントとして処理
   - 1つ目のテキストを`male`、2つ目を`female`とする

3. **エラーハンドリング**:
   - 不正な形式の行はwarningログ出力してスキップ
   - ファイルエンコーディング: UTF-8想定

### 4.2 用語集ビルダー (`glossary_builder.py`)

**責務**: 英日エントリをマッピングし、用語集JSONを構築

```python
class GlossaryEntry:
    """用語集エントリ"""
    id: str
    english: str
    japanese: dict  # {default, male, female}
    metadata: dict

class GlossaryBuilder:
    """用語集ビルダー"""

    def build(self,
              en_entries: Dict[int, TRAEntry],
              ja_entries: Dict[int, TRAEntry],
              game: str) -> List[GlossaryEntry]:
        """英日エントリから用語集を構築"""

    def should_skip_entry(self, en_text: str, ja_text: str) -> bool:
        """エントリをスキップすべきか判定"""
        # <NO TEXT>, placeholder等を除外
```

**スキップ条件**:
- `<NO TEXT>`
- `placeholder`
- 英語が空文字
- 日本語がすべてNone

### 4.3 用語抽出器 (`term_extractor.py`)

**責務**: 頻出用語、固有名詞の抽出

```python
class TermExtractor:
    """用語抽出器"""

    def extract_proper_nouns(self, entries: List[GlossaryEntry]) -> Dict[str, TermInfo]:
        """固有名詞を抽出"""
        # 英語の大文字始まり単語を抽出

    def build_frequency_index(self, entries: List[GlossaryEntry]) -> Dict[str, TermInfo]:
        """頻出語インデックスを構築"""
```

**抽出ロジック**:

1. **固有名詞検出**:
   - 英語で大文字始まりの単語（Gorion, Baldur's Gate等）
   - 頻度2回以上のもののみ
   - 対応する日本語訳を記録

2. **定型句検出**:
   - 完全一致で5回以上出現するフレーズ
   - 例: "Yes.", "No.", "Thank you."等

3. **除外パターン**:
   - 変数タグ: `<CHARNAME>`, `<SIRMAAM>`
   - 一般的な英単語（the, a, is等）のストップワード

### 4.4 データモデル (`models.py`)

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class JapaneseTranslation:
    default: Optional[str] = None
    male: Optional[str] = None
    female: Optional[str] = None

@dataclass
class EntryMetadata:
    game: str
    tra_id: int
    has_variables: bool
    has_sound_ref: bool
    char_count_en: int
    char_count_ja: int

@dataclass
class GlossaryEntry:
    id: str
    english: str
    japanese: JapaneseTranslation
    metadata: EntryMetadata
```

### 4.5 メインスクリプト (`create_glossary.py`)

```python
def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='BG:EE用語集生成')
    parser.add_argument('--games', nargs='+',
                       choices=['bg1ee', 'bg2ee', 'all'],
                       default=['all'])
    parser.add_argument('--output', default='glossary.json')
    parser.add_argument('--include-stats', action='store_true',
                       help='統計情報を含める')

    args = parser.parse_args()

    # 1. TRAファイル読み込み
    # 2. 用語集構築
    # 3. 用語抽出
    # 4. JSON出力
```

## 5. 実装フェーズ

### Phase 1: 基本パーサー (最優先)
- [ ] TRAパーサー実装
- [ ] 基本的なエントリ抽出
- [ ] 性別バリアント処理
- [ ] 簡易的なJSON出力

### Phase 2: 用語集ビルダー
- [ ] 英日マッピング
- [ ] メタデータ生成
- [ ] スキップ条件実装
- [ ] 完全なJSON構造出力

### Phase 3: 用語抽出 (オプション)
- [ ] 固有名詞抽出
- [ ] 頻度インデックス構築
- [ ] 定型句検出

### Phase 4: 最適化・テスト
- [ ] 大量エントリ処理の最適化
- [ ] エラーハンドリング強化
- [ ] ユニットテスト
- [ ] ドキュメント整備

## 6. 使用方法（予定）

```bash
# 環境準備
cd scripts
pip install -r requirements.txt

# 全ゲームの用語集生成
python create_glossary.py --games all --output ../glossary.json --include-stats

# BG1EEのみ
python create_glossary.py --games bg1ee --output ../glossary_bg1ee.json

# BG2EEのみ
python create_glossary.py --games bg2ee --output ../glossary_bg2ee.json
```

## 7. パフォーマンス見積もり

- **BG1EE**: 34,000エントリ → 処理時間 ~5-10秒
- **BG2EE**: 128,424エントリ → 処理時間 ~20-30秒
- **合計**: 162,424エントリ → 処理時間 ~30-40秒

メモリ使用量: ~100-200MB (全エントリをメモリ上に展開)

## 8. 拡張性

将来的な拡張機能:

1. **Claude API統合**: 用語の文脈分析、カテゴリ分類
2. **差分更新**: 既存glossary.jsonとの差分検出・更新
3. **複数出力フォーマット**: CSV, SQLite, Excel対応
4. **翻訳一貫性チェック**: 同一英語に対する複数訳の検出
5. **Web UI**: ブラウザベースの用語集閲覧・検索インターフェース

## 9. 注意事項

- TRAファイルのエンコーディングはUTF-8前提
- 巨大ファイル(BG2EE)処理時はメモリ使用量に注意
- 性別バリアントの正規表現は慎重にテスト
- プレースホルダー等の除外漏れがないか検証
