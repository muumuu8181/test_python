# OpenAPI Templates

このディレクトリには、中規模および大規模プロジェクト向けのOpenAPI定義ファイルのテンプレートが含まれています。プロジェクトの規模やチーム構成に合わせて選択してください。

## 1. 中規模プロジェクト向け (`medium/`)

**特徴:**
- 機能ごとにファイルを分割しますが、ディレクトリ階層は浅く保ちます。
- `paths/` と `components/` にファイルを分けることで、単一ファイル `openapi.yaml` が肥大化するのを防ぎます。
- 比較的小規模なチームや、ドメインが複雑に入り組んでいない場合に適しています。

**構成:**
```
medium/
├── openapi.yaml          # エントリーポイント
├── paths/                # パス定義 (例: users.yaml)
└── components/
    ├── schemas/          # スキーマ定義 (例: User.yaml)
    ├── parameters/       # パラメータ定義
    └── responses/        # レスポンス定義
```

## 2. 大規模プロジェクト向け (`large/`)

**特徴:**
- **ドメイン駆動設計 (DDD)** を意識し、機能領域 (Domain) ごとにディレクトリを分割します。
- 各ドメイン (`domains/users` 等) が独立して開発できるように設計されています。
- 共通のスキーマやパラメータは `shared/` ディレクトリで管理します。
- 複数のチームが並行して開発する場合や、マイクロサービスアーキテクチャを採用している場合に適しています。

**構成:**
```
large/
├── openapi.yaml          # 全体のエントリーポイント (各ドメインを参照)
├── domains/              # ドメインごとの定義
│   └── users/
│       ├── index.yaml    # ドメインのエントリーポイント
│       ├── paths/        # ドメイン固有のパス
│       └── schemas/      # ドメイン固有のスキーマ
└── shared/               # 共有リソース
    ├── schemas/          # 共通スキーマ (例: Error)
    └── parameters/       # 共通パラメータ (例: Pagination)
```

## ツールの利用方法

これらのテンプレートは複数のファイルに分割されているため、ツールを使用して単一のファイルにバンドル (結合) することをお勧めします。

### 推奨ツール

1. **swagger-cli**
   ```bash
   npm install -g @apidevtools/swagger-cli
   swagger-cli bundle openapi_templates/medium/openapi.yaml -o dist/openapi.json -t json
   ```

2. **Redocly CLI**
   ```bash
   npm install -g @redocly/cli
   redocly bundle openapi_templates/large/openapi.yaml -o dist/openapi.yaml
   ```

### 検証 (Validation)

作成したファイルが正しいOpenAPI仕様に準拠しているか確認するには、以下のようにコマンドを実行します。

```bash
swagger-cli validate openapi_templates/medium/openapi.yaml
```
