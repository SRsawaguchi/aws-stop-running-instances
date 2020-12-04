# Stop running instances
Running中のec2およびrdsインスタンスのうち、以下のタグが付いているインスタンスを停止するスクリプト。  
なお、AWS Lambdaで実行することもできる。  

| Key | Value | 
| -- | -- |
| Env | dev |

## 依存関係のインストール

```
pip install -r requirements.txt
```

## ローカルで実行する

```
python src/stop_instances.py
```

## AWS Lambdaで利用する

### 設定
あらかじめ以下の関数を作成するか、書き換えてください。  

- 関数名: hello_slack `※あとで変える`

以下の環境変数を作成する。  

| Key | Description | 
| -- | -- |
| SLACK_CHANNEL | 投稿するSlackのチャンネル名 |
| SLACK_ICON_EMOJI | 投稿時のSlackアイコン |
| SLACK_USERNAME | 投稿時の名前 |
| WEBHOOK_URL | SlackのWebhook URL |


### 注意点  
※タイムアウトは5秒程度にしておく。  

### デプロイする

```
make deploy
```

### 実行する

```
make invoke
```


## Licence
MIT
