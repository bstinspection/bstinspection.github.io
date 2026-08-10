# AGENTS.md — BST Inspection 多语言项目

## 多语言文本同步规则

当任意一种语言的页面文件内容被修改时：
1. 立即在全部 7 个语言目录中找到对应的文件
2. 在提交前，将同一语义变更**同步应用到所有**语言版本
3. 英文版本（`docs/*.md`）作为内容结构的权威参考；中文版本作为文风权威参考

### 文件映射对照表

| 英文（根目录） | 中文 | 法语 | 俄语 | 西班牙语 | 葡萄牙语 | 阿拉伯语 |
|----------------|---------|--------|---------|---------|------------|--------|
| `docs/about.md` | `docs/zh/about.md` | `docs/fr/about.md` | `docs/ru/about.md` | `docs/es/about.md` | `docs/pt-BR/about.md` | `docs/ar/about.md` |
| `docs/services.md` | ... | ... | ... | ... | ... | ... |
| 所有 .md 页面同理 | | | | | | |

### i18n 数据同步

`docs/_data/i18n.yml` — 全部 7 种语言共用此单一文件。
- 在一个语言分区新增/修改 key 时，须**同时在全部 7 种语言**中操作
- 每个语言分区必须拥有完全相同的 key 集合

### 提交前检查

在执行 `git commit` 之前：
1. 运行：`for lang in zh fr ru es pt-BR ar; do diff -q docs/about.md docs/$lang/about.md; done`
2. 若有页面文件在某语言中被修改但其他语言未修改 → 自动生成缺失的翻译
3. 若差异仅为结构性的（frontmatter/lang 字段）且所有内容一致 → 可以跳过

## 文风与 SKILL 使用规则

### humanizer-zh（去 AI 味）— 善用、多用

- 中文文档必须应用去 AI 味处理，但**适当保持商业宣传的书面冗余表达，不要过分口语化**
- 外文文档亦可参考该 SKILL
- 英文文档（`docs/*.md`）虽是内容结构的权威基准，但**中文文档是文风基准**

### official-document-skill（公文）— 慎用、批判性使用

- 本项目是商业宣传站点，不是公文场景
- 如使用该 SKILL，仅借鉴其正式、克制的行文纪律，必须保持商业宣传的特征，不得沾染公文腔

## 网络 / Git 代理

- 远端仓库：`https://github.com/bstinspection/bstinspection.github.io.git`
- 推送前默认配置 7890 端口代理，失败后清除代理直连重试：
  ```bash
  git config --local http.proxy http://localhost:7890
  git config --local https.proxy http://localhost:7890
  # 执行 git push
  # 若推送失败，清除代理后重试：
  git config --local --unset http.proxy
  git config --local --unset https.proxy
  git push
  ```
- 若直连推送成功，则清除代理：
  ```bash
  git config --local --unset http.proxy
  git config --local --unset https.proxy
  ```

## 架构参考

- **引擎**：Jekyll 静态站点（GitHub Pages）
- **语言**：en ✅ zh ✅ fr ✅ ru ✅ es ✅ pt-BR ✅ ar ✅
- **持久化 i18n 数据**：`docs/_data/i18n.yml`
- **语言子目录**：`docs/zh/` `docs/fr/` `docs/ru/` `docs/es/` `docs/pt-BR/` `docs/ar/`
- **链接的语言前缀**：在模板中使用 Liquid 变量 `{{ lang_prefix }}`
- **当前页面的基础路径**：在模板中使用 `{{ base_path }}`（用于语言切换器链接）
- **语言路由映射**：
  - 英语 → `/`
  - 中文 → `/zh/`
  - 法语 → `/fr/`
  - 俄语 → `/ru/`
  - 西班牙语 → `/es/`
  - 葡萄牙语/巴西 → `/pt-BR/`
  - 阿拉伯语 → `/ar/`
