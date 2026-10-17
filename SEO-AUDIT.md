# BST Inspection 站点搜索优化审计与修改意见

审计对象：https://bstinspection.com（Jekyll + GitHub Pages，7 语言）
审计日期：2026-10-17
审计方式：源码逐行核对 + 线上实测（HTTP 状态码、渲染后 `<head>`、多语言跳转）

范围约定：本报告只提修改意见，不修改仓库任何文件；不调整 URL 与页面结构，`/services/#fa` 等八个服务锚点保持现状。

---

## 一、结论摘要

按投入产出排序，最该先动的三件事：

1. **补上 sitemap 与 hreflang**。线上 `/sitemap.xml` 现在是 404，而 `robots.txt` 却把这个地址报给了搜索引擎。同时 7 种语言之间没有任何互指，Google 只能靠 `<html lang>` 猜测语言版本关系。
2. **给 91 个页面各写一条 description**。目前全站 91 个页面共用 `_config.yml` 里同一句英文描述，中文、俄语、阿语页面也一样输出这句英文。
3. **改首页和服务页的 title 与 H1**。线上首页标题是 `Home — Guangzhou BST Tech.`，H1 是公司名，整页没有 "inspection" 或 "quality assurance" 这类业务词。

预期收益：技术层修完，等于把已经写好的内容真正交给搜索引擎；文案层改完，才有机会在 "third party inspection China" 这类商业词上出现。两者缺一，后面所有内容投入的回报都会被压住。

总工作量估算：技术层 2～3 个工作日（含 7 语言文案录入），文案层 3～5 个工作日，内容与站外为持续投入。

---

## 二、现状基线

### 2.1 线上实测结果

| URL | 状态码 | 关键观察 |
|---|---|---|
| `/` | 200 | `<html lang="en">`；title 为 `Home — Guangzhou BST Tech.`；description 为站点兜底英文；无 canonical、hreflang、og、twitter、JSON-LD |
| `/zh/` | 200 | `<html lang="zh">`；title 为 `首页 — Guangzhou BST Tech.`；**description 仍是英文兜底句** |
| `/services/` | 200 | title 为 `Our Services — Guangzhou BST Tech.`，H1 为 `Our Services` |
| `/zh/services/` | 200 | title 为 `我们的服务 — Guangzhou BST Tech.`，H1 为 `我们的服务` |
| `/news/` | 200 | 纯列表，无摘要、无分页 |
| `/news/sri-lanka/` | 200 | 文章正常渲染，title 为 `BST Now Serves Sri Lanka — Guangzhou BST Tech.` |
| `/zh/news/sri-lanka/` | 200 | 语言前缀正常，未出现中英文互相覆盖 |
| `/sitemap.xml` | **404** | robots.txt 却对外声明此地址 |
| `/robots.txt` | 200 | 内容仅四行：`User-agent: *` / `Allow: /` / 空行 / `Sitemap: …` |
| 不存在的路径 | 404 | 状态码正确；但页面 title 输出为 `{{ site.data.i18n[page.lang].misc.page_not_found }} — Guangzhou BST Tech.` |
| `/zh`（无尾斜杠） | 301 → `/zh/` | 规范化正常 |
| `http://` 与 `www.` | 301 → `https://bstinspection.com/` | 规范化正常，无需处理 |

响应头方面，首页 HTML 约 25 KB（含内联 `@font-face`），由 GitHub Pages/Fastly 提供，`Cache-Control: max-age=600`，`Vary: Accept-Encoding` 存在。

### 2.2 源码事实

| 项目 | 现状 | 证据位置 |
|---|---|---|
| 页面总数 | 91 个 `.md`（13 页 × 7 语言）+ 42 篇文章 + 7 个 `404.html` | `docs/` |
| meta description | **91 个页面 0 个 `description` 字段**，唯一来源是站点级兜底 | `docs/_config.yml:3` |
| title 模板 | `{{ page.title }} — {{ site.title }}` | `docs/_includes/head.html:4` |
| 社交卡片 / 结构化数据 | 全部缺失，`grep` 全目录无命中 | `docs/_includes/head.html:1-109` |
| canonical / hreflang | 全部缺失 | 同上 |
| 语言信号 | 只有 `<html lang>`，阿语加 `dir="rtl"` | `docs/_layouts/default.html:2` |
| 本地化页面 permalink | 78 个本地化页面**全部没有** `permalink`。实测 `/zh/services.html` 为 404、`/zh/services/` 为 200，说明这是 Jekyll 3 对页面的默认 pretty 输出，不是配置副作用 | 线上实测 + `docs/_config.yml:25` |
| 首页 H1 | 取 `hero.title`，7 个语言中 6 个是品牌名 `Guangzhou BST Tech.` | `docs/_includes/hero.html:14`、`docs/_data/i18n.yml:17/187/272/357/442/527` |
| 404 页 title | frontmatter 里写了 Liquid，不会被执行，原样输出 | `docs/404.html:3` |
| 锚点引用 | header 全 8 个；footer 仅 5 个（缺 `#ipqc`/`#dupro`/`#ta`）；7 个首页卡片全 8 个 | `docs/_includes/header.html:26-33`、`docs/_includes/footer.html:30-34` |
| 孤儿锚点 | `#ci`（Contact Information）定义但零引用 | `docs/services.md:145` |
| 图片 | 5 个文件；`background.webp` 126 KB 反而比 `background.jpg` 68 KB 大；内容图无 `width/height` | `docs/images/` |
| 未翻译 alt | MIL-STD 抽样表在 ru / es / pt-BR 三个版本仍是英文 alt | 各语言 `quality-standard.md` |
| 死字段 | `nav_order` 写了 10 处，全站模板从未读取 | `docs/about.md:6` 等 |
| 分析与验证 | 无 GA4、无 GSC/Bing 验证、无百度统计 | 全目录无命中 |
| 隐私政策 | 明确写"不使用 Cookie 与分析工具" | `docs/privacy.md:23` |

### 2.3 三条硬约束

**第一，URL 不动，等于放弃"一项服务一个入口"。** 八项服务挤在 `/services/` 单页的八个锚点上。锚点不是独立 URL，不参与独立排名，只能靠该页整体的相关性去争。这是本次结构上的天花板，后面的补偿方案都在这个前提下设计。

**第二，78 个本地化页面没有显式 permalink，但不构成风险。** 这一点在实施阶段做了复核：`/zh/services.html` 返回 404，`/zh/services/` 返回 200，说明本地化页面走的是 Jekyll 3 对页面的默认 pretty 输出，与 `_config.yml:25` 里 posts 的 permalink 设置无关。原报告把它当成"依赖尾斜杠副作用"的判断不成立，已从缺陷清单移除，也不需要批量补 permalink（补了反而会改变输出结构）。

**第三，隐私政策与统计工具互相牵制。** `docs/privacy.md:23` 声明站点不使用 Cookie 与分析工具。如果要接 GA4，7 种语言的隐私政策必须同步改写，否则前后矛盾。报告里给出的替代方案是优先使用 Search Console 与 Bing 站长工具（不写 Cookie），GA4 单列为可选项。

---

## 三、P0 阻断项

不修这几条，其他优化基本拿不到效果。

### P0-1 线上 sitemap.xml 返回 404，robots.txt 却声明了它

**现状证据**
- 实测 `/sitemap.xml` → 404；`/robots.txt` → 200，第 4 行为 `Sitemap: https://bstinspection.com/sitemap.xml`。
- 仓库内 `.xml` 文件数为 0；`docs/_config.yml`（47 行）无 `plugins:` 键；`Gemfile` 只有 `gem "github-pages"`。

