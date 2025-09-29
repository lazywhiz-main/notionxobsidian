# データベース設計

## 概要

Notion ↔ Obsidian Sync Systemのデータベース設計を定義します。統一データモデル、Notion固有の構造、Obsidian固有の構造、および同期メカニズムを説明します。

## 統一データモデル

### コアエンティティ

```sql
-- コンテンツアイテム（統一モデル）
CREATE TABLE content_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT,
    content_type VARCHAR(50) NOT NULL, -- 'page', 'note', 'database', 'block'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(20) NOT NULL, -- 'notion', 'obsidian'
    source_id VARCHAR(255) NOT NULL, -- 元システムのID
    parent_id UUID REFERENCES content_items(id),
    metadata JSONB,
    sync_status VARCHAR(20) DEFAULT 'synced', -- 'synced', 'pending', 'conflict', 'error'
    sync_version INTEGER DEFAULT 1,
    UNIQUE(source, source_id)
);

-- タグ
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    color VARCHAR(7), -- HEX color code
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- コンテンツアイテムとタグの関連
CREATE TABLE content_item_tags (
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (content_item_id, tag_id)
);

-- リンク関係
CREATE TABLE content_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    target_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    link_type VARCHAR(50), -- 'reference', 'mention', 'embed', 'backlink'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(source_id, target_id, link_type)
);

-- ファイル添付
CREATE TABLE attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    file_size BIGINT,
    mime_type VARCHAR(100),
    source VARCHAR(20) NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Notion固有のデータ構造

### Notion API データモデル

```sql
-- Notionページ
CREATE TABLE notion_pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notion_page_id VARCHAR(255) NOT NULL UNIQUE,
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    parent_page_id VARCHAR(255),
    parent_database_id VARCHAR(255),
    properties JSONB, -- Notionのプロパティ
    icon JSONB, -- アイコン情報
    cover JSONB, -- カバー画像情報
    archived BOOLEAN DEFAULT FALSE,
    created_time TIMESTAMP WITH TIME ZONE,
    last_edited_time TIMESTAMP WITH TIME ZONE,
    created_by JSONB,
    last_edited_by JSONB,
    url VARCHAR(500),
    public_url VARCHAR(500)
);

-- Notionデータベース
CREATE TABLE notion_databases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notion_database_id VARCHAR(255) NOT NULL UNIQUE,
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    title VARCHAR(500),
    description TEXT,
    properties JSONB, -- データベースプロパティ定義
    icon JSONB,
    cover JSONB,
    archived BOOLEAN DEFAULT FALSE,
    created_time TIMESTAMP WITH TIME ZONE,
    last_edited_time TIMESTAMP WITH TIME ZONE,
    created_by JSONB,
    last_edited_by JSONB,
    url VARCHAR(500),
    public_url VARCHAR(500)
);

-- Notionブロック
CREATE TABLE notion_blocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notion_block_id VARCHAR(255) NOT NULL UNIQUE,
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    parent_id VARCHAR(255),
    type VARCHAR(50) NOT NULL, -- 'paragraph', 'heading', 'bulleted_list_item', etc.
    content JSONB, -- ブロックの内容
    properties JSONB, -- ブロックのプロパティ
    has_children BOOLEAN DEFAULT FALSE,
    archived BOOLEAN DEFAULT FALSE,
    created_time TIMESTAMP WITH TIME ZONE,
    last_edited_time TIMESTAMP WITH TIME ZONE,
    created_by JSONB,
    last_edited_by JSONB
);
```

## Obsidian固有のデータ構造

### Obsidian Vault データモデル

```sql
-- Obsidianファイル
CREATE TABLE obsidian_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_extension VARCHAR(10),
    file_size BIGINT,
    created_at TIMESTAMP WITH TIME ZONE,
    modified_at TIMESTAMP WITH TIME ZONE,
    frontmatter JSONB, -- YAML frontmatter
    content_hash VARCHAR(64), -- ファイル内容のハッシュ
    vault_path VARCHAR(500) NOT NULL
);

-- Obsidianリンク
CREATE TABLE obsidian_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file_id UUID REFERENCES obsidian_files(id) ON DELETE CASCADE,
    target_file_path VARCHAR(500),
    link_text VARCHAR(255),
    link_type VARCHAR(20), -- 'wikilink', 'markdown', 'embed'
    position_start INTEGER,
    position_end INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Obsidianタグ
CREATE TABLE obsidian_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID REFERENCES obsidian_files(id) ON DELETE CASCADE,
    tag_name VARCHAR(100) NOT NULL,
    position_start INTEGER,
    position_end INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Obsidianグラフノード
CREATE TABLE obsidian_graph_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID REFERENCES obsidian_files(id) ON DELETE CASCADE,
    node_type VARCHAR(20), -- 'file', 'tag', 'heading'
    node_id VARCHAR(255) NOT NULL,
    position_x FLOAT,
    position_y FLOAT,
    size INTEGER,
    color VARCHAR(7),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Obsidianグラフエッジ
