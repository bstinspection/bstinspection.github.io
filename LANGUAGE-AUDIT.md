# BST Inspection 多语言文案审查报告

**审查日期**：2026-10-31
**范围**：13 个页面 × 7 种语言（91 个文件）、7 篇新闻 × 7 种语言（49 个文件）、共用 UI 文案 `docs/_data/i18n.yml`
**依据**：[AGENTS.md](AGENTS.md)（7 语言同步、中文文风基准）、[humanizer-zh](C:/Users/AFewMoon/Documents/Projects/SKILLs/Humanizer-zh/SKILL.md)（去 AI 味）、《BST Inspection 全站 7 语言文案审查与修复计划》

---

## 一、审查方法与口径

三条判定标准：

1. **地道**：按目标语言的商业写作习惯重写，不做英文逐句直译；技术术语使用行业通用译法。
2. **统一**：同一概念全站一个词；同一事实 7 种语言一个数字；同一服务名在菜单、标题、卡片、条款、结构化数据中逐字相同。
3. **专业不死板**：保留商业书面语的克制与信息密度，删除模板句、空泛修饰、为对称而对称的排比、粗体伪标题。

执行方式：先由英文与中文版本确定事实与术语契约，再按语言分域（zh / fr / ru / es / pt-BR / ar）逐文件审查修改，最后做结构、术语、链接、编码与数字的自动化复核。本机未安装 Ruby/Jekyll，未做本地构建；本次不改模板与 Liquid，构建风险受控。

---

## 二、结论摘要

| 语言 | 主要问题 | 处理结果 | 结论 |
|---|---|---|---|
| EN | 语法与搭配错误、服务页模板句、预约承诺自相矛盾、英式/美式拼写混用 | 全部修正；服务页重写；统一美式拼写 | 结构基准已可用；作为 7 语言的语义源 |
| ZH | 「品质保证/质量保证」「人工天/人天」「孟加拉/孟加拉国」漂移；服务页模板句；翻译腔 | 全部统一；服务页去模板化；按 humanizer-zh 清理 | 术语与语气已收敛 |
| FR | `portée de production`、`témoignage des équipements`、`homme-jour` 等误译；IPQC 与 DUPRO 同名 | 全部改正；服务名与导航一致 | 误译已清除 |
| RU | `Объем производства`（产量）误作「生产范围」；文书化直译；条款中残留中文「保留」 | 全部改正；服务名与导航一致 | 语义错误已清除 |
| ES | `No aseguramos nuevos negocios` 语义错；TA 名称不统一；Title Case | 全部改正；标题 sentence case | 用词与大小写已统一 |
| PT | `Providência de testes`、未译 `swabs`、`testemunha de equipamentos`、`encargos` | 全部改正 | 机翻残留已清除 |
| AR | `توسّع نطاقها` 及物性错误、`محورًا` 悬挂、`تبقى…الجزء الأكبر`、`تفتيش/فحص` 混用 | 全部改正；inspection 统一 `فحص` | 语法与术语已统一 |

**总体判断**：全站事实口径已统一，服务名与术语已契约化，服务页的模板化行文已清除；七种语言均按本地商业书面语重写，未出现口语化或「贴吧体」。仍未解决的是三类需要业务/法务拍板的事项（见第七节），代码与文案层面没有阻塞项。

---

## 三、事实与术语契约（唯一来源）

### 3.1 对外事实

| 项目 | 统一口径 |
|---|---|
| 公司名 | Guangzhou BST Technology Services Co., Ltd. / 广州睿翔技术服务有限公司 |
| 联系人 | Jeffrey Zeng（中文页：曾勇俊（Jeffrey Zeng）） |
| 邮箱 | jeffrey@bstinspection.com（`info@` 已全站停用） |
| 地址 | 中文页：中国广东省广州市黄埔区茅岗路环村大街21号3栋2803房；其他语言：Room 2803, Building 3, No. 21 Huancun Avenue, Maogang Road, Huangpu District, Guangzhou, Guangdong, China |
| 价格 | 验货 198 美元/人天；工厂审核 258 美元/人天；差旅、住宿按实报销 |
| 预约 | 收到委托后 24 小时内初步答复并展开磋商，争取 3 天内基本确定订单；检验日期一般需提前 3 个工作日预约，紧急订单视排期安排 |
| 覆盖 | 8 国，固定顺序：中国、越南、印度、孟加拉国、泰国、马来西亚、柬埔寨、斯里兰卡 |

### 3.2 服务名唯一表

