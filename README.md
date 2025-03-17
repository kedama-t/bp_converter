# 血圧表変換

- オムロンヘルスケア[上腕式血圧計 HCR-761AT2](https://store.healthcare.omron.co.jp/item/HCR_761AT2.html)で計測した血圧の CSV を、`日付`、`最高血圧（朝）`、`最低血圧（朝）`、`脈拍（朝）`、`最高血圧（夜）`、`最低血圧（夜）`、`脈拍（夜）`の形式に変換する

## Usage

```sh
uv sync
uv run streamlit run main.py
```
