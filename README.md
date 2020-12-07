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

## AWS Lambdaで実行

### policyの作成

```
aws iam create-policy \
        --policy-name stop-running-ec2-rds-instances \
        --policy-document file://policy.json
```

※policyのARNを控えておいてください。  

### roleの作成

```
aws iam create-role \
    --role-name lambda-stop-running-ec2-rds-instances \
    --assume-role-policy-document file://role.json
```

(参考)作成したroleにpolicyをアタッチ

```
aws iam attach-role-policy \
	--role-name lambda-stop-running-ec2-rds-instances \
	--policy-arn <policyのarn>
```

(参考) roleのARNを取得する

```
aws iam get-role --role-name lambda-stop-running-ec2-rds-instances | jq -r '.Role.Arn'
```

### 設定
あらかじめ以下の関数を作成するか、書き換えてください。  

- 関数名:  stop-running-ec2-rds-instances

以下の環境変数を作成する。  

| Key | Description | 
| -- | -- |
| SLACK_CHANNEL | 投稿するSlackのチャンネル名 |
| SLACK_ICON_EMOJI | 投稿時のSlackアイコン |
| SLACK_USERNAME | 投稿時の名前 |
| WEBHOOK_URL | SlackのWebhook URL |

(参考) 関数の作成  
※チャンネルの名前とWebhookのURLを入力してください。  

```
mkdir build
make build
aws lambda create-function \
    --region ap-northeast-1 \
    --role $(aws iam get-role --role-name lambda-stop-running-ec2-rds-instances | jq -r '.Role.Arn') \
    --function-name stop-running-ec2-rds-instances \
    --zip-file fileb://build/lambda.zip \
    --runtime python3.8 \
    --timeout 5 \
    --handler lambda_function.lambda_handler \
    --environment "Variables={ \
        SLACK_CHANNEL='<channel name>', \
        SLACK_ICON_EMOJI=':ghost:', \
        SLACK_USERNAME='lambda-stop-instances', \
        WEBHOOK_URL='<Webhook url>'  \
    }"
```

### 注意点  
※タイムアウトは5秒程度にしておく。  

### デプロイする
ソースコードを書き換えてデプロイする場合は以下のようにします。  
なければ`build`ディレクトリを作成しておく。  

```
mkdir build
```

`make`で実行  

```
make deploy
```

### 実行する

```
make invoke
```


## Licence
MIT