CREATE TABLE obsidian_graph_edges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_node_id UUID REFERENCES obsidian_graph_nodes(id) ON DELETE CASCADE,
    target_node_id UUID REFERENCES obsidian_graph_nodes(id) ON DELETE CASCADE,
    edge_type VARCHAR(20), -- 'link', 'tag', 'mention'
    weight INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 分析・メタデータテーブル

### コンテンツ分析

```sql
-- テキスト分析結果
CREATE TABLE content_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    analysis_type VARCHAR(50) NOT NULL, -- 'similarity', 'topic', 'sentiment', 'summary'
    analysis_data JSONB NOT NULL,
    confidence_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(content_item_id, analysis_type)
);

-- 類似度マトリックス
CREATE TABLE similarity_matrix (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    target_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    similarity_score FLOAT NOT NULL,
    similarity_type VARCHAR(50), -- 'cosine', 'jaccard', 'semantic'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(source_item_id, target_item_id, similarity_type)
);

-- トピッククラスター
CREATE TABLE topic_clusters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_name VARCHAR(255) NOT NULL,
    cluster_description TEXT,
    cluster_centroid JSONB, -- クラスターの中心ベクトル
    cluster_size INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- コンテンツとトピッククラスターの関連
CREATE TABLE content_topic_clusters (
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    topic_cluster_id UUID REFERENCES topic_clusters(id) ON DELETE CASCADE,
    membership_score FLOAT NOT NULL,
    PRIMARY KEY (content_item_id, topic_cluster_id)
);
```

## 同期管理テーブル

### 同期状態管理

```sql
-- 同期ログ
CREATE TABLE sync_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_type VARCHAR(50) NOT NULL, -- 'notion_to_obsidian', 'obsidian_to_notion', 'bidirectional'
    source_id UUID REFERENCES content_items(id),
    target_id UUID REFERENCES content_items(id),
    sync_status VARCHAR(20) NOT NULL, -- 'success', 'error', 'conflict', 'pending'
    error_message TEXT,
    sync_data JSONB, -- 同期時のデータ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 同期競合
CREATE TABLE sync_conflicts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_item_id UUID REFERENCES content_items(id) ON DELETE CASCADE,
    conflict_type VARCHAR(50) NOT NULL, -- 'content', 'metadata', 'structure'
    conflict_data JSONB NOT NULL, -- 競合の詳細
    resolution_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'resolved', 'ignored'
    resolution_data JSONB, -- 解決方法
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- 同期設定
CREATE TABLE sync_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    source_platform VARCHAR(20) NOT NULL, -- 'notion', 'obsidian'
    target_platform VARCHAR(20) NOT NULL,
    sync_frequency VARCHAR(20) DEFAULT 'realtime', -- 'realtime', 'hourly', 'daily'
    sync_rules JSONB, -- 同期ルール
    auto_resolve_conflicts BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## インデックス設計

### パフォーマンス最適化

```sql
-- コンテンツアイテムのインデックス
CREATE INDEX idx_content_items_source ON content_items(source, source_id);
CREATE INDEX idx_content_items_updated_at ON content_items(updated_at DESC);
CREATE INDEX idx_content_items_sync_status ON content_items(sync_status);
CREATE INDEX idx_content_items_parent_id ON content_items(parent_id);

-- タグのインデックス
CREATE INDEX idx_content_item_tags_tag_id ON content_item_tags(tag_id);
CREATE INDEX idx_content_item_tags_content_item_id ON content_item_tags(content_item_id);

-- リンクのインデックス
CREATE INDEX idx_content_links_source_id ON content_links(source_id);
CREATE INDEX idx_content_links_target_id ON content_links(target_id);
CREATE INDEX idx_content_links_link_type ON content_links(link_type);

-- Notion固有のインデックス
CREATE INDEX idx_notion_pages_notion_page_id ON notion_pages(notion_page_id);
CREATE INDEX idx_notion_pages_parent_page_id ON notion_pages(parent_page_id);
CREATE INDEX idx_notion_pages_parent_database_id ON notion_pages(parent_database_id);

-- Obsidian固有のインデックス
CREATE INDEX idx_obsidian_files_file_path ON obsidian_files(file_path);
CREATE INDEX idx_obsidian_files_vault_path ON obsidian_files(vault_path);
CREATE INDEX idx_obsidian_files_content_hash ON obsidian_files(content_hash);

-- 分析結果のインデックス
CREATE INDEX idx_content_analysis_content_item_id ON content_analysis(content_item_id);
CREATE INDEX idx_similarity_matrix_source_item_id ON similarity_matrix(source_item_id);
CREATE INDEX idx_similarity_matrix_target_item_id ON similarity_matrix(target_item_id);
CREATE INDEX idx_similarity_matrix_similarity_score ON similarity_matrix(similarity_score DESC);

