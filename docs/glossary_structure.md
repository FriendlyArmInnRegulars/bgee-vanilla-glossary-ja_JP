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

## 用語集の用途

1. **翻訳一貫性チェック**: 同じ英語に異なる日本語訳がないか
2. **用語統一**: 固有名詞の表記揺れ検出
3. **機械翻訳の基礎データ**: Claude API等での翻訳支援
4. **翻訳メモリ**: 新規Mod翻訳時の参考資料
