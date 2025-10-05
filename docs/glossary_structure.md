# 用語集データ構造設計書

## 概要

Baldur's Gate Enhanced Edition (BG1EE/BG2EE) の英日翻訳用語集を生成するためのデータ構造を定義します。

## TRAファイル構造の分析結果

### 基本フォーマット
```
@<ID> = ~<テキスト>~
```

### 特殊ケース

1. **性別バリアント** (日本語のみ)
   ```
   @6 = ~しかし俺は何もやっちゃいない！~ ~でも私は何もしていないわ！~
   ```
   - 1つ目: 男性形
   - 2つ目: 女性形

2. **空テキスト**
   ```
   @0 = ~<NO TEXT>~
   ```

3. **プレースホルダー**
   ```
   @33999 = ~placeholder~
   ```

4. **変数タグ**
   - `<CHARNAME>`: キャラクター名
   - `<SIRMAAM>`: Sir/Madam
   - `[ZOMBI01]`: サウンドファイル参照

## 用語集JSONスキーマ (v1.0)

### 全体構造

```json
{
  "metadata": {
    "version": "1.0",
    "generated_at": "ISO8601形式のタイムスタンプ",
    "source_games": ["bg1ee", "bg2ee"],
    "total_entries": 162424,
    "statistics": {
      "bg1ee": {
        "total": 34000,
        "with_translation": 33950,
        "with_gender_variant": 5200,
        "placeholders": 50
      },
      "bg2ee": {
        "total": 128424,
        "with_translation": 127000,
        "with_gender_variant": 18000,
        "placeholders": 1424
      }
    }
  },
  "entries": [
    {
      "id": "bg1ee:1",
      "english": "Why hast thou disturbed me here? Hast thou no manners? Get out!",
      "japanese": {
        "default": "何故に私の邪魔をしに来たのだ？礼儀を知らぬのか？出て行け！",
        "male": null,
        "female": null
      },
      "metadata": {
        "game": "bg1ee",
        "tra_id": 1,
        "has_variables": false,
        "has_sound_ref": false,
        "char_count_en": 60,
        "char_count_ja": 30
      }
    },
    {
      "id": "bg1ee:6",
      "english": "But I have done nothing wrong! Why have you accused me of such a thing?",
      "japanese": {
        "default": null,
        "male": "しかし俺は何もやっちゃいない！なぜそんなことを言うんだ？",
        "female": "でも私は何もしていないわ！なぜそんなことを言うの？"
      },
      "metadata": {
        "game": "bg1ee",
        "tra_id": 6,
        "has_variables": false,
        "has_sound_ref": false,
        "char_count_en": 73,
        "char_count_ja": 28
      }
    }
  ],
  "term_frequency": {
    "Gorion": {
      "count": 45,
      "translations": ["ゴライオン"],
      "entries": ["bg1ee:15", "bg1ee:112", "..."]
    },
    "Iron Throne": {
      "count": 89,
      "translations": ["アイアンスロウン"],
      "entries": ["bg1ee:5", "bg1ee:20", "..."]
    }
  }
}
```

## データ設計のポイント

### 1. エントリ構造

- **id**: `{game}:{tra_id}` 形式で一意に識別
- **english**: 原文テキスト
- **japanese**: 翻訳テキスト
  - `default`: 性別バリアントがない場合
  - `male`: 男性形
  - `female`: 女性形
  - すべてnullの場合はプレースホルダー

### 2. メタデータ

各エントリに付随する情報:
- `game`: bg1ee/bg2ee
- `tra_id`: 元のTRAファイルでの@ID
- `has_variables`: `<CHARNAME>`等の変数タグを含むか
- `has_sound_ref`: `[ZOMBI01]`等のサウンド参照を含むか
- `char_count_en/ja`: 文字数（翻訳長の比較に有用）

### 3. 用語頻度インデックス

翻訳で重要な固有名詞や定型表現を抽出:
- 固有名詞（人名、地名、組織名）
- 頻出フレーズ
- ゲーム固有用語

## 実装時の考慮事項

### スキップすべきエントリ

1. `<NO TEXT>` エントリ
2. `placeholder` エントリ
3. テスト用エントリ（`@30 = ~0~` など）

### 正規化処理

1. **空白文字の統一**: 全角/半角スペース、改行の正規化
2. **チルダのエスケープ**: TRA内での`~`のエスケープ処理
3. **性別バリアント分離**: `~...~ ~...~`形式の正規表現パース

### パフォーマンス最適化

- BG2EEは12万エントリ超なので、ストリーミング処理を検討
- インデックス構築時はメモリ使用量に注意
- 必要に応じてエントリを分割ファイルで保存

## 名詞用語集JSONスキーマ (nouns_glossary.json)

### 概要

`nouns_glossary.json` は、メイン用語集から抽出された固有名詞・専門用語のみを集めた特化型用語集です。重複排除とカテゴリ分類を行い、翻訳Mod制作で頻繁に参照される用語を効率的に検索できる構造になっています。

