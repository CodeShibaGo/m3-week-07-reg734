# Virtualenv + VS Code 開發環境筆記

## 1. 如何使用 Virtualenv 建立環境

```bash
# 安裝 virtualenv（若尚未安裝）
python3 -m pip install --user virtualenv

# 建立虛擬環境（在專案根目錄）
python3 -m virtualenv .venv
```

## 2. 調教 VS Code 讓 VirtualEnv 環境更好用

- 開啟專案資料夾
- 按下 `Cmd + Shift + P`，輸入 `Python: Select Interpreter`
- 選擇 `.venv/bin/python` 的解譯器
- 可建立 `.vscode/settings.json` 自動載入：

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python"
}
```

## 3. 如何測試環境是否有載入成功

進入虛擬環境：

```bash
source .venv/bin/activate
```

驗證 Python 路徑是否正確：

```bash
which python
which pip
```

應該要看到 `.venv/bin/` 開頭的路徑。

## 4. 如何判斷套件是否安裝成功

```bash
# 安裝 flask
pip install flask

# 查看已安裝的套件
pip list

# 或指定檢查
pip show flask
```

如果有列出版本與路徑，就代表安裝成功。
