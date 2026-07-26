# 多语言同步规则

## 核心原则
- 修改任意语言的页面文件后，须**同步修改全部 7 种语言**的对应文件
- 英文版本 `docs/*.md` 是内容结构的权威参考

## 文件映射
| 英文（根目录） | 中文 | 法语 | 俄语 | 西班牙语 | 葡萄牙语 | 阿拉伯语 |
|----------------|---------|--------|---------|---------|------------|--------|
| `docs/about.md` | `docs/zh/about.md` | `docs/fr/about.md` | `docs/ru/about.md` | `docs/es/about.md` | `docs/pt-BR/about.md` | `docs/ar/about.md` |

## i18n 数据
- `docs/_data/i18n.yml` 由全部语言共用
- 在一个语言分区增删 key 时，**所有 7 个语言分区**须同步变更
- 每个语言分区的 key 集合必须完全一致

## 提交前检查
1. 运行：`for lang in zh fr ru es pt-BR ar; do diff -q docs/about.md docs/$lang/about.md; done`
2. 若某语言页面被修改但其他语言未改 → 自动生成翻译
3. 仅 frontmatter/lang 字段差异且内容一致 → 可忽略