**影响**
搜索引擎按 robots.txt 的指引去取 sitemap，拿到 404。91 个页面加 42 篇文章没有任何主动提交渠道，只能等爬虫顺着内链慢慢发现。多语言站点尤其吃亏，六个语言目录的页面藏在二级路径下，抓取优先级本就低。

**改法（二选一，推荐 A）**
- A：在 `_config.yml` 增加 `plugins: [jekyll-sitemap]`，重新构建后由插件生成。该插件在 GitHub Pages 白名单内，无需额外依赖。
- B：手写一个 `docs/sitemap.xml`，用 Liquid 遍历 `site.pages` 与 `site.posts`，可同时输出 `xhtml:link` 的 hreflang 注解。工作量大一些，但对多语言更友好。

无论选哪种，都要把 `robots.txt` 的声明保留，并在上线后到 Search Console 提交一次。

**工作量**：A 方案 0.5 小时；B 方案 3～4 小时。

**验收**：`/sitemap.xml` 返回 200 且 `Content-Type` 为 XML；文件内 URL 数量 ≥ 133；GSC「站点地图」显示"成功"。

### P0-2 91 个页面共用一条 meta description，且六种语言输出英文

**现状证据**
- `grep '^description:'` 在 `docs/` 下只命中 `docs/_config.yml:3` 一处。91 个页面与 42 篇文章的 frontmatter 均无该字段。
- `docs/_includes/head.html:3` 的逻辑是 `page.description` 优先，否则回落到 `site.description`。因此 `/zh/`、`/fr/`、`/ar/` 全部输出同一句英文。
- 实测确认：`/zh/` 的 description 为 `BST provides purchase consultations and quality assurance services to the importers, retailers, distributors who are sourcing from China.`

**影响**
这是全站最直接的点击率损失。Google 遇到重复描述会自行截取正文片段，中文页面的搜索结果里可能出现一句英文，语言与内容都对不上。同时 91 个页面在 SERP 上呈现完全相同的摘要，等于放弃了对每个页面卖点的差异化表达。

**改法**
1. 把 `_config.yml` 的 `description` 保留为兜底值（用于 404 等边缘页），不要删。
2. 给 91 个页面逐个补 frontmatter `description`，内容见第七章矩阵。
3. 文章页补 `description`，42 篇按语种同步。
4. 若不想逐页写，也可在 `_data/i18n.yml` 增加 `meta` 分区按语言存标题与描述，模板按 `page.permalink` 映射。但这样维护难度高于直接写 frontmatter，不推荐。

**工作量**：文案已在第七章备好，录入约 4～6 小时（91 个页面，13 页 × 7 语言，可用脚本批量插入）。

**验收**：随机抽 10 个不同语言页面，`view-source` 中 description 互不相同且与页面语言一致；GSC 覆盖报告无"重复元描述"提示。

### P0-3 七种语言之间没有 hreflang，也没有 x-default

**现状证据**
- 全目录 `grep hreflang` 与 `grep alternate` 均无命中。
- 语言切换器只存在于页面可见区域（`docs/_includes/header.html:42-48`），`<head>` 里没有任何对应声明。
- 模板中已有现成的 `base_path` 计算逻辑（`header.html:5-9`），说明数据齐备，只是没有输出到 head。

**影响**
Google 对多语言站点的语言簇识别主要依赖 hreflang。缺失后有三种代价：各语言版本可能被判为重复内容而只保留一个；法语用户在法国搜索时可能被送到英文页；阿语页面因为 `dir="rtl"` 与字符集差异，更容易被当成低质量镜像。

**改法**
在 `head.html` 用一段循环输出七个 `rel="alternate"`，加一条 `x-default` 指向英文版。代码见附录 A.1。关键点有三个：
- 每条都要绝对 URL（`site.url` + 路径），不能写相对路径。
- 语言代码用 `pt-BR` 原样输出，`hreflang` 大小写不敏感但惯例保持与目录一致。
- 七个语言必须两两互指，即中文页也要指向英文、法语、俄语等其余六种。少一条，Google 就会忽略整组关系。

**工作量**：模板改造 1 小时，验证 1 小时。

**验收**：用 GSC 的"国际化定位"报告或第三方 hreflang 校验工具，确认 7 × 7 = 49 组关系无缺失、无"缺少返回链接"告警。

### P0-4 全站缺 canonical

**现状证据**
- `grep canonical` 全目录零命中。
- 页面可通过 `/zh/`、`/zh`（301 跳转）、`https://www.bstinspection.com/zh/`（301）等多种形式抵达，另有 `/index.html` 这类潜在变体。

**影响**
GitHub Pages 已经做了 http→https、www→裸域、无尾斜杠→有尾斜杠的三层跳转，重复内容风险不算高。但 canonical 仍是廉价保险，尤其是带 `?v=5` 这类缓存参数时（`docs/_config.yml:47` 的 `cache_buster` 被拼在图片和样式表上，一旦有人把带参 URL 分享出去，缺少 canonical 就会产生额外的索引变体）。

**改法**
`head.html` 加一行自引用 canonical：`{{ site.url }}{{ page.url }}`。注意 `page.url` 已含语言前缀，不需要再拼 `lang_prefix`。

**工作量**：0.5 小时。

**验收**：抽查 7 个语言的首页与内页，canonical 均指向自身绝对地址，不含查询参数。

### P0-5 首页 title 与 H1 都不含业务词

**现状证据**
- 线上首页 title：`Home — Guangzhou BST Tech.`（模板 `head.html:4` + `docs/index.md:3` 的 `title: Home`）。
- 首页 H1：`docs/_includes/hero.html:14` 取 `i18n.yml` 的 `hero.title`，英文值为 `Guangzhou BST Tech.`，中文值为 `广州睿翔技术服务有限公司`，其余五种语言直接沿用英文品牌名。
- 真正的关键词句藏在副标题里：`Independent Third-Party Quality Assurance — Justice, Integrity, Science`（`i18n.yml:18`）。

**影响**
首页是权重最高的页面，也是品牌词之外唯一有机会排到行业词首页的页面。现在的标题里既没有 inspection，也没有 China，搜索引擎只能从正文推断主题。H1 用品牌名，同样浪费了页面最强的语义信号。

**改法**
- 保留 H1 作为品牌识别的位置，但在其后增加一行关键词化的 `<p class="hero-subtitle">` 或调整 H1 结构：建议 H1 改为"关键词 + 品牌"的组合式，例如 `Third-Party Quality Inspection in China — BST`。若品牌露出优先，则退一步把 H1 保留为公司名，副标题前置关键词并加粗（视觉上仍是次级）。两种都能接受，前者对排名更有利。
- title 模板改为 `{{ page.title }} | BST Inspection`，并把品牌后缀从 `Guangzhou BST Tech.` 换成 `BST Inspection`。理由：域名是 bstinspection.com，用户搜索品牌时更可能输 "BST inspection"；公司全称留在 `Organization` 结构化数据和页脚即可。
- 中文版对应改为"中国第三方验货与质量保证 — BST"，与公司注册名解耦。

**工作量**：决策 0.5 小时，改 7 语言 `i18n.yml` 与模板 2 小时。

**验收**：首页 title 含 `Inspection` 与 `China`（各语言含对应本地词），长度 ≤ 60 字符；H1 唯一且含业务词。

### P0-6 404 页 title 输出未渲染的 Liquid 源码

**现状证据**
- `docs/404.html:3` 写的是 `title: "{{ site.data.i18n[page.lang].misc.page_not_found }}"`。frontmatter 不执行 Liquid，这个字符串被原样当作 title。
- 实测不存在路径返回的 `<title>` 为 `{{ site.data.i18n[page.lang].misc.page_not_found }} — Guangzhou BST Tech.`。