| 缩写 | EN | ZH | FR | RU | ES | PT-BR | AR |
|---|---|---|---|---|---|---|---|
| FA | Factory Audit | 工厂审核 | Audit d'usine | Аудит фабрики | Auditoría de fábrica | Auditoria de fábrica | تدقيق المصنع |
| SCA | Social Compliance Audit | 社会责任审核 | Audit de conformité sociale | Аудит социального соответствия | Auditoría de cumplimiento social | Auditoria de conformidade social | تدقيق الامتثال الاجتماعي |
| IPC | Initial Production Check | 初期生产检查 | Contrôle de production initiale | Проверка начальной продукции | Control de producción inicial | Verificação de produção inicial | فحص الإنتاج الأولي |
| IPQC | In-Process Quality Check | 过程质量控制 | Contrôle qualité en cours de fabrication | Контроль качества в процессе производства | Control de calidad en proceso | Controle de qualidade em processo | فحص الجودة أثناء العملية |
| DUPRO | During Production Check | 生产中期检查 | Contrôle en cours de production | Контроль во время производства | Control durante la producción | Verificação durante a produção | الفحص أثناء الإنتاج |
| FRI | Final Random Inspection | 最终随机抽样检验 | Inspection finale aléatoire | Финальная случайная инспекция | Inspección final aleatoria | Inspeção final aleatória | الفحص العشوائي النهائي |
| L/S | Loading Supervision | 装柜监督 | Supervision du chargement | Наблюдение за погрузкой | Supervisión de carga | Supervisão de carregamento | الإشراف على التحميل |
| TA | Testing Arrangement | 测试安排 | Organisation des tests | Организация испытаний | Organización de pruebas | Organização de testes | ترتيبات الاختبار |

### 3.3 术语

- 质量保证：zh 质量保证 / en quality assurance / fr assurance qualité / ru обеспечение качества / es aseguramiento de calidad / pt garantia da qualidade / ar ضمان الجودة。
- 人天·人时：zh 人天·人时 / en man-day·man-hour / fr jour-homme·heure-homme / ru человеко-день·человеко-час / es día-hombre·hora-hombre / pt dia-homem·hora-homem / ar يوم عمل للفرد·ساعة عمل للفرد。
- 阿语：inspection 统一 `فحص`，audit 统一 `تدقيق`；不再用 `تفتيش` 表示 inspection。

---

## 四、P0 问题台账（事实矛盾与明显错误）

| # | 位置 | 改前 | 改后 |
|---|---|---|---|
| 1 | 下单页 × 7 / 服务条款 × 7 | 「最短 24 小时通知即可验货」与条款「提前 3 个工作日」并存 | 统一为「24 小时内初步答复、争取 3 天内定单；检验日期提前 3 个工作日」 |
| 2 | 下单页、参考报告 × 7 | `info@bstinspection.com`（28 处） | `jeffrey@bstinspection.com` |
| 3 | 联系我们 × 7 | Jeffrey Tsang / 曾勇俊 / 微信号 JeffreyZengBST 三种写法 | 统一 Jeffrey Zeng（中文页曾勇俊（Jeffrey Zeng）） |
| 4 | 中文隐私政策 | 地址缺「环村大街」、房号写作「室」 | 补全「环村大街」并统一「2803 房」 |
| 5 | 中文联系页 | description「黄浦区」 | 「黄埔区」 |
| 6 | 中文定价页 | description 多出「批量订单另有优惠，欢迎来函索取报价单」 | 删除，与正文「不以不可持续折扣争取新业务」一致 |
| 7 | 参考报告 × 7 | 标题/描述称可「下载」，正文为「按需提供」 | 统一为按需提供（PDF 样本） |
| 8 | EN 质量标准 | `quality insurance services`；`What is critical defects` | `quality assurance services`；`What are critical, major and minor defects?` |
| 9 | EN 下单页 | `1. First: Submit inspection application form.`；`Customer require or specification` | `1. Submit the booking form`；`Customer requirements or specifications` |
| 10 | EN 服务条款 | `prevail any purchase terms`；`consist in…communicating`；`palette of quality tools`；`That BST can start claim investigations` | `prevail over…`；`setting out the information…`；`a set of quality tools`；`so that BST can open a claim investigation` |
| 11 | EN 服务页 | `an calculation chart`；`machineries and equipment tools` | `a capacity calculation table`；`machinery and equipment` |
| 12 | 服务名 × 5 语言 | 菜单名与落地标题不一致；FR 的 IPQC 与 DUPRO 都叫 `en cours de production` | 以 3.2 唯一表为准，8×7 一次对齐 |
| 13 | RU / ES / PT | `Объем производства`（产量）；`No aseguramos nuevos negocios`；`Providência de testes` | `Сфера производства`；`No conseguimos nuevos negocios`；`Organização de testes` |
| 14 | 2026-10-17 文章 × 7 | 英文 `Three Lines of Work` 与中文「三大品类」语义不一致 | 英文改 `Three Product Categories` |
| 15 | 2021 合并文章（EN） | 用 `**粗体**` 充当小标题，其余 6 语言用 `##` | 改为 `##`，结构对齐 |
| 16 | 中文术语 | 品质保证 8 处、人工天 16 处、孟加拉 10 处 | 质量保证 / 人天 / 孟加拉国 |
| 17 | AR 2026-10-17 / 2025-11-10 | `توسّع BST نطاقها`、`محورًا لخمس سنوات`、`تبقى…الجزء الأكبر` | `وسّعت BST نطاقها`、`محور السنوات الخمس المقبلة`、`لا تزال…تمثل الجزء الأكبر` |
| 18 | PT / FR 文章 | 未译 `swabs`；`testemunha de equipamentos`；`assumir esses encargos`；`portée de production`；`témoignage des équipements` | `cotonetes`；`acompanhamento de equipamentos`；`assumir essas demandas`；`périmètre de production`；`surveillance des essais` |
| 19 | EN 2026-07-21 文章 | `with improved navigation, working on desktop…` | `with improved navigation that works on desktop, tablet and mobile` |
| 20 | RU 服务条款 | 残留中文「保留」等未翻译词 | 改为俄文并重写句子 |