### 全体構造

```json
{
  "metadata": {
    "source_file": "glossary.json",
    "total_entries_processed": 104858,
    "extraction_date": "ISO8601形式のタイムスタンプ",
    "deduplication_stats": {
      "original_term_count": 32776,
      "deduplicated_term_count": 18626,
      "duplicates_removed": 14150,
      "deduplication_rate": "43.2%"
    },
    "categories": [
      "class",
      "class_race",
      "creature",
      "deity",
      "location",
      "organization",
      "other",
      "proper_noun",
      "race",
      "spell",
      "title"
    ]
  },
  "categories": {
    "location": {
      "count": 1234,
      "terms": [
        {
          "english": "Baldur's Gate",
          "japanese": "バルダーズ・ゲート",
          "categories": ["location", "proper_noun"],
          "ids": ["bg1ee:42", "bg1ee:156", "bg2ee:789"],
          "games": ["bg1ee", "bg2ee"],
          "occurrence_count": 231
        }
      ]
    },
    "proper_noun": {
      "count": 5678,
      "terms": [...]
    }
  }
}
```

### カテゴリ分類

名詞用語集は以下の11カテゴリに自動分類されます:

1. **class**: キャラクタークラス（Fighter, Mage, Clericなど）
2. **class_race**: クラス/種族の組み合わせ（Elf Ranger, Dwarf Fighterなど）
3. **creature**: クリーチャー名（Dragon, Beholder, Mindflayerなど）
4. **deity**: 神格名（Bhaal, Mystra, Helmなど）
5. **location**: 地名（Candlekeep, Nashkel, Athkatlaなど）
6. **organization**: 組織名（Iron Throne, Flaming Fist, Harperなど）
7. **other**: その他の固有名詞
8. **proper_noun**: 人名等の一般的固有名詞
9. **race**: 種族名（Elf, Dwarf, Halflingなど）
10. **spell**: 呪文名（Magic Missile, Fireball, Healなど）
11. **title**: 称号（Lord, Master, Archimageなど）

### エントリ構造

各用語エントリは以下のフィールドを持ちます:

```json
{
  "english": "Iron Throne",
  "japanese": "アイアンスロウン",
  "categories": ["organization", "proper_noun"],
  "ids": ["bg1ee:5", "bg1ee:20", "bg1ee:42"],
  "games": ["bg1ee", "bg2ee"],
  "occurrence_count": 338
}
```

- **english**: 英語の用語（大文字小文字を保持）
- **japanese**: 日本語訳（性別バリアントがある場合は最頻出のものを採用）
- **categories**: 該当するカテゴリのリスト（複数カテゴリに属する場合あり）
- **ids**: この用語が出現する全エントリID
- **games**: 出現するゲーム（bg1ee, bg2ee）
- **occurrence_count**: 総出現回数

### 重複排除ロジック

同一の英語用語で複数の日本語訳が存在する場合、以下の優先順位で統合:

1. **出現回数**: より多く出現する訳を採用
2. **性別バリアント**: 性別バリアントがある場合は男性形を優先
3. **エントリID**: 同数の場合は最初のエントリを採用

例:
```
"Sarevok" -> "サレヴォク" (251回)
"Sarevok" -> "サリヴォク" (3回)
→ "サレヴォク" を採用
```

### 用語抽出基準

以下の条件を満たす用語を自動抽出:

1. **大文字始まり**: 固有名詞の一般的パターン
2. **2-50語**: 単語数が妥当な範囲
3. **ストップワード除外**: 一般的な単語（the, a, is等）を除外
4. **最低出現回数**: 2回以上出現する用語
5. **パターンマッチ**: カテゴリ別の正規表現パターン

### ファイルサイズと統計

- **ファイルサイズ**: 約1.5 MB（メイン用語集の2%）
- **総用語数**: 18,626語（重複排除後）
- **カテゴリ分布**:
  - proper_noun: 約8,000語
  - location: 約1,200語
  - creature: 約800語
  - spell: 約600語
  - その他: 約8,000語

## 用語集の用途

### メイン用語集（glossary.json）

1. **翻訳一貫性チェック**: 同じ英語に異なる日本語訳がないか
2. **用語統一**: 固有名詞の表記揺れ検出
3. **機械翻訳の基礎データ**: Claude API等での翻訳支援
4. **翻訳メモリ**: 新規Mod翻訳時の参考資料

### 名詞用語集（nouns_glossary.json）

1. **高速用語検索**: 固有名詞のみを効率的に検索
2. **カテゴリ別参照**: 地名、人名、呪文名等をカテゴリ別に閲覧
3. **翻訳支援ツール統合**: LLMへの軽量な用語辞書として提供
4. **Mod制作支援**: 新規コンテンツの用語統一確認