**影响**
不影响排名，但直接影响用户看到的第一行文字。404 页也是被外链或旧链接带到站内的入口页，标题露出模板代码，观感与专业度都受损。这一页还没有 `noindex`，理论上可能被抓取。

**改法**
把 title 改成各语言的固定文案（例如 `Page Not Found`），或在 `head.html` 中对 `page.layout == '404'` 单独处理。同时给 404 页加 `<meta name="robots" content="noindex">`。

**工作量**：1 小时（含 7 个语言文件）。

**验收**：访问任意不存在路径，title 为正常文案，页面源码含 `noindex`。

---

## 四、P1 高收益项

### P1-1 补 Open Graph 与 Twitter 卡片

**现状证据**：`grep 'og:'` 与 `grep 'twitter:'` 全目录零命中。

**影响**：站点现在唯一的对外传播资产是 7 个语言首页和 42 篇新闻。链接贴到 LinkedIn、WhatsApp、微信、Telegram 时，没有卡片就是一条裸链，没有标题图、没有摘要。B2B 询盘常从这些渠道转发开始，分享形态会直接影响点击。

**改法**：`head.html` 增加 `og:type`、`og:title`、`og:description`、`og:url`、`og:image`、`og:locale`、`og:locale:alternate`（其余六种语言）与 `twitter:card`。图片需要一个 1200×630 的固定分享图，现有 `background.jpg`（1920×1280）可以裁一版，文件名建议 `og-cover.jpg`，避免每次分享都拉整张背景图。

**工作量**：2 小时，含制作分享图。

**验收**：用 LinkedIn Post Inspector 与 Facebook Sharing Debugger 各测一次，标题、描述、图片均正确。

### P1-2 补结构化数据

**现状证据**：`grep 'ld+json'` 零命中。

**影响**：结构化数据本身不加排名，但能让搜索结果出现组织信息、面包屑路径，长期看提升点击率与品牌可信度。对一个做第三方检验的公司，"公司名 + 地址 + 电话 + 服务范围"的结构化声明，也是客户核验真实性的依据。

**改法**：分三类，都在 `head.html` 或布局里输出。
- `Organization` / `ProfessionalService`：名称、logo、地址（黄浦区环村大道 21 号 3 栋 2803）、电话、邮箱、`areaServed` 覆盖八个国家。数据可直接从 `i18n.yml` 的 `footer` 分区取，避免维护两份。
- `Service`：在服务页为八项服务各输出一条，`serviceType` 用英文标准名称（Factory Audit、Social Compliance Audit 等），`provider` 指向 Organization。
- `BreadcrumbList`：文章页已有可见面包屑（`docs/_layouts/post.html:11-15`），补上对应的 JSON-LD 即可；内页目前没有面包屑，P2-4 会补可见版本。

代码见附录 A.2。注意 JSON-LD 里的文本要按 `page.lang` 输出，否则中文页会带出英文公司描述。

**工作量**：4～5 小时。

**验收**：Rich Results Test 三类均无错误；GSC「增强功能」中出现面包屑数据。

### P1-3 13 个页面 × 7 语言的 title 与 description 逐页改写

**现状证据**：英文 title 为 `About Us`、`Our Services`、`Pricing`、`News`、`Contact Us` 这类泛词；中文为 `关于我们`、`我们的服务`、`收费标准`；91 个页面无一有 description。

**影响**：title 是排名与点击的第一要素。`Our Services — Guangzhou BST Tech.` 这样的标题，既没有覆盖 "inspection" 这类主词，也没有体现"从工厂审核到装柜监督"的服务宽度，在 SERP 里与同行并列时几乎没有辨识度。

**改法**：按第七章矩阵逐条替换。三条统一规则：
- title 结构为「业务词 + 地域/范围 + 品牌」，总长 ≤ 60 字符（含 ` | BST Inspection`）。
- description 120～155 字符，一句说清"做什么、给谁做、覆盖哪里"，结尾带行动暗示但不堆感叹号。
- 品牌后缀统一为 `BST Inspection`，与域名一致。

**工作量**：文案录入 4～6 小时。

**验收**：SERP 预览工具抽查 7 语言各 3 页，无截断；同语言内 title 无重复。

### P1-4 接入 Search Console 与 Bing 站长工具

**现状证据**：全目录无 `google-site-verification`、无 Bing 验证文件、无百度统计代码。

**影响**：没有 GSC 就等于在黑暗里做优化。收录了多少页、哪些词有展现、CTR 多少、hreflang 有没有报错，全部看不到。这也解释了为什么 sitemap 404 能一直没被发现。

**改法**
1. GSC 用 DNS TXT 验证（域名在 NameSilo，加一条 TXT 记录即可），避免往仓库塞验证文件。若走 HTML 标签验证，则需在 `head.html` 留一个可配置的验证位。
2. Bing 站长工具可直接从 GSC 导入，顺带覆盖 DuckDuckGo。
3. 百度站长工具单独提交，中文版有实际意义；验证方式建议用 CNAME 或 HTML 标签。
4. 三个平台都提交 sitemap（依赖 P0-1 先完成）。

**工作量**：1～2 小时。

**验收**：GSC 显示"已发现 133 个网址"，hreflang 报告无错误。

### P1-5 统计方案与隐私政策同步

**现状证据**：`docs/privacy.md:23` 明确声明不使用 Cookie 与分析工具；站点无任何统计代码。

**影响**：这条不是纯粹的 SEO 项，但会影响 P1-4 之后能拿到多少数据。接了 GA4 却不改隐私政策，属于自相矛盾；不接 GA4，就只能看 GSC 的展现与点击，看不到站内行为。

**改法**：两条路，选一条即可。
- 保守路线：只用 GSC + Bing，不引入 Cookie，隐私政策不动。成本为零，足够支撑 SEO 决策。
- 完整路线：接 GA4，同时把 7 个语言的 `privacy.md` 第 23 行附近改写成"使用 Google Analytics 4 进行匿名流量统计"，并说明退出方式。

**工作量**：保守路线 0；完整路线 3 小时（含 7 语言文案）。

**验收**：隐私政策文本与实际埋点一致，无相互否定的表述。

### P1-6 修正 404 与错误页的多语言跳转

**现状证据**：404 页的语言切换器指向 `/404.html`、`/zh/404.html` 等七个地址，实测这些地址都返回 200。

**影响**：用户从 404 页切换语言时，看到的是"另一个语言的 404 页"，而不是回到该语言的首页。体验上说不过去，也会让 404 页被正常索引。

**改法**：404 模板的语言切换器改为指向各语言首页，并给 404 页加 `noindex`（与 P0-6 合并处理）。

**工作量**：1 小时。

**验收**：访问不存在路径后点击任意语言，落到该语言首页。

---

## 五、P2 内容与结构补偿

URL 不动，八项服务只能共用一个页面。以下四条是在这个约束下的最优补偿。

### P2-1 服务页做锚点目录与关键词化小标题

**现状证据**：`docs/services.md` 现有 9 个锚点（8 项服务 + `#ci`），标题为 `## 1. Factory Audit (FA) {#fa}` 这类"编号 + 英文缩写"格式，页面顶部没有目录。

**影响**：单页承载八个主题，搜索引擎只能给它一个整体主题判定。页面内部如果缺少清晰的层级和目录，爬虫对各个子主题的识别更弱，用户也很难在长页里定位。

