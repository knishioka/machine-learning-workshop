## 概要
Ollama紹介デモ用のスクリプト

## 準備
### 独自モデルの作成

```sh
ollama create llama3.1-planner -f llama3.1-planner.modelfile
ollama create llama3.1-translator -f llama3.1-translator.modelfile
```

### pipeで出力結果を渡して実行

```sh
ollama run llama3.1-planner "空はなぜ青いのか" |
  tee /dev/tty |
  ollama run deepseek-r1:8b |
  tee /dev/tty |
  ollama run llama3.1-translator
```
