# Stop running instances
Running中のec2およびrdsインスタンスのうち、以下のタグが付いているインスタンスを停止するスクリプト。  

| Key | Value | 
| -- | -- |
| Env | dev |

## 依存関係のインストール

```
pip install -r requirements.txt
```

## 実行する

```
python stop_instances.py
```

## Licence
MIT