**改法**
- 页面顶部加一个锚点目录（8 项 + 联系方式），既方便用户，也在页面内形成密集的内部链接。
- 每个 H2 后补一句 60～80 词的定义式说明，把 "factory audit"、"pre-shipment inspection"、"social compliance audit" 这类词与具体动作绑定。现有正文偏流程描述，缺少可直接被引用的定义句。
- 给八项服务各加一个 H3 小标题，写清适用场景（如 "When to book: 30–45 days before shipment"），这类短句容易成为精选摘要的候选。
- 保持 `{:#fa}` 锚点不变。

**工作量**：8 项 × 7 语言，写作 2 天，录入 1 天。

**验收**：页面出现可见目录；八项服务在 GSC 中各自带来非品牌词的展现。

**天花板说明**：锚点页面无法像独立 URL 那样针对 "factory audit China" 单独排名。这项补偿能把服务页整体推到相关词的中游，但想拿下单项服务的头部位置，最终仍需拆页。这条留作下一阶段的选项，本次不做。

### P2-2 首页增加服务范围与信任要素

**现状证据**：`docs/index.md` 现有模块为服务卡片、四条优势、四个数字、新闻列表、CTA。文字全部来自 `i18n.yml`，偏短。

**影响**：首页正文实际文字量偏少，除服务卡片外缺少可被引用的实质内容。四个数字（15 年、8 国、3000 项目、99% 满意度）是很好的信任要素，但目前只是数字，没有说明口径。

**改法**
- 数字下方补一行口径说明，例如"8 国"列出具体国家名。国家名单本身就是长尾词（Vietnam、Bangladesh、Sri Lanka 等），且与新闻内容互相印证。
- 首屏下方增加一段 80～120 词的业务说明，明确"我们为从中国及亚洲采购的进口商、零售商、分销商提供……"，把地域与服务对象写进正文。
- 服务卡片文案（`service_cards.*_desc`）各补一个具体交付物，例如"48 小时内出具英文报告"。具体承诺比形容词有用。

**工作量**：1.5 天（含 7 语言翻译）。

**验收**：首页正文（去标签）词数 ≥ 400；"8 国"具体国家名出现在正文中。

### P2-3 新闻页与 42 篇文章的元数据治理

**现状证据**：`docs/news.md` 只输出日期与标题的列表，无摘要、无分页；42 篇文章的标题为新闻式（`BST New Office Address and Updated Contact Information`），无 description。

**影响**：新闻是内容更新的主要来源，但现在的标题对搜索没有价值。办公地址变更这类内容本身也没有搜索需求，真正能带来流量的是"某国检验服务可用""某国供应链质量风险"这类主题。

**改法**
- 列表页补摘要（取正文首段或单独 `excerpt` 字段），每条 40～60 字。
- 42 篇补 description，标题改为"服务 + 地域"结构，例如 `Inspection Services in Sri Lanka: What Importers Should Know`。
- 后续选题围绕搜索需求展开：各国家的进口检验要求、常见质量问题、检验标准解读。这类内容才有长尾价值。
- 新闻列表超过 10 条后加分页，避免单页过长。

**工作量**：存量改写 2 天；后续每篇 2 小时。

**验收**：文章页 description 覆盖 100%；新闻类页面带来非品牌展现。

### P2-4 内链与面包屑

**现状证据**：内页（`page.html`）没有面包屑；文章页有可见面包屑但无结构化数据；footer 只链 5 个服务锚点（`footer.html:30-34`），缺 `#ipqc`、`#dupro`、`#ta`；`#ci` 锚点零引用。

**影响**：内链是爬虫分配权重的通道。服务页是全站最重要的落地页，却缺少从其他页面指向它的上下文链接。页脚少链三个服务，等于人为削弱这三项的入口。

**改法**
- 内页加面包屑（首页 / 当前页），与文章页统一，并输出 `BreadcrumbList`。
- footer 补齐剩余三个锚点，八个服务全量露出。
- `#ci` 要么在目录里链上，要么删掉锚点，不要留孤儿。
- 正文内做上下文链接：关于页提到"工厂审核"时链到 `#fa`，质量标准页提到抽样时链到 `#fri`，价格页链到 `#ci`。
- 首页新闻列表与新闻页之间已有链接，保持即可。

**工作量**：1 天。

**验收**：全站无孤儿锚点；每个服务锚点至少被 3 个不同页面引用。

### P2-5 图片与首屏性能

**现状证据**
- `docs/images/background.webp` 为 126 KB，比 `background.jpg` 的 68 KB 大 86%。`hero.html:9` 优先加载 webp，等于选了更大的那个。
- `hero.html:10` 的 LCP 背景图 `alt=""`（装饰图可接受，但该图同时是 LCP 元素）。
- `quality-standard.md` 的抽样表在 ru / es / pt-BR 三个版本仍是英文 alt。
- 内容图都没有 `width`/`height`，存在 CLS 风险。
- 12 个 woff2 字体文件，Inter latin-ext 单个 85 KB；`head.html` 只 preload 了 `inter-400-latin` 与 `poppins-700-latin` 两个，策略基本正确。

**影响**：页面速度是排名因素之一，首屏大图直接影响 LCP。webp 比 jpg 大属于打包失误，不涉及设计取舍。

**改法**
- 重新压缩 `background.webp`，目标 ≤ 60 KB（质量 75～80 即可，背景图本身带遮罩层）。压缩后保留 `<picture>` 结构。
- 内容图补 `width`/`height` 或 CSS `aspect-ratio`。
- 补齐三个语言的 alt 翻译。
- 中文、日文等 CJK 字符不落在 Inter 的 unicode-range 内，会回退系统字体。这不是缺陷，但如果中文版首屏字体跳动明显，可考虑给中文单独指定 `font-family` 回退栈。

**工作量**：半天。

**验收**：PageSpeed Insights 移动端 LCP ≤ 2.5s，CLS ≤ 0.1。

### P2-6 清理死字段

**现状证据**：`nav_order` 在 10 个英文页面里写了值，但全站模板从未读取。

**影响**：属于噪音，会误导后续维护者以为导航顺序由它控制。不影响排名，也不影响渲染。

**改法**：实施阶段决定保留不动。它符合 Jekyll 的常规约定，将来若把导航改成数据驱动可以直接启用，删掉再恢复的成本更高。真正要避免的是"以为它在生效"，记在这里备案即可。本地化页面的 permalink 经复核无风险，见 2.3 第二段。

**工作量**：0。

**验收**：无。

---

## 六、P3 长期运营

### P3-1 站外信任信号

**现状**：站点无外链建设痕迹，无社交媒体资料链接。

**做法**
- 公司 LinkedIn 页面与站点互链，新闻同步发布。B2B 采购负责人在做供应商尽调时，会交叉核对 LinkedIn 与官网。
- 行业协会、展会（广交会、各类消费品展）的参展商名录，是高质量且相关的外链来源。
- 检验行业目录、B2B 平台（阿里、环球资源）的供应商档案里填写官网地址。
- 客户案例页（需授权）比任何形容词都有说服力，也容易被引用。

**验收**：GSC「链接」报告出现 ≥ 10 个引用域，且锚文本含品牌词或服务词。

### P3-2 各语言市场的差异化运营

七种语言不能平均用力。按采购活跃度排优先级：

