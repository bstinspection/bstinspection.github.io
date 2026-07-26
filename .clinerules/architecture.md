# 项目架构参考

## 引擎
Jekyll 静态站点（GitHub Pages）

## 语言支持
en ✅ zh ✅ fr ✅ ru ✅ es ✅ pt-BR ✅ ar ✅

## 目录结构
- 持久化 i18n 数据：`docs/_data/i18n.yml`
- 语言子目录：`docs/zh/` `docs/fr/` `docs/ru/` `docs/es/` `docs/pt-BR/` `docs/ar/`

## Liquid 变量
- `{{ lang_prefix }}` — 链接的语言前缀
- `{{ base_path }}` — 当前页面的基础路径（用于语言切换器链接）

## 语言路由映射
| 语言 | 路径 |
|------|------|
| 英语 | `/` |
| 中文 | `/zh/` |
| 法语 | `/fr/` |
| 俄语 | `/ru/` |
| 西班牙语 | `/es/` |
| 葡萄牙语/巴西 | `/pt-BR/` |
| 阿拉伯语 | `/ar/` |