---

## 五、P1：地道性与语气

### 5.1 服务页去模板化（7 语言 × 11 处）

改前（各语言同一模式）：

- EN `This section includes an assessment of the internal Quality Processes…`
- ZH `本节包括对内部质量流程……的评估。`
- FR `Cette section comprend une évaluation des processus qualité internes…`
- RU `Этот раздел включает оценку внутренних процессов контроля качества…`
- ES `Esta sección incluye una evaluación de los procesos de calidad internos…`
- PT `Esta seção inclui uma avaliação dos processos internos de qualidade…`
- AR `يتضمن هذا القسم تقييمًا للعمليات الداخلية للجودة…`

改后：删除「本节包括 / This section includes」框架，直接陈述检查内容（如 `Internal quality processes, QC facilities, quality team, records and quality certificates.`），并合并与新导语重复的旧段落；标准号、比例、时限等技术事实全部保留。

同时统一了服务页结构：每个服务 = H2 + 2–4 句导语 + `What the audit covers` / `What the check covers` / `Key check points` + `When to book`；7 种语言均为 9 H2 / 14 H3 / 11 H4。

### 5.2 承诺与营销语收敛

- `why.speed_desc`：由「24 小时内安排验货」改为「24 小时内答复」，与下单页、条款口径一致。
- `why.subtitle`：由「We deliver exceptional value through expertise, speed, and global reach.」等抽象句改为具体能力描述。
- `why.cost_desc`：由「Cost-effective solutions starting at USD 198…」改为「Inspection from USD 198 per man-day, with no reduction in service standards.」
- `cta.title`：由「Ready to Ensure Your Product Quality?」改为「Ready to book an inspection?」（各语言同步）。
- 中文清理「我们的客户承诺」「本地化优势：验货员都是当地母语人士」「其加入」「一个品质保证合作伙伴即可覆盖…」等翻译腔。

### 5.3 中文去 AI 味（humanizer-zh）

- 删除空泛总结与三段式排比；拆开连续同构短句；减少破折号；法律页仅改语法与清晰度。
- 保留商业宣传的书面冗余，未口语化。
- 自评：直接性 8 / 节奏 8 / 信任度 8 / 真实性 7 / 精炼度 8，合计 39/50（良好）。

---

## 六、P2：细节与格式

- 统一英文为美式拼写（labor / color / traveling / authorized / specialization / willful）。
- ES/PT 标题改为 sentence case；EN 旧小标题同步 sentence case。
- 修正 AQL 表分隔行（原 9 段对应 8 列）为 8 段；本地化表头与区间。
- 28 个文件补齐末尾换行；全部文件统一 CRLF、UTF-8 无 BOM。
- 修正 ES/PT/AR 的 `%` 与数字间距（如 `20 %`、`20٪`），保留原数值。
- 修正 RU 条款中的中文残留、PT 的 `Taxa de Reinsp eção` 等错字。

---

## 七、未决事项（未改动，需业务/法务确认）

