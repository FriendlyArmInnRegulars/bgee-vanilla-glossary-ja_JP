# 用語集使用例

このドキュメントでは、生成された用語集 (`glossary.json`) の実際の使用例を紹介します。

## 1. 用語集の読み込み

### Python

```python
import json

# 用語集を読み込む
with open('glossary.json', 'r', encoding='utf-8') as f:
    glossary = json.load(f)

# 基本情報を表示
metadata = glossary['metadata']
print(f"バージョン: {metadata['version']}")
print(f"総エントリ数: {metadata['total_entries']}")
print(f"生成日時: {metadata['generated_at']}")

# BG1EEの統計
bg1ee_stats = metadata['statistics']['bg1ee']
print(f"\nBG1EE統計:")
print(f"  総数: {bg1ee_stats['total']}")
print(f"  性別バリアント: {bg1ee_stats['with_gender_variant']}")
```

### JavaScript (Node.js)

```javascript
const fs = require('fs');

// 用語集を読み込む
const glossary = JSON.parse(fs.readFileSync('glossary.json', 'utf-8'));

// 基本情報を表示
const { metadata } = glossary;
console.log(`バージョン: ${metadata.version}`);
console.log(`総エントリ数: ${metadata.total_entries}`);
```

## 2. 特定の用語を検索

### 英語から日本語を検索

```python
def find_translation(glossary, english_text):
    """英語テキストから日本語訳を検索"""
    for entry in glossary['entries']:
        if entry['english'] == english_text:
            ja = entry['japanese']
            if ja['default']:
                return ja['default']
            elif ja['male']:
                return f"男性: {ja['male']}, 女性: {ja['female']}"
    return None

# 使用例
translation = find_translation(glossary, "Thank you.")
print(f"翻訳: {translation}")
```

### エントリIDから検索

```python
def find_by_id(glossary, entry_id):
    """エントリIDから検索"""
    for entry in glossary['entries']:
        if entry['id'] == entry_id:
            return entry
    return None

# 使用例
entry = find_by_id(glossary, "bg1ee:1")
if entry:
    print(f"英語: {entry['english']}")
    print(f"日本語: {entry['japanese']['default']}")
```

## 3. 固有名詞の翻訳を取得

```python
def get_proper_noun_translation(glossary, noun):
    """固有名詞の日本語訳を取得"""
    term_freq = glossary.get('term_frequency', {})
    if noun in term_freq:
        info = term_freq[noun]
        return {
            'translations': info['translations'],
            'count': info['count'],
            'example_entries': info['entries'][:3]
        }
    return None

# 使用例
result = get_proper_noun_translation(glossary, "Sarevok")
if result:
    print(f"Sarevok の翻訳:")
    print(f"  日本語: {result['translations']}")
    print(f"  出現回数: {result['count']}")
    print(f"  例: {result['example_entries']}")
```

出力:
```
Sarevok の翻訳:
  日本語: ['サレヴォク']
  出現回数: 251
  例: ['bg1ee:251', 'bg1ee:564', 'bg1ee:2319']
```

## 4. 性別バリアントの抽出

```python
def get_gender_variants(glossary, game=None):
    """性別バリアントを持つエントリを抽出"""
    variants = []
    for entry in glossary['entries']:
        # ゲーム指定がある場合はフィルタリング
        if game and entry['metadata']['game'] != game:
            continue

        ja = entry['japanese']
        if ja['male'] or ja['female']:
            variants.append({
                'id': entry['id'],
                'english': entry['english'],
                'male': ja['male'],
                'female': ja['female']
            })
    return variants

# 使用例: BG1EEの性別バリアントを最初の5件取得
variants = get_gender_variants(glossary, game='bg1ee')[:5]
for v in variants:
    print(f"\n英語: {v['english']}")
    print(f"  男性: {v['male']}")
    print(f"  女性: {v['female']}")
```

## 5. 変数タグを含むエントリの検索

```python
def find_entries_with_variables(glossary):
    """<CHARNAME>等の変数タグを含むエントリを検索"""
    var_entries = []
    for entry in glossary['entries']:
        if entry['metadata']['has_variables']:
            var_entries.append({
                'id': entry['id'],
                'english': entry['english'][:100],  # 最初の100文字
                'japanese': entry['japanese']['default'] or entry['japanese']['male']
            })
    return var_entries

# 使用例
var_entries = find_entries_with_variables(glossary)[:3]
for e in var_entries:
    print(f"\nID: {e['id']}")
    print(f"英語: {e['english']}...")
    print(f"日本語: {e['japanese'][:100]}...")
```

## 6. 文字数分析

```python
def analyze_length_ratio(glossary, sample_size=1000):
    """英日の文字数比率を分析"""
    import random

    entries = random.sample(glossary['entries'], min(sample_size, len(glossary['entries'])))
    ratios = []

    for entry in entries:
        en_len = entry['metadata']['char_count_en']
        ja_len = entry['metadata']['char_count_ja']
        if en_len > 0 and ja_len > 0:
            ratios.append(ja_len / en_len)

    avg_ratio = sum(ratios) / len(ratios)
    return {
        'average_ratio': avg_ratio,
        'min_ratio': min(ratios),
        'max_ratio': max(ratios),
        'sample_size': len(ratios)
    }

# 使用例
result = analyze_length_ratio(glossary)
print(f"平均文字数比率（日本語/英語）: {result['average_ratio']:.2f}")
print(f"最小: {result['min_ratio']:.2f}")
print(f"最大: {result['max_ratio']:.2f}")
```