-- 同期管理のインデックス
CREATE INDEX idx_sync_logs_sync_type ON sync_logs(sync_type);
CREATE INDEX idx_sync_logs_created_at ON sync_logs(created_at DESC);
CREATE INDEX idx_sync_conflicts_content_item_id ON sync_conflicts(content_item_id);
CREATE INDEX idx_sync_conflicts_resolution_status ON sync_conflicts(resolution_status);
```

## データ変換ルール

### Notion → Obsidian 変換

```python
# Notionページ → Obsidianファイル
def notion_to_obsidian_page(notion_page):
    return {
        'title': notion_page['properties']['title']['title'][0]['text']['content'],
        'content': convert_notion_blocks_to_markdown(notion_page['blocks']),
        'frontmatter': {
            'notion_id': notion_page['id'],
            'created_time': notion_page['created_time'],
            'last_edited_time': notion_page['last_edited_time'],
            'tags': extract_notion_tags(notion_page['properties'])
        },
        'file_path': generate_obsidian_path(notion_page)
    }

# Notionブロック → Markdown
def convert_notion_blocks_to_markdown(blocks):
    markdown_content = []
    for block in blocks:
        if block['type'] == 'paragraph':
            markdown_content.append(block['paragraph']['rich_text'][0]['text']['content'])
        elif block['type'] == 'heading_1':
            markdown_content.append(f"# {block['heading_1']['rich_text'][0]['text']['content']}")
        # ... 他のブロックタイプの変換
    return '\n'.join(markdown_content)
```

### Obsidian → Notion 変換

```python
# Obsidianファイル → Notionページ
def obsidian_to_notion_page(obsidian_file):
    return {
        'title': obsidian_file['title'],
        'blocks': convert_markdown_to_notion_blocks(obsidian_file['content']),
        'properties': {
            'title': {'title': [{'text': {'content': obsidian_file['title']}}]},
            'obsidian_id': obsidian_file['id'],
            'file_path': obsidian_file['file_path']
        }
    }

# Markdown → Notionブロック
def convert_markdown_to_notion_blocks(markdown_content):
    blocks = []
    lines = markdown_content.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            blocks.append({
                'type': 'heading_1',
                'heading_1': {'rich_text': [{'text': {'content': line[2:]}}]}
            })
        elif line.startswith('## '):
            blocks.append({
                'type': 'heading_2',
                'heading_2': {'rich_text': [{'text': {'content': line[3:]}}]}
            })
        # ... 他のMarkdown要素の変換
        else:
            blocks.append({
                'type': 'paragraph',
                'paragraph': {'rich_text': [{'text': {'content': line}}]}
            })
    
    return blocks
```

## データ整合性制約

### 外部キー制約

```sql
-- カスケード削除の設定
ALTER TABLE content_item_tags 
ADD CONSTRAINT fk_content_item_tags_content_item 
FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE;

ALTER TABLE content_item_tags 
ADD CONSTRAINT fk_content_item_tags_tag 
FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;

-- 同期整合性の制約
ALTER TABLE notion_pages 
ADD CONSTRAINT fk_notion_pages_content_item 
FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE;

ALTER TABLE obsidian_files 
ADD CONSTRAINT fk_obsidian_files_content_item 
FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE;
```

### チェック制約

```sql
-- 同期ステータスの有効値
ALTER TABLE content_items 
ADD CONSTRAINT chk_sync_status 
CHECK (sync_status IN ('synced', 'pending', 'conflict', 'error'));

-- ソースプラットフォームの有効値
ALTER TABLE content_items 
ADD CONSTRAINT chk_source 
CHECK (source IN ('notion', 'obsidian'));

-- 類似度スコアの範囲
ALTER TABLE similarity_matrix 
ADD CONSTRAINT chk_similarity_score 
CHECK (similarity_score >= 0 AND similarity_score <= 1);
```

## バックアップ・復旧戦略

### データバックアップ

```sql
-- 重要なテーブルのバックアップ
CREATE TABLE content_items_backup AS SELECT * FROM content_items;
CREATE TABLE sync_logs_backup AS SELECT * FROM sync_logs;
CREATE TABLE sync_conflicts_backup AS SELECT * FROM sync_conflicts;

-- 定期的なバックアップスケジュール
-- 1. 日次フルバックアップ
-- 2. 時間別増分バックアップ
-- 3. 同期前のスナップショット
```

### 復旧手順

```sql
-- 同期競合の復旧
UPDATE sync_conflicts 
SET resolution_status = 'resolved', 
    resolved_at = NOW() 
WHERE resolution_status = 'pending';

-- データ整合性の修復
UPDATE content_items 
SET sync_status = 'synced' 
WHERE sync_status = 'error' 
AND updated_at < NOW() - INTERVAL '1 hour';
```