1. **服务条款责任倍数**：第 3 节表格写「服务费的 3 倍，特殊情况下最高 10 倍」，第 6.1/6.2.1 条写「最高 10 倍」。七种语言均保留原文，未统一。建议法务确认后统一表述。
2. **预订表格下载**：`/BST booking form.doc` 在仓库中不存在，链接可能 404。建议补入文件或改为「来函索取」。
3. **Quality Links 页的 meta 描述**：描述承诺「AQL 抽样表、第三方实验室」，页面实际只有 4 条标准/监管机构链接。为避免影响 SEO，本次未改描述；建议后续补内容或调整描述。
4. **文章文件名**：`...-vietnam-and-bangladesh-inspection-services(.md/-es.md)` 与其余语言的 `-<lang>.md` 命名不一致。URL 由 permalink 决定，本次未改名。
5. **页脚品牌名**：`site.title = Guangzhou BST Tech.` 在七种语言页面均显示英文，未改（品牌决策）。
6. **「报告以英文出具」「验货员均为当地母语人士」**：前者已按未确认删除，后者已软化为「本地验货员熟悉当地制造实践与法规」；如业务确认，可恢复更具体表述。
7. **本地构建**：本机无 Ruby/Bundler/Jekyll，未执行 `bundle exec jekyll serve`；Liquid 令牌与 HEAD 完全一致，仍建议部署前在 GitHub Pages 或具备 Ruby 的环境预览一次。
8. **人工复核**：本次为 AI 编辑 + 自动化校验，建议阿拉伯语与法律页面由母语/法务人员做一次抽读。

---

## 八、验证结果

自动校验（本次执行，0 项残留）：

| 检查项 | 结果 |
|---|---|
| `i18n.yml` 7 分区 key 集合 | 每区 74 key，完全一致 |
| 服务名：i18n 与 services 页 H2（8×7） | 全部逐字相等 |
| 页面标题结构（9 H2 / 14 H3 / 11 H4，另页按 EN） | 7 语言一致 |
| 显式锚点 `{#fa…ci}` | 完整未改 |
| Liquid `{{ }}` / `{% %}` 令牌数 | 与 HEAD 全等 |
| frontmatter 字段集合 | 本地化页面按设计省略 `permalink`/`nav_order`，其余一致 |
| 站内链接目标 | 0 处失效（预订表格 .doc 资源缺失另列） |
| 术语黑名单（品质保证/人工天/孟加拉/info@/quality insurance/تفتيش/DQC 等） | 0 处 |
| 法律页与定价页数字 | 与 HEAD 一致（RU 条款仅「1」改写为「один」） |
| 编码与行尾 | 无 BOM，CRLF，全部有末尾换行 |
| 国家枚举顺序 | 7 语言均为契约固定顺序 |
| 预约口径 | 7 语言下单页均为 24 小时答复 / 3 天定单 / 3 个工作日预约 |

**改动规模**：134 个内容文件（91 页 + 49 文 + i18n；未改动的 6 页为纯 Liquid 或无需修改的页面），约 1,270 行新增、1,417 行删除；另更新 `README.md` 并新增本报告。

---

## 九、复核方法（可复用）

本次校验用临时 Python 脚本完成，未提交入库。维护时可按下述项抽查：

1. **i18n key 对齐**：解析 `docs/_data/i18n.yml`，比较 7 个语言分区的扁平 key 集合，应完全相等（当前 74 个）。
2. **服务名一致**：取 `i18n.yml` 的 `services` 8 项，与 `docs/*/services.md` 的 `## N. 名称 (XX)` 逐字比较。
3. **结构对齐**：统计各页 `##`/`###`/`####` 数量，7 语言应一致（services 为 9/14/11）。
4. **Liquid 未动**：`git show HEAD:<file>` 与工作区文件的 `{{`、`}}`、`{%`、`%}` 计数应相等。
5. **术语黑名单**：`品质保证`、`人工天`、`人工小时`、`孟加拉(?!国)`、`info@bstinspection.com`、`Jeffrey Tsang`、`quality insurance`、`This section`、`Cette section`、`Этот раздел`、`Esta sección`、`Esta seção`、`يتضمن هذا القسم`、`تفتيش`、`DQC` 均应为 0。
6. **编码**：UTF-8 无 BOM、CRLF、末尾有换行。
7. **数字不变**：对 `terms.md`、`privacy.md`、`pricing.md` 提取数字 token 与 HEAD 比较（允许数字写作文字，如「1」→「один」）。
8. **口径短语**：7 语言下单页应含「24 小时答复 / 3 天定单 / 3 个工作日预约」对应表述；`i18n.yml` 与页面不得再出现「24 小时即可上门验货」。

---

## 十、附：本次未改动的页面

`docs/index.md`、`docs/news.md`、`docs/{es,pt-BR,ru,fr,ar}/index.md`、`docs/{es,fr,ru,ar}/news.md`、`docs/{zh,es,ru}/quality-link.md`、`docs/ar/production-scope.md`、`docs/zh/quality-link.md` 等：正文为纯 Liquid 或经通读无口径/文风问题；仅补齐了末尾换行。`docs/404.html`、`_layouts`、`_includes`、`_config.yml`、图片与脚本未改动。