## 7. 頻出フレーズのランキング

```python
def get_top_phrases(glossary, n=10, min_length=5):
    """頻出フレーズのトップN"""
    term_freq = glossary.get('term_frequency', {})

    # フレーズのみ抽出（複数単語）
    phrases = {k: v for k, v in term_freq.items() if len(k.split()) >= 2 and len(k) >= min_length}

    # 出現回数でソート
    sorted_phrases = sorted(phrases.items(), key=lambda x: x[1]['count'], reverse=True)

    return sorted_phrases[:n]

# 使用例
top_phrases = get_top_phrases(glossary, n=10)
print("頻出フレーズ トップ10:")
for i, (phrase, info) in enumerate(top_phrases, 1):
    translation = info['translations'][0] if info['translations'] else 'N/A'
    print(f"{i}. {phrase} ({info['count']}回)")
    print(f"   → {translation}")
```

## 8. 翻訳一貫性チェック

```python
def check_translation_consistency(glossary):
    """同一英語に対する複数の日本語訳を検出"""
    from collections import defaultdict

    en_to_ja = defaultdict(set)

    for entry in glossary['entries']:
        english = entry['english']
        ja = entry['japanese']

        # 日本語訳を取得
        ja_text = ja['default'] or ja['male'] or ja['female']
        if ja_text:
            en_to_ja[english].add(ja_text)

    # 複数の訳がある英語を抽出
    inconsistencies = {k: list(v) for k, v in en_to_ja.items() if len(v) > 1}

    return inconsistencies

# 使用例
inconsistencies = check_translation_consistency(glossary)
print(f"翻訳の揺れがある英語フレーズ: {len(inconsistencies)}個")

# 最初の3つを表示
for i, (english, translations) in enumerate(list(inconsistencies.items())[:3], 1):
    print(f"\n{i}. {english}")
    for tr in translations:
        print(f"   - {tr}")
```

## 9. CSV形式でエクスポート

```python
import csv

def export_to_csv(glossary, output_file, game=None):
    """用語集をCSV形式でエクスポート"""
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # ヘッダー
        writer.writerow(['ID', 'Game', 'English', 'Japanese (Default)', 'Japanese (Male)', 'Japanese (Female)'])

        # データ
        for entry in glossary['entries']:
            if game and entry['metadata']['game'] != game:
                continue

            ja = entry['japanese']
            writer.writerow([
                entry['id'],
                entry['metadata']['game'],
                entry['english'],
                ja['default'] or '',
                ja['male'] or '',
                ja['female'] or ''
            ])

# 使用例
export_to_csv(glossary, 'glossary_export.csv')
print("CSV出力完了: glossary_export.csv")
```

## 10. 特定ゲームのみを抽出

```python
def extract_game_glossary(glossary, game):
    """特定ゲームのエントリのみを抽出"""
    game_entries = [e for e in glossary['entries'] if e['metadata']['game'] == game]

    return {
        'metadata': {
            **glossary['metadata'],
            'source_games': [game],
            'total_entries': len(game_entries)
        },
        'entries': game_entries,
        'term_frequency': glossary.get('term_frequency', {})
    }

# 使用例: BG1EEのみの用語集を作成
bg1ee_glossary = extract_game_glossary(glossary, 'bg1ee')

# ファイルに保存
with open('glossary_bg1ee_only.json', 'w', encoding='utf-8') as f:
    json.dump(bg1ee_glossary, f, ensure_ascii=False, indent=2)

print(f"BG1EE用語集を保存: {len(bg1ee_glossary['entries'])}エントリ")
```

## 11. Webアプリケーションでの使用（Flask例）

```python
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# 起動時に用語集を読み込む
with open('glossary.json', 'r', encoding='utf-8') as f:
    glossary = json.load(f)

@app.route('/search')
def search():
    """英語テキストから翻訳を検索"""
    query = request.args.get('q', '')

    results = []
    for entry in glossary['entries']:
        if query.lower() in entry['english'].lower():
            results.append({
                'id': entry['id'],
                'english': entry['english'],
                'japanese': entry['japanese']
            })
            if len(results) >= 10:  # 最大10件
                break

    return jsonify(results)

@app.route('/term/<term>')
def get_term(term):
    """固有名詞の情報を取得"""
    term_freq = glossary.get('term_frequency', {})
    if term in term_freq:
        return jsonify(term_freq[term])
    return jsonify({'error': 'Term not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

## 12. Claude APIへの用語集提供

```python
import anthropic

def translate_with_glossary(text, glossary, client):
    """用語集を参照しながらClaude APIで翻訳"""

    # 関連する固有名詞を抽出
    term_freq = glossary.get('term_frequency', {})
    relevant_terms = {}

    for term, info in term_freq.items():
        if term in text:
            relevant_terms[term] = info['translations'][0] if info['translations'] else None

    # プロンプト作成
    prompt = f"""以下の英語テキストを日本語に翻訳してください。

【用語集】
以下の固有名詞は指定された訳語を使用してください：
{chr(10).join(f'- {en}: {ja}' for en, ja in relevant_terms.items())}

【翻訳対象テキスト】
{text}

【翻訳】
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

# 使用例（要: anthropic ライブラリのインストール）
# client = anthropic.Anthropic(api_key="your-api-key")
# result = translate_with_glossary("Sarevok plans to take over Baldur's Gate.", glossary, client)
# print(result)
```

---

これらの例を参考に、用途に応じて用語集を活用してください。
