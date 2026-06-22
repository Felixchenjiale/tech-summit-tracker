# Tech Summit Tracker 技术峰会追踪

自动汇总国内技术峰会/大会信息，每3天更新一次。

## 数据格式

`data/summits.json` 包含以下字段：

| 字段 | 说明 |
|------|------|
| id | 唯一标识符 |
| name | 峰会全称 |
| start_date / end_date | 起止日期 YYYY-MM-DD |
| city | 举办城市 |
| venue | 场馆 |
| category | 分类标签：AI / 云 / 开发者 / 硬件·芯片 / 综合 |
| organizer | 主办方 |
| theme | 主题 |
| description | 简介 |
| status | 状态：upcoming / ongoing / ended |
| register_url | 报名链接 |
| source_urls | 信息来源链接 |

## 更新机制

- Agent 每3天自动搜索最新峰会信息并更新 `data/summits.json`
- Web 页面从 GitHub Raw URL 读取 JSON 数据实时展示
- 支持按月份、城市、分类筛选

## 数据来源

- 搜索引擎实时检索
- 各大会官网
- InfoQ / 36kr / 虎嗅等科技媒体
- 活动行 / 百格活动等平台