| 语言 | 优先级 | 关键词侧重 | 运营动作 |
|---|---|---|---|
| 英文 | 高 | third party inspection China、factory audit、pre-shipment inspection | 主站内容深耕，长文与案例优先 |
| 西班牙语 | 高 | inspección de calidad en China、auditoría de fábrica | 拉美进口商集中，可做西语案例 |
| 俄语 | 中高 | инспекция качества в Китае、аудит фабрики | 俄语区采购商依赖 Yandex，建议同步提交 Yandex Webmaster |
| 葡萄牙语（巴西） | 中高 | inspeção de qualidade na China | 巴西进口商体量大，注意 `pt-BR` 与 `pt-PT` 用词差异 |
| 阿拉伯语 | 中 | فحص الجودة في الصين、التفتيش قبل الشحن | 保持 RTL 与阿语排版正确性，Google 阿语区搜索占比高 |
| 法语 | 中 | inspection qualité Chine、audit d'usine | 西非与北非市场，法语区采购决策链较长 |
| 中文 | 中 | 第三方验货、中国验货公司、工厂审核 | 与英文站互不冲突，可承接国内贸易公司与外贸 SOHO |

**注意**：俄语市场除 Google 外要覆盖 Yandex，阿语市场需确认 `hreflang="ar"` 是否要细分为 `ar-SA`、`ar-AE`。当前统一用 `ar` 可以接受，不必过度细分。

### P3-3 度量与迭代节奏

- 每月看一次 GSC：展现量、点击率、平均排名、覆盖错误。
- 每季度看一次关键词分布：哪些词进了前 20 但没进前 10，针对性补内容。
- 每半年复核一次 hreflang 与 sitemap，尤其在新增加语言或页面时。
- 建立一张关键词—页面映射表，避免多个页面互相竞争同一个词（现在的 title 全是泛词，这个问题会在改写后浮现）。

### P3-4 内容资产建设

第三方检验行业的搜索需求集中在三类：某国进口检验要求、某类产品的常见缺陷、检验标准与流程怎么读。站点已有 MIL-STD-105E 抽样表、质量标准页、参考报告页，底子不错，缺的是把这些资产组织成可被搜索到的问答式内容。

建议每年产出 12～20 篇长文，围绕实际客户问题写。这类内容转化率高于新闻稿，也更适合被同行与采购方引用。

---

## 七、7 语言 × 13 页面 title 与 description 建议矩阵

使用说明：
- title 一律含品牌后缀 ` | BST Inspection`，总长按 ≤ 60 字符控制；description 按 120～155 字符控制。
- 英文条目实测落在 title 37～58 字符、description 128～152 字符区间。俄语、阿语等语种按字符计会偏短或偏长，落地时用附录 A.3 的脚本统一跑一遍，再以 SERP 预览截图确认截断位置。
- 所有条目必须 7 语言成套落地。按 `AGENTS.md` 的规则，任何一页改动都要在七个目录同步，不能只改英文。
- 品牌后缀从 `Guangzhou BST Tech.` 改为 `BST Inspection`。公司全称保留在页脚、`Organization` 结构化数据与关于页正文，不影响品牌一致性。

### 7.1 首页 `/` · `index.md`

| 语言 | title | description |
|---|---|---|
| en | Third-Party Quality Inspection China \| BST Inspection | Independent third-party quality inspection in China and 8 Asian countries. Factory audits, production checks and loading supervision for importers. |
| zh | 中国第三方验货与质量检验 \| BST Inspection | BST 为从中国及亚洲八国采购的进口商、零售商与分销商提供独立第三方验货、工厂审核与装柜监督服务，48 小时内出具英文报告。 |
| fr | Inspection qualité en Chine \| BST Inspection | Inspection tierce partie indépendante en Chine et dans 8 pays d'Asie : audit d'usine, contrôle en production et supervision du chargement. |
| ru | Инспекция качества в Китае \| BST Inspection | Независимая инспекция качества в Китае и 8 странах Азии: аудит фабрики, проверка в процессе производства и надзор при погрузке. |
| es | Inspección de calidad en China \| BST Inspection | Inspección independiente de calidad en China y 8 países de Asia: auditoría de fábrica, control en producción y supervisión de carga. |
| pt-BR | Inspeção de qualidade na China \| BST Inspection | Inspeção independente de qualidade na China e em 8 países da Ásia: auditoria de fábrica, controle em produção e supervisão de embarque. |
| ar | فحص الجودة في الصين \| BST Inspection | فحص جودة مستقل في الصين و8 دول آسيوية: تدقيق المصانع، ومراقبة الإنتاج، والإشراف على التحميل، مع تقارير بالإنجليزية. |

### 7.2 关于我们 `/about/` · `about.md`

| 语言 | title | description |
|---|---|---|
| en | About BST Inspection: QA Partner in Asia \| BST Inspection | BST is a Guangzhou quality assurance firm serving importers and retailers sourcing from China and 8 Asian countries. Independent, factory-floor based. |
| zh | 关于 BST：亚洲质量保证伙伴 \| BST Inspection | BST 是一家位于广州的第三方质量保证公司，为从中国及亚洲八国采购的进口商与零售商提供驻厂检验服务，团队覆盖主要制造基地。 |
| fr | À propos de BST : assurance qualité \| BST Inspection | BST est une société d'assurance qualité basée à Guangzhou. Nous accompagnons les importateurs en Chine et dans 8 pays d'Asie, sur le terrain. |
| ru | О компании BST: контроль качества \| BST Inspection | BST — компания по обеспечению качества в Гуанчжоу. Мы работаем для импортеров в Китае и 8 странах Азии, с проверками на производстве. |
| es | Sobre BST: socio de calidad en Asia \| BST Inspection | BST es una firma de aseguramiento de calidad en Guangzhou. Trabajamos para importadores en China y 8 países de Asia, con inspección en fábrica. |
| pt-BR | Sobre a BST: parceira de qualidade \| BST Inspection | A BST é uma empresa de garantia de qualidade em Guangzhou. Atendemos importadores na China e em 8 países da Ásia, com inspeção na fábrica. |
| ar | عن BST: شريك الجودة في آسيا \| BST Inspection | BST شركة لضمان الجودة مقرها قوانغتشو، تخدم المستوردين في الصين و8 دول آسيوية من خلال فحص ميداني داخل المصانع. |

### 7.3 服务 `/services/` · `services.md`

| 语言 | title | description |
|---|---|---|
| en | Factory Audit & Inspection Services \| BST Inspection | Eight inspection services covering the full production cycle: factory audit, social compliance, IPC, IPQC, DUPRO, final random inspection and loading. |
| zh | 工厂审核与验货服务全流程 \| BST Inspection | 覆盖生产全周期的八项服务：工厂审核、社会责任审核、初期生产检查、过程质量控制、生产中期检查、最终随机抽样、装柜监督与测试安排。 |
| fr | Audit d'usine et inspections \| BST Inspection | Huit prestations sur tout le cycle de production : audit d'usine, conformité sociale, IPC, IPQC, DUPRO, inspection finale et supervision du chargement. |
| ru | Аудит фабрики и инспекции \| BST Inspection | Восемь услуг по всему циклу производства: аудит фабрики, социальный аудит, IPC, IPQC, DUPRO, финальная инспекция и надзор при погрузке. |
| es | Auditoría de fábrica e inspecciones \| BST Inspection | Ocho servicios en todo el ciclo productivo: auditoría de fábrica, cumplimiento social, IPC, IPQC, DUPRO, inspección final y supervisión de carga. |
| pt-BR | Auditoria de fábrica e inspeções \| BST Inspection | Oito serviços em todo o ciclo produtivo: auditoria de fábrica, conformidade social, IPC, IPQC, DUPRO, inspeção final e supervisão de embarque. |
| ar | تدقيق المصانع وخدمات الفحص \| BST Inspection | ثماني خدمات تغطي دورة الإنتاج كاملة: تدقيق المصنع، والامتثال الاجتماعي، وفحص الإنتاج، والفحص النهائي، والإشراف على التحميل. |

