# BST Inspection 官网源码

广州 BST 质量服务公司（Guangzhou BST Technology Services Co., Ltd.）多语言宣传站点的 Jekyll 源码仓库。站点托管于 GitHub Pages，绑定自定义域名 <https://bstinspection.com>，共 7 种语言、91 个页面、49 篇新闻文章。

> 本仓库的项目规则另有 [AGENTS.md](AGENTS.md) 详述（多语言同步、文风、Git 代理、域名管理）。本 README 面向维护者与协作者，目标是让人不读代码也能看懂站点全貌，并照着规范安全地改内容、加翻译、发上线。

---

## 目录

- [一、项目简介](#一项目简介)
- [二、技术栈](#二技术栈)
- [三、目录结构](#三目录结构)
- [四、本地开发指南](#四本地开发指南)
- [五、多语言（i18n）架构](#五多语言i18n架构)
- [六、内容创作规范](#六内容创作规范)
- [七、文风与多语言同步规则](#七文风与多语言同步规则)
- [八、部署与运维](#八部署与运维)
- [九、SEO 实施状态](#九seo-实施状态)
- [十、日常维护清单](#十日常维护清单)
- [十一、联系方式](#十一联系方式)

---

## 一、项目简介

### 1.1 公司背景

- 公司全称：广州 BST 技术服务有限公司（Guangzhou BST Technology Services Co., Ltd.），总部位于广州市黄埔区。
- 前身：香港 Brightsky Technology Services Co., Ltd.。
- 业务定位：面向从中国及亚洲采购的进口商、零售商、分销商，提供第三方质量检验与采购咨询服务。
- 服务网络覆盖 8 个亚洲国家：中国、越南、印度、孟加拉、泰国、马来西亚、柬埔寨、斯里兰卡。
- 检验产品线分三类：
  - **消费品**（业务主体）：家电、家具、厨具、消费电子、照明、玩具、礼品工艺品、五金、服装鞋帽；
  - **工业品**（未来五年重点投入方向）：电线电缆、钢管与铁塔、结构材料、泵、锅炉、阀门、油管，以及钢结构、起重机械、船舶、油气设备；
  - **医疗品**（已成常备品类）：棉签、绷带、血压计、口罩、胶带、眼垫、指夹式血氧仪、体温计。

### 1.2 站点定位

站点是公司的门面与获客入口：用 7 种语言讲清我们是谁、能验什么、怎么合作，展示服务能力与价格，把访客导向联系页。新闻（News）栏目则用来发布公司动态，同时支撑搜索引擎收录。

线上地址：<https://bstinspection.com>（GitHub Pages 托管，DNS 在 NameSilo 管理，详见[第八节](#八部署与运维)）。

### 1.3 业务规模数字

首页统计区展示的四个数字（维护时如与公司实际不符，需同步修改 `docs/index.md` 中 `data-target` 的值与 `i18n.yml` 中对应文案）：

| 数字 | 含义 |
|---|---|
| 15+ | 年行业经验 |
| 8+ | 覆盖国家数 |
| 3000+ | 已完成项目 |
| 99+% | 客户满意度 |

### 1.4 八项检验服务

服务页（`services`）按生产周期顺序组织 8 个锚点，导航与首页卡片均引用这些锚点，增删服务时须全站同步：

| 锚点 | 服务名称 | 检查节点 |
|---|---|---|
| `#fa` | Factory Audit（工厂审核） | 量产前，审核工厂质量体系 |
| `#sca` | Social Compliance Audit（社会责任审核） | 量产前，审核人权、工时、安全等 |
| `#ipc` | Initial Production Check（初期产品检查） | 量产启动时，查部件与来料 |
| `#ipqc` | In-Process Quality Check（制程中检查） | 量产中，提前发现质量隐患 |
| `#dupro` | During Production Check（生产中检查） | 完工 20–30% 时巡检 |
| `#fri` | Final Random Inspection（出货前抽检） | 完工入库后，装运前抽检 |
| `#ls` | Loading Supervision（装柜监督） | 监督装箱、封柜 |
| `#ta` | Testing Arrangement（测试安排） | 安排第三方实验室测试与 CE 认证 |

---

## 二、技术栈

| 组件 | 选型 | 说明 |
|---|---|---|
| 站点引擎 | Jekyll | 静态站，无数据库、无后端 |
| 托管 | GitHub Pages | 推送即部署，绑定自定义域名 |
| 构建依赖 | `github-pages` gem | 见根目录 [Gemfile](Gemfile)，保证本地构建与线上一致 |
| Markdown | kramdown（GFM 输入） | `docs/_config.yml` 中 `input: GFM` |
| 插件 | jekyll-sitemap | 生成 `sitemap.xml`，404 页已排除 |
| 国际化 | 自建 `_data/i18n.yml` + `lang_prefix`/`base_path` Liquid 变量 | 不依赖 i18n 插件，7 语言共用一套模板 |
| 时区 | Asia/Shanghai | 影响文章发布时间 |
| 缓存 | `cache_buster: 5` | 静态资源 URL 后加 `?v=5`，改资源时需手动递增 |

---

## 三、目录结构

站点源码全部位于 `docs/` 目录（GitHub Pages 选定的发布目录），仓库根目录只放配置文件与文档：

```text
bstinspection.github.io/
├── AGENTS.md                  # 项目规则：多语言同步、文风、Git 代理、域名管理
├── Gemfile                    # Ruby 依赖（github-pages gem）
├── SEO-AUDIT.md               # SEO 审计报告与修改意见
├── README.md                  # 本文件（已被 Jekyll exclude，不进入构建）
└── docs/                      # Jekyll 站点源码
    ├── _config.yml            # 站点配置（标题、URL、语言列表、permalink 等）
    ├── CNAME                  # 自定义域名 bstinspection.com
    ├── robots.txt             # 爬虫协议（含 Sitemap 声明）
    ├── 404.html               # 英文 404 页；各语言目录下另有本地化版本
    ├── index.md               # 英文首页
    ├── about.md               # 关于我们
    ├── services.md            # 服务页（含 8 个服务锚点）
    ├── news.md                # 新闻列表页
    ├── pricing.md             # 价格页
    ├── order-procedure.md     # 下单流程
    ├── contact.md             # 联系页
    ├── production-scope.md    # 检验范围
    ├── quality-standard.md    # 质量标准
    ├── quality-link.md        # 质量链接
    ├── reference-reports.md   # 报告样例
    ├── privacy.md             # 隐私政策
    ├── terms.md               # 服务条款
    ├── _data/
    │   └── i18n.yml           # 7 语言共用的单一 i18n 数据文件
    ├── _includes/             # 公共片段
    │   ├── head.html          # <head>：title、meta、字体
    │   ├── header.html        # 站头：导航、服务下拉、语言切换器
    │   ├── footer.html        # 页脚：联系方式、链接、版权
    │   ├── hero.html          # 首页 Hero 区
    │   └── icon.html          # 内联 SVG 图标
    ├── _layouts/              # 页面骨架
    │   ├── default.html       # 基础布局（<html>、阿语 RTL 判断）
    │   ├── home.html          # 首页布局
    │   ├── page.html          # 普通页布局
    │   └── post.html          # 文章布局
    ├── _posts/                # 新闻文章，49 篇（7 个主题 × 7 语言）
    ├── assets/
    │   ├── css/               # 全站样式（3 个 CSS 文件）
    │   ├── js/                # main.min.js（导航、滚动动画、数字滚动）
    │   └── *.woff2            # 自托管字体（12 个字体文件）
    ├── images/                # 站点图片（webp）
    ├── zh/  fr/  ru/  es/  pt-BR/  ar/
    │   ├── index.md ... terms.md   # 该语言的 13 个页面
    │   └── 404.html                # 该语言的 404 页
```

几点说明：

- **英文页面在 `docs/` 根目录**，其余 6 种语言在各自子目录，两边的 `.md` 文件一一对应。
- **`_posts` 不分子目录**，靠文件名后缀区分语言（见[第六节](#六内容创作规范)）。
- **`assets`、`images` 全语言共用**，没有按语言拆分。
- `docs/_config.yml` 的 `exclude` 已排除 `README.md`、`Gemfile`、`vendor`，这些文件不会出现在构建产物中。

---

## 四、本地开发指南

### 4.1 环境要求

- Ruby 3.x（Windows 建议用 [RubyInstaller](https://rubyinstaller.org/) 选 "Ruby+Devkit" 版本，自带 MSYS2 工具链）
- Bundler（一般随 Ruby 一同装好，若缺失执行 `gem install bundler`）
- Git

### 4.2 安装与启动

在仓库根目录执行：

```bash
# 安装依赖（按 Gemfile.lock 锁定的版本）
bundle install

# 本地预览，默认 http://127.0.0.1:4000
bundle exec jekyll serve

# 想边改边看，加 --livereload；改完 _config.yml 需重启
bundle exec jekyll serve --livereload
```

### 4.3 验证页面

```bash
# 首页（英文）
http://127.0.0.1:4000/

# 中文首页
http://127.0.0.1:4000/zh/

# 服务页、新闻页同理
http://127.0.0.1:4000/services/
http://127.0.0.1:4000/zh/news/
```

### 4.4 注意事项

- **务必用 `bundle exec`**，直接 `jekyll serve` 可能用到系统里其他版本的 Jekyll，构建结果与 GitHub Pages 不一致。
- 本地构建产物 `_site/` 已由 Jekyll 默认排除，别手动提交进仓库。
- 修改静态资源（CSS、字体、图片）后，记得把 `docs/_config.yml` 里的 `cache_buster` 数值 +1，否则访客浏览器可能仍加载旧缓存。
- `Gemfile.lock` 若存在请一并提交，保证协作者本地构建版本一致。

---

## 五、多语言（i18n）架构

### 5.1 单一数据文件

全站 7 种语言共用 `docs/_data/i18n.yml` 一个文件。文件顶层是 7 个语言键，每个语言分区内部结构完全一致：

```yaml
en:        # 第 1–88 行
  nav: { home: ..., about: ..., services: ..., ... }   # 导航文案
  hero: { title, subtitle, cta, cta2 }                 # 首页 Hero
  footer: { about, address, email, phone, wechat_id, ... }  # 页脚与联系方式
  news: { title, read_more, back }                     # 新闻栏目
  why: { title, expertise, ... }                       # 首页"为什么选我们"
  stats: { years, countries, projects, satisfaction }  # 首页统计区
  cta: { title, desc, button }                         # 首页底部行动号召
  page: { back_to_top, home }                          # 通用页面元素
  services: { fa, sca, ipc, ipqc, dupro, fri, ls, ta } # 8 项服务名
  service_cards: { fa_desc, ... }                      # 首页服务卡片描述
  index_services: { title, subtitle }                  # 首页服务区标题
  misc: { og_locale, logo_alt, menu_toggle, ... }      # 杂项
zh:        # 第 89 行起，结构与 en 完全相同
fr:
ru:
es:
pt-BR:
ar:
```

**硬性要求：任何一个语言分区新增、修改或删除 key，必须同时在全部 7 个分区做同样操作**，保证各语言 key 集合完全一致。模板按 `site.data.i18n[page.lang].xxx` 取值，缺 key 的页面会静默输出空白，不报错，只能靠逐语言核对发现。

### 5.2 语言路由映射

| 语言 | `page.lang` | URL 前缀 | 页面目录 |
|---|---|---|---|
| 英语 | `en` | `/` | `docs/*.md` |
| 中文 | `zh` | `/zh/` | `docs/zh/` |
| 法语 | `fr` | `/fr/` | `docs/fr/` |
| 俄语 | `ru` | `/ru/` | `docs/ru/` |
| 西班牙语 | `es` | `/es/` | `docs/es/` |
| 葡萄牙语（巴西） | `pt-BR` | `/pt-BR/` | `docs/pt-BR/` |
| 阿拉伯语 | `ar` | `/ar/` | `docs/ar/` |

语言列表同时维护在两处，新增语言时都要改：`docs/_config.yml` 的 `available_langs`，以及 `docs/_includes/header.html` 的语言切换器下拉。

### 5.3 模板变量

- **`lang_prefix`**：当前页的语言前缀。英文为 `''`，其余语言为 `'/' + page.lang`（如 `/zh`）。每个页面正文顶部的 Liquid 片段负责计算它，站内链接统一写成 `{{ lang_prefix }}/services/` 这种形式，保证同一份页面源码在 7 种语言下都链向正确的语言版本。
- **`base_path`**：当前页去掉语言前缀后的路径，供语言切换器使用。切换语言时只换前缀、不动页面路径，例如在 `/zh/services/` 页面上点 "English"，会跳到 `/services/`。

### 5.4 阿拉伯语 RTL

`docs/_layouts/default.html` 对 `page.lang == 'ar'` 的页面输出 `dir="rtl"`，右对齐排版由 CSS 处理。阿语页面内容变动时，除了文字，还要在浏览器里看一眼 RTL 下导航、页脚、卡片的实际效果。

### 5.5 新增一种语言的步骤

1. 在 `docs/_config.yml` 的 `available_langs` 中加入语言代码；
2. 复制 `docs/zh/` 全部文件到新目录（如 `docs/de/`），逐文件把 frontmatter 的 `lang` 改为新代码并翻译正文；
3. 在 `docs/_data/i18n.yml` 末尾追加结构相同的语言分区并完整翻译；
4. 在 `docs/_includes/header.html` 的语言切换器中补一个 `<li>`；
5. 在 `docs/_posts/` 中为每篇文章补对应语言版本（文件名加 `-<lang>` 后缀）；
6. 本地逐个语言页面检查渲染与链接。

---

## 六、内容创作规范

### 6.1 页面 frontmatter 字段

以 `docs/services.md` 为例：

```yaml
---
layout: page            # 使用的布局：page / home / post / default
heading: "Our Services" # 页面主标题（导航与页内 H1 用）
title: "Factory Audit & Inspection Services"  # <title> 用的完整标题
description: "Eight inspection services covering..."  # meta description
lang: en                # 页面语言：en / zh / fr / ru / es / pt-BR / ar
permalink: /services/   # 线上 URL（无尾斜杠会 404 或被重定向）
nav_order: 2            # 页脚等位置的排序权重
sidebar: false          # 是否显示侧栏（仅首页类页面设置）
hero_image: /images/background.jpg  # Hero 背景图（仅首页类页面）
---
```

字段要点：

- `title` 与 `description` 是 SEO 关键字段。91 个页面与 49 篇文章已按语言补齐 description，新写的页面必须继续补齐，且不得与本语言内其他页面重复。
- `permalink` 必须带尾斜杠。本地化页面（`zh/` 等目录下的页面）没有写 `permalink`，靠 Jekyll 默认输出，实测 `/zh/services/` 可用、`/zh/services.html` 为 404。
- 正文里引用站内链接用 `{{ lang_prefix }}/xxx/`，引用服务锚点用 `{{ lang_prefix }}/services/#fa`。
- 页面正文顶部的标准 Liquid 片段（计算 `lang_prefix`）：

```liquid
{% assign lang_prefix = '' %}
{% if page.lang and page.lang != 'en' %}
  {% assign lang_prefix = '/' | append: page.lang %}
{% endif %}
```

### 6.2 布局（_layouts）

| 布局 | 用途 | 被谁使用 |
|---|---|---|
| `default.html` | 最外层骨架，拼装 head/header/footer，处理阿语 RTL | 其他布局的基础 |
| `home.html` | 首页 | `index.md` |
| `page.html` | 普通内容页 | about、services、pricing 等 |
| `post.html` | 新闻文章 | `_posts/` 下文章 |

### 6.3 公共片段（_includes）

`head.html` 管 `<head>`（title、meta、字体）；`header.html` 管导航、服务下拉、语言切换器；`footer.html` 管联系方式与页脚链接；`hero.html` 是首页 Hero；`icon.html` 按名字输出内联 SVG 图标（如 `{% include icon.html name="ship" %}`）。

### 6.4 新闻文章（_posts）

- 命名规则：`YYYY-MM-DD-slug.md`（英文），其他语言在 slug 后加 `-<lang>` 后缀，如 `2026-10-17-bst-expands-industrial-medical-inspection-zh.md`。
- frontmatter 示例：

```yaml
---
layout: post
heading: "BST Expands Product Scope: ..."   # 文章主标题
title: "Product Scope Expanded for ..."     # <title> 用
description: "BST adds medical products ..."  # meta description
date: 2026-10-17 00:00:00 +0800             # 发布时间（含时区）
lang: en                                    # 文章语言
permalink: /news/industrial-medical-inspection-expansion/  # 线上 URL
---
```

- `_config.yml` 中 `permalink: /news/:title/` 是默认规则，文章 frontmatter 里的 `permalink` 可精确指定最终 URL。
- 首页与新闻列表页按 `lang` 字段过滤当前语言的文章：`{% assign lang_posts = site.posts | where: "lang", current_lang %}`，所以 `lang` 字段写错会导致文章"消失"。

---

## 七、文风与多语言同步规则

> 本节是 [AGENTS.md](AGENTS.md) 中相关规则的浓缩，完整规则以 AGENTS.md 为准。

### 7.1 文风

- 中文文档必须做去 AI 味处理：避免空洞总结、排比堆砌、夸大用词，参照仓库引用的 humanizer-zh 方法识别并重写。
- 本仓库是商业宣传站点：保持商业宣传应有的书面表达与专业感，不要为了去 AI 味把文案改成口语化、贴吧化。
- **英文版 `docs/*.md` 是内容结构的权威基准，中文版是文风的权威基准**；外语文种可参考中文版的语气尺度。

### 7.2 多语言同步

改动任何一个语言版本的页面后，按以下流程同步：

1. 在全部 7 个语言目录中找到对应文件；
2. 提交前，把同一语义变更应用到所有语言版本；
3. 提交前运行结构比对（PowerShell 可用 `Compare-Object` 或 Git Bash 的 `diff`）：

```bash
for lang in zh fr ru es pt-BR ar; do diff -q docs/about.md docs/$lang/about.md; done
```

比对结果只应剩 frontmatter 与 `lang` 字段的差异；正文出现语义偏差说明漏改。
4. `i18n.yml` 的 key 变更同样要求 7 个分区完全对齐（见 [5.1](#51-单一数据文件)）。

---

## 八、部署与运维

### 8.1 发布流程

1. 本地 `bundle exec jekyll serve` 验证渲染；
2. 完成多语言同步与提交前检查（见[第十节](#十日常维护清单)）；
3. `git commit` 提交，`git push` 推送到 `https://github.com/bstinspection/bstinspection.github.io.git`；
4. GitHub Pages 自动构建发布，线上地址 <https://bstinspection.com>（`docs/` 为发布目录）。

### 8.2 域名

- `docs/CNAME` 内容为 `bstinspection.com`，删掉或改错这个文件会导致自定义域名失效。
- 域名注册与 DNS 解析在 NameSilo 控制台管理（<https://www.namesilo.com>），本仓库只承载静态内容，不涉及域名注册与解析配置。

### 8.3 Git 代理规则

推送前按以下顺序处理，**任一步骤失败即停止，不再尝试其他方式**：

```bash
# 1. 先清除可能的代理配置，直连推送
git config --local --unset http.proxy
git config --local --unset https.proxy
git push
```

直连失败时，配置 7890 端口代理重试一次：

```bash
git config --local http.proxy http://localhost:7890
git config --local https.proxy http://localhost:7890
git push
```

代理也失败时：立即还原配置并如实报告，交人工处理：

```bash
git config --local --unset http.proxy
git config --local --unset https.proxy
```

推送成功或确认失败后，本地都不应残留任何代理配置。

---

## 九、SEO 实施状态

审计基线见 [SEO-AUDIT.md](SEO-AUDIT.md)（2026-10-17，源码逐行核对 + 线上实测；该报告是审计当时的快照，未随后续实施更新）。技术层改造已由两个提交落地：`b506dab`（抓取基础设施与逐页元数据）与 `8f7ea60`（404 页排除出 sitemap）。当前状态如下。

### 9.1 已完成

| 项目 | 现状 |
|---|---|
| sitemap | `_config.yml` 启用 jekyll-sitemap 插件，`robots.txt` 保留 Sitemap 声明，404 页以 `sitemap: false` 排除 |
| description 全覆盖 | 91 个页面与 49 篇文章的 frontmatter 均按语言补齐；`head.html` 取 `page.description`，缺失才回落到 `site.description` 兜底 |
| hreflang | `head.html` 输出七语言 `rel="alternate"` 两两互指，另有 `x-default` 指向英文版 |
| canonical | `head.html` 输出自引用绝对地址 `{{ site.url }}{{ page.url }}` |
| title 与 H1 关键词化 | title 模板为 `{{ page.title }} \| BST Inspection`；各页 title 按「业务词 + 范围 + 品牌」结构改写，与审计第七章矩阵一致；七语言首页 H1（`i18n.yml` 的 `hero.title`）均为业务词，如 "Third-Party Quality Inspection in China"、"中国第三方验货与质量保证" |
| 404 页修复 | 各语言使用固定 title（如 "Page Not Found"、"页面未找到"）；`head.html` 对 404 输出 `noindex`；"返回首页"链到对应语言首页 |
| 社交卡片 | `head.html` 输出 og:type / title / description / url / image / locale（含其余六语言 alternate）与 twitter:card 等，分享图暂用 `background.jpg` |
| 结构化数据 | `head.html` 输出 ProfessionalService（含 `@id`、`areaServed`、`knowsLanguage`）；`page` 布局另输出 BreadcrumbList |
| 内链与面包屑 | 页脚八个服务锚点全量露出；服务页有锚点目录；内页有可见面包屑；新闻列表带文章摘要 |

### 9.2 待办与范围外

| 项目 | 说明 |
|---|---|
| 站长平台验证 | GSC 建议用 DNS TXT 验证（域名在 NameSilo），Bing 可从 GSC 导入；验证与 sitemap 提交在仓库外操作，`head.html` 未留验证位 |
| GA4 与隐私政策 | `docs/privacy.md` 仍声明不使用分析工具；接 GA4 前须先同步改写 7 语言隐私政策，否则前后矛盾 |
| Service 结构化数据 | 八项服务尚未各输出 `Service` 对象，属审计 P1-2 的剩余部分 |
| 图片性能 | `background.webp`（126 KB）比 `background.jpg`（68 KB）大，`head.html` 却优先 preload webp；内容图缺 `width`/`height` |
| 服务页正文补强 | 锚点目录已有；定义句与 "when to book" 类小标题未补，属 P2-1 的剩余部分 |
| 站外与内容运营 | 外链建设、各语言差异化运营、长文内容资产（P3，长期项） |

以上待办均记录在 SEO-AUDIT.md 的对应编号下，动工前先读全文，按优先级推进。

---

## 十、日常维护清单

新增或修改内容时，按此清单过一遍：

- [ ] 改动涉及某个页面时，7 个语言目录的对应文件都改了；
- [ ] `i18n.yml` 的 key 在 7 个分区中完全一致；
- [ ] 新页面 frontmatter 字段齐全（`layout`/`heading`/`title`/`description`/`lang`/`permalink`）；
- [ ] 新页面 title 按「业务词 + 范围 + 品牌」结构写，description 在本语言内唯一；
- [ ] 新文章命名符合 `YYYY-MM-DD-slug-<lang>.md`，`lang` 字段正确；
- [ ] 站内链接用 `{{ lang_prefix }}`，服务锚点全站一致（8 个）；
- [ ] 改了静态资源，`cache_buster` 已 +1；
- [ ] 本地 `bundle exec jekyll serve` 下逐个语言抽查渲染；
- [ ] 提交前跑过 7 语言 diff 比对；
- [ ] 推送遵守 Git 代理规则，不残留代理配置。

---

## 十一、联系方式

| 渠道 | 信息 |
|---|---|
| 邮箱 | jeffrey@bstinspection.com |
| 电话 | 0086-13798166270 |
| 微信 | JeffreyZengBST |
| 地址 | 广东省广州市黄埔区茂港路环村大街 21 号 3 号楼 2803 室 |

以上信息同步维护在 `docs/_data/i18n.yml` 各语言分区的 `footer` 键下，修改时 7 个分区都要改。

---

*本 README 描述仓库当前状态。规则类内容以 [AGENTS.md](AGENTS.md) 为准；[SEO-AUDIT.md](SEO-AUDIT.md) 是 2026-10-17 的审计基线快照，SEO 各项的实施进度以本文件第九节为准。如各处冲突，先核对仓库源码再改文档。*