### 7.4 联系我们 `/contact/` · `contact.md`

| 语言 | title | description |
|---|---|---|
| en | Contact BST in Guangzhou, China \| BST Inspection | Contact BST in Guangzhou for a quote or inspection booking. Email, phone and WeChat details, plus our office address in Huangpu District. |
| zh | 联系广州 BST 验货团队 \| BST Inspection | 邮件、电话或微信联系广州 BST，获取验货报价与排期。办公室位于广州市黄浦区茅岗路环村大街 21 号 3 栋 2803 室。 |
| fr | Contacter BST à Guangzhou \| BST Inspection | Contactez BST à Guangzhou pour un devis ou une réservation d'inspection. E-mail, téléphone, WeChat et adresse du bureau à Huangpu. |
| ru | Связаться с BST в Гуанчжоу \| BST Inspection | Свяжитесь с BST в Гуанчжоу, чтобы получить расчет стоимости или заказать инспекцию. Почта, телефон, WeChat и адрес офиса в Хуанпу. |
| es | Contacto con BST en Guangzhou \| BST Inspection | Contacte con BST en Guangzhou para un presupuesto o reservar una inspección. Correo, teléfono, WeChat y dirección en el distrito de Huangpu. |
| pt-BR | Fale com a BST em Guangzhou \| BST Inspection | Fale com a BST em Guangzhou para orçamento ou agendamento de inspeção. E-mail, telefone, WeChat e endereço no distrito de Huangpu. |
| ar | تواصل مع BST في قوانغتشو \| BST Inspection | تواصل مع BST في قوانغتشو لطلب عرض سعر أو حجز فحص. بريد إلكتروني وهاتف وWeChat وعنوان المكتب في حي هوانغبو. |

### 7.5 收费标准 `/pricing/` · `pricing.md`

| 语言 | title | description |
|---|---|---|
| en | Inspection Pricing & Quotes in China \| BST Inspection | Inspection fees depend on service type, man-days and location. Request a quote for factory audits, production checks or loading supervision. |
| zh | 验货费用与报价说明 \| BST Inspection | 验货费用由服务类型、人天与地区决定。工厂审核、过程检查与装柜监督可按项目报价，批量订单另有优惠，欢迎来函索取报价单。 |
| fr | Tarifs des inspections en Chine \| BST Inspection | Les tarifs dépendent du type de prestation, du nombre de jours et de la zone. Demandez un devis pour un audit, un contrôle ou un chargement. |
| ru | Стоимость инспекции в Китае \| BST Inspection | Стоимость зависит от вида услуги, числа человеко-дней и региона. Запросите расчет для аудита, проверки производства или погрузки. |
| es | Precios de inspección en China \| BST Inspection | El precio depende del servicio, los días de trabajo y la ubicación. Solicite presupuesto para auditoría, control en producción o carga. |
| pt-BR | Preços de inspeção na China \| BST Inspection | O preço depende do serviço, dos dias de trabalho e da localização. Solicite orçamento para auditoria, controle em produção ou embarque. |
| ar | أسعار الفحص في الصين \| BST Inspection | تختلف الأسعار حسب نوع الخدمة وعدد أيام العمل والموقع. اطلب عرض سعر لتدقيق المصنع أو مراقبة الإنتاج أو الإشراف على التحميل. |

### 7.6 新闻 `/news/` · `news.md`

| 语言 | title | description |
|---|---|---|
| en | Inspection News & Market Updates \| BST Inspection | Company news, new service coverage and inspection market updates from BST. Country launches and practical notes for importers sourcing in Asia. |
| zh | 公司动态与检验行业资讯 \| BST Inspection | BST 的服务覆盖扩展、办事机构变动与检验行业观察。按国家与品类整理，供从亚洲采购的进口商参考。 |
| fr | Actualités et veille qualité \| BST Inspection | Nouvelles de BST, extensions de couverture et notes pratiques pour les importateurs en Asie. Mises à jour par pays et par secteur. |
| ru | Новости и обзоры рынка \| BST Inspection | Новости BST, расширение географии услуг и практические заметки для импортеров в Азии. Обновления по странам и отраслям. |
| es | Noticias y novedades del sector \| BST Inspection | Noticias de BST, ampliación de cobertura y notas prácticas para importadores en Asia. Actualizaciones por país y sector. |
| pt-BR | Notícias e atualizações do setor \| BST Inspection | Notícias da BST, ampliação de cobertura e notas práticas para importadores na Ásia. Atualizações por país e setor. |
| ar | أخبار الشركة ومستجدات السوق \| BST Inspection | أخبار BST وتوسّع تغطية الخدمات وملاحظات عملية للمستوردين من آسيا، مرتبة حسب الدولة والقطاع. |

### 7.7 生产范围 `/production-scope/` · `production-scope.md`

| 语言 | title | description |
|---|---|---|
| en | Products We Inspect in China & Asia \| BST Inspection | Product categories BST inspects in China and Asia, from textiles and footwear to electronics, furniture, toys and hardware. See the full scope. |
| zh | 我们检验的产品品类与行业 \| BST Inspection | BST 的检验范围覆盖纺织服装、鞋类、电子电器、家具、玩具、五金工具与日用消费品，按品类提供对应的检验要点与抽样方案。 |
| fr | Produits contrôlés en Chine et Asie \| BST Inspection | Catégories contrôlées par BST : textile, chaussures, électronique, mobilier, jouets, quincaillerie et biens de consommation. Voir le périmètre. |
| ru | Какие товары мы проверяем \| BST Inspection | Категории товаров, которые проверяет BST: текстиль, обувь, электроника, мебель, игрушки, инструмент и потребительские товары. |
| es | Productos que inspeccionamos \| BST Inspection | Categorías que inspecciona BST: textil, calzado, electrónica, muebles, juguetes, ferretería y bienes de consumo. Consulte el alcance completo. |
| pt-BR | Produtos que inspecionamos \| BST Inspection | Categorias inspecionadas pela BST: têxtil, calçados, eletrônicos, móveis, brinquedos, ferramentas e bens de consumo. Veja o escopo completo. |
| ar | المنتجات التي نفحصها \| BST Inspection | فئات المنتجات التي تفحصها BST: المنسوجات والأحذية والإلكترونيات والأثاث والألعاب والأدوات والسلع الاستهلاكية. |

### 7.8 质量标准 `/quality-standard/` · `quality-standard.md`

| 语言 | title | description |
|---|---|---|
| en | AQL & MIL-STD-105E Standards \| BST Inspection | BST applies AQL and MIL-STD-105E sampling to every inspection. Read how sample sizes, acceptance limits and defect classification work. |
| zh | AQL 与 MIL-STD-105E 抽样标准 \| BST Inspection | BST 的检验按 AQL 与 MIL-STD-105E 抽样方案执行。本页说明抽样数量、允收上限与缺陷分级的具体判定方式。 |
| fr | Normes AQL et MIL-STD-105E \| BST Inspection | BST applique l'échantillonnage AQL et MIL-STD-105E à chaque contrôle. Taille d'échantillon, limites d'acceptation et classement des défauts. |
| ru | Стандарты AQL и MIL-STD-105E \| BST Inspection | BST применяет выборку по AQL и MIL-STD-105E. Объем выборки, приемочные пределы и классификация дефектов описаны на этой странице. |
| es | Normas AQL y MIL-STD-105E \| BST Inspection | BST aplica muestreo AQL y MIL-STD-105E en cada inspección. Tamaño de muestra, límites de aceptación y clasificación de defectos. |
| pt-BR | Normas AQL e MIL-STD-105E \| BST Inspection | A BST aplica amostragem AQL e MIL-STD-105E em cada inspeção. Tamanho da amostra, limites de aceitação e classificação de defeitos. |
| ar | معايير AQL و MIL-STD-105E \| BST Inspection | تطبّق BST أسلوب أخذ العينات وفق AQL وMIL-STD-105E، وتوضح هذه الصفحة حجم العينة وحدود القبول وتصنيف العيوب. |

### 7.9 下单流程 `/order-procedure/` · `order-procedure.md`

| 语言 | title | description |
|---|---|---|
| en | How to Book an Inspection in 4 Steps \| BST Inspection | Book an inspection in four steps: send the request, confirm the quote, schedule the visit and receive the report. Typical lead time is 48 hours. |
| zh | 四步预约验货流程 \| BST Inspection | 提交申请、确认报价、安排行程、接收报告。常规验货从确认到出具报告约需 48 小时，遇到紧急订单可申请加急安排。 |
| fr | Commander une inspection en 4 étapes \| BST Inspection | Quatre étapes : demande, confirmation du devis, planification et remise du rapport. Le délai habituel est de 48 heures après confirmation. |
| ru | Как заказать инспекцию: 4 шага \| BST Inspection | Четыре шага: заявка, подтверждение стоимости, планирование выезда и получение отчета. Обычный срок — 48 часов после подтверждения. |
| es | Cómo contratar una inspección \| BST Inspection | Cuatro pasos: solicitud, confirmación del presupuesto, programación de la visita y entrega del informe. El plazo habitual es de 48 horas. |
| pt-BR | Como contratar uma inspeção \| BST Inspection | Quatro etapas: solicitação, confirmação do orçamento, agendamento da visita e entrega do relatório. O prazo usual é de 48 horas. |
| ar | كيف تطلب خدمة الفحص \| BST Inspection | أربع خطوات: إرسال الطلب، وتأكيد عرض السعر، وتحديد موعد الزيارة، واستلام التقرير. المدة المعتادة 48 ساعة بعد التأكيد. |

### 7.10 参考报告 `/reference-reports/` · `reference-reports.md`

| 语言 | title | description |
|---|---|---|
| en | Sample Inspection Reports (PDF) \| BST Inspection | Download sample BST inspection reports. See how findings, photos, defect classification and measurements are presented in the final PDF. |
| zh | 检验报告样本下载 \| BST Inspection | 查看 BST 的实际检验报告样本，了解缺陷记录、现场照片、测量数据与结论页的呈现方式，报告以英文出具。 |
| fr | Exemples de rapports d'inspection \| BST Inspection | Consultez des exemples de rapports BST : constats, photos, classement des défauts et mesures, tels qu'ils figurent dans le PDF final. |
| ru | Образцы отчетов об инспекции \| BST Inspection | Примеры отчетов BST: выявленные дефекты, фотографии, классификация и измерения в том виде, в каком они входят в итоговый PDF. |
| es | Ejemplos de informes de inspección \| BST Inspection | Consulte informes de ejemplo de BST: hallazgos, fotografías, clasificación de defectos y mediciones tal como aparecen en el PDF final. |
| pt-BR | Exemplos de relatórios de inspeção \| BST Inspection | Veja relatórios de exemplo da BST: constatações, fotos, classificação de defeitos e medições como aparecem no PDF final. |
| ar | نماذج تقارير الفحص \| BST Inspection | اطلع على نماذج من تقارير BST: الملاحظات والصور وتصنيف العيوب والقياسات كما تظهر في ملف PDF النهائي. |

### 7.11 质量链接 `/quality-link/` · `quality-link.md`

| 语言 | title | description |
|---|---|---|
| en | Quality Standards & Testing Resources \| BST Inspection | Standards, testing laboratories and reference material for importers sourcing from Asia. Curated links to AQL tables and product regulations. |
| zh | 质量标准与检测资源 \| BST Inspection | 面向进口商的检验标准、检测机构与法规查询入口，涵盖 AQL 抽样表、主要市场的产品法规与常用第三方实验室。 |
| fr | Normes et ressources qualité \| BST Inspection | Normes, laboratoires et documents de référence pour les importateurs en Asie : tables AQL, réglementations produits et laboratoires tiers. |
| ru | Стандарты и ресурсы качества \| BST Inspection | Стандарты, лаборатории и справочные материалы для импортеров из Азии: таблицы AQL, требования к продукции и независимые лаборатории. |
| es | Normas y recursos de calidad \| BST Inspection | Normas, laboratorios y material de referencia para importadores en Asia: tablas AQL, reglamentos de producto y laboratorios independientes. |
| pt-BR | Normas e recursos de qualidade \| BST Inspection | Normas, laboratórios e material de referência para importadores na Ásia: tabelas AQL, regulamentos de produto e laboratórios independentes. |
| ar | معايير الجودة ومصادرها \| BST Inspection | معايير ومختبرات ومواد مرجعية للمستوردين من آسيا، تشمل جداول AQL ولوائح المنتجات والمختبرات المستقلة. |

### 7.12 服务条款 `/terms/` · `terms.md`

| 语言 | title | description |
|---|---|---|
| en | Terms and Conditions \| BST Inspection | Terms and conditions covering inspection bookings, report delivery, liability and payment for BST quality assurance services. |
| zh | 服务条款 \| BST Inspection | BST 服务条款，涵盖验货预约、报告交付、责任范围与付款安排等事项，适用于全部检验与审核服务。 |
| fr | Conditions générales \| BST Inspection | Conditions générales couvrant la réservation, la remise des rapports, la responsabilité et le paiement des prestations BST. |
| ru | Условия обслуживания \| BST Inspection | Условия оказания услуг BST: заказ инспекций, передача отчетов, ответственность сторон и порядок оплаты. |
| es | Términos y condiciones \| BST Inspection | Términos y condiciones de los servicios BST: reserva de inspecciones, entrega de informes, responsabilidad y condiciones de pago. |
| pt-BR | Termos e condições \| BST Inspection | Termos e condições dos serviços BST: agendamento de inspeções, entrega de relatórios, responsabilidade e condições de pagamento. |
| ar | الشروط والأحكام \| BST Inspection | شروط وأحكام خدمات BST: حجز الفحوصات، وتسليم التقارير، وحدود المسؤولية، وترتيبات الدفع. |

### 7.13 隐私政策 `/privacy/` · `privacy.md`

| 语言 | title | description |
|---|---|---|
| en | Privacy Policy \| BST Inspection | Privacy policy for bstinspection.com: what data BST collects, how enquiry information is used and how long it is retained. |
| zh | 隐私政策 \| BST Inspection | bstinspection.com 的隐私政策，说明 BST 收集哪些信息、询盘数据如何被使用与保存，以及用户的权利与联系方式。 |
| fr | Politique de confidentialité \| BST Inspection | Politique de confidentialité de bstinspection.com : données collectées, usage des demandes de devis, durée de conservation et droits. |
| ru | Политика конфиденциальности \| BST Inspection | Политика конфиденциальности bstinspection.com: какие данные собирает BST, как используются запросы и сколько они хранятся. |
| es | Política de privacidad \| BST Inspection | Política de privacidad de bstinspection.com: qué datos recopila BST, cómo se usan las solicitudes y durante cuánto tiempo se conservan. |
| pt-BR | Política de privacidade \| BST Inspection | Política de privacidade do bstinspection.com: quais dados a BST coleta, como as solicitações são usadas e por quanto tempo são mantidas. |
| ar | سياسة الخصوصية \| BST Inspection | سياسة الخصوصية لموقع bstinspection.com: البيانات التي تجمعها BST، وكيفية استخدام بيانات الاستفسارات ومدة الاحتفاظ بها. |

### 7.14 实施方式

不建议手动逐条粘贴。推荐做法：

1. 把上表整理成 `seo-meta.yml`，结构为 `语言 → 页面 slug → {title, description}`。
2. 用一次性脚本按 `permalink` 匹配，把 `title` 与 `description` 写入各页面的 frontmatter（保留原有字段顺序，只替换 title 值、追加 description）。
3. 构建后逐页核对，确认 91 个页面的 description 互不相同，且与 `page.lang` 一致。
4. 42 篇文章按同一模式处理，标题改写建议另见 P2-3。

---

## 八、执行路线与验收指标

### 8.1 分阶段排期

| 阶段 | 内容 | 工期 | 前置条件 |
|---|---|---|---|
| 第 1 周 | P0-1 sitemap、P0-3 hreflang、P0-4 canonical、P0-6 404 修复 | 3 天 | 无 |
| 第 2 周 | P1-4 GSC/Bing/百度接入并提交 sitemap | 2 天 | 第 1 周完成 |
| 第 2～3 周 | P0-2 + P1-3 的 91 页文案录入，P0-5 首页 title 与 H1 | 5 天 | 第七章矩阵已备 |
| 第 4 周 | P1-1 OG 卡片、P1-2 结构化数据、P2-4 内链与面包屑 | 4 天 | 第 3 周完成 |
| 第 5～6 周 | P2-1 服务页目录与正文扩写、P2-2 首页补强 | 6 天 | 文案矩阵落地 |
| 第 7 周 | P2-3 新闻治理、P2-5 图片与性能、P2-6 配置清理 | 4 天 | 无 |
| 持续 | P3 站外与内容资产 | 长期 | — |

### 8.2 验收指标

技术层（上线后 2 周内）
- `/sitemap.xml` 返回 200，URL 数 ≥ 133，GSC 显示"成功"。
- 91 个页面 description 唯一率 100%，语言与页面一致率 100%。
- hreflang：7 × 7 关系完整，无"缺少返回链接"。
- canonical：100% 页面自引用绝对地址。
- 404 页：状态码 404、含 `noindex`、title 正常。

效果层（3 个月）
- GSC 有效收录页数从当前基线增长到 ≥ 100（91 页 + 42 篇文章的大部分）。
- 品牌词以外的展现量出现连续三个月增长。
- 7 个语言各有至少 5 个词进入前 30。
- 首页与 `/services/` 的 CTR 相对基线提升 20% 以上（描述改写的主要收益点）。

体验层
- 移动端 LCP ≤ 2.5s，CLS ≤ 0.1，INP ≤ 200ms。
- 404 页与多语言切换无死链。

### 8.3 需要先定的两个决策

1. **品牌后缀用 `BST Inspection` 还是 `Guangzhou BST Tech.`**。报告全文按前者设计，理由是域名与用户搜索习惯更匹配；如果品牌层面必须保留公司名，把第七章所有 title 的后缀替换即可，其余结构不变。
2. **首页 H1 是否让位给关键词**。方案 A 是 H1 改为"关键词 + 品牌"，方案 B 是 H1 保留公司名、由副标题承担关键词。方案 A 对排名更有利，方案 B 对品牌一致性更稳妥。

---

## 九、附录：建议代码（仅供实施参考，本次未写入仓库）

### A.1 hreflang 与 canonical

放在 `docs/_includes/head.html` 的 `<title>` 之后：

```liquid
{%- assign lang_prefix = '' -%}
{%- if page.lang and page.lang != 'en' -%}
  {%- assign lang_prefix = '/' | append: page.lang -%}
{%- endif -%}
{%- assign base_path = page.url -%}
{%- if page.lang and page.lang != 'en' -%}
  {%- assign lang_slash = page.lang | prepend: '/' -%}
  {%- assign base_path = page.url | remove_first: lang_slash -%}
{%- endif -%}
<link rel="canonical" href="{{ site.url }}{{ page.url }}">
{%- for l in site.available_langs %}
<link rel="alternate" hreflang="{{ l }}" href="{{ site.url }}{% if l != 'en' %}/{{ l }}{% endif %}{{ base_path }}">
{%- endfor %}
<link rel="alternate" hreflang="x-default" href="{{ site.url }}{{ base_path }}">
```

要点：`base_path` 的算法与 `_includes/header.html:5-9` 保持一致，避免两处逻辑分叉；文章页的 `page.url` 已含语言前缀，同样适用；`x-default` 指向英文版。

### A.2 Organization 与 Service 结构化数据

```liquid
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Guangzhou BST Technology Services Co., Ltd.",
  "alternateName": "BST Inspection",
  "url": "{{ site.url }}{{ lang_prefix }}/",
  "logo": "{{ site.url }}/images/logo_%E9%80%8F%E6%98%8E.webp",
  "image": "{{ site.url }}/images/og-cover.jpg",
  "description": "{{ site.data.i18n[page.lang].footer.about | escape }}",
  "email": "{{ site.data.i18n[page.lang].footer.email }}",
  "telephone": "{{ site.data.i18n[page.lang].footer.phone }}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Room 2803, Building 3, No. 21 Huancun Avenue, Maogang Road",
    "addressLocality": "Guangzhou",
    "addressRegion": "Guangdong",
    "addressCountry": "CN"
  },
  "areaServed": ["CN","VN","IN","BD","TH","MY","KH","LK"],
  "knowsLanguage": ["en","zh","fr","ru","es","pt","ar"]
}
</script>
```

服务页再按 `site.data.i18n[page.lang].services` 循环输出 `Service` 对象，`serviceType` 固定用英文标准名（Factory Audit、Social Compliance Audit、Initial Production Check、In-Process Quality Check、During Production Check、Final Random Inspection、Loading Supervision、Testing Arrangement），`provider` 用 `{"@id": "{{ site.url }}/#organization"}` 关联。

### A.3 description 长度校验脚本

放在仓库外临时运行即可，不需要入库：

```python
import re, pathlib, sys

LIMIT_TITLE, LIMIT_DESC = 60, 155
root = pathlib.Path("docs")
bad = []
for p in root.rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not fm:
        continue
    block = fm.group(1)
    t = re.search(r"^title:\s*[\"']?(.*?)[\"']?$", block, re.M)
    d = re.search(r"^description:\s*[\"']?(.*?)[\"']?$", block, re.M)
    if t and len(t.group(1)) > LIMIT_TITLE:
        bad.append((str(p), "title", len(t.group(1))))
    if d and len(d.group(1)) > LIMIT_DESC:
        bad.append((str(p), "desc", len(d.group(1))))
    if not d:
        bad.append((str(p), "missing description", 0))
for row in bad:
    print(*row)
print("total issues:", len(bad))
```

注意脚本对阿语、俄语按字符计数，与搜索引擎的实际截断宽度不完全等价。字符数只是下限保障，最终以 SERP 预览为准。

### A.4 本次审计未覆盖的内容

- 未做关键词搜索量与竞争度测算。第七章的用词基于行业常见检索习惯与站点现有内容主题，属于方向性判断。落地前建议用关键词工具对每个主词做一次量与难度核对。
- 未做全站外链盘点（需 GSC 或 Ahrefs 类工具）。
- 未做多语言内容质量评估（翻译准确性、阿语排版）。这部分建议由各语言的母语者复核一次，尤其是俄语与阿语的服务名称。

---

报告结束。本次未修改 `docs/` 下任何文件，未执行构建，未产生提交。

