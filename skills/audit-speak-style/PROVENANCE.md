# 来源、改编与许可（随技能保留）

AuditSpeakStyle 0.2.0 的表达与复核内核实质改编自 **zeweihan/A-market-ecm-lawyer-plugin**，而非仅参考项目名或README。固定提交：`42b295ffbd9a8d7b07eef11ec653c1d375862d13`（2026-06-16）。改编包括披露表达分类、正文功能分离、数字口径、一致性及防误判；目标改为审计写作，不继承法律业务结论。

上游版权：**Copyright (c) 2026 zeweihan and A-market-ecm-lawyer-plugin contributors**。上游采用MIT；完整原许可及其附加声明原样保存在 [LICENSES/A-market-ecm-lawyer-plugin.txt](LICENSES/A-market-ecm-lawyer-plugin.txt)。复制本技能时保留本说明与许可文件。上游许可文本内提及的DISCLAIMER.md指[上游文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/DISCLAIMER.md)，不是要求本技能具有同名本地文件。

新增内容采用 MIT，版权署名为 **Copyright (c) 2026 herecythrone and AuditSpeakStyle contributors**。完整许可见 [LICENSES/AuditSpeakStyle.txt](LICENSES/AuditSpeakStyle.txt)。上游版权、完整许可及附加声明独立保留，复制和分发时须一并携带。

## 具体采用的源文件与落点

| 来源 | 固定版本 | 主要改编落点 |
|---|---|---|
| U01 | [`shared/templates/senior-lawyer-execution-standards.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/senior-lawyer-execution-standards.md) | S08、S11；B边界 |
| U02 | [`skills/ecm-qc-disclosure-review/references/disclosure-style-checklist.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-qc-disclosure-review/references/disclosure-style-checklist.md) | S01、S04、S05、S09—S11 |
| U03 | [`skills/ecm-draft-disclosure-review/references/disclosure-style-checklist.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-disclosure-review/references/disclosure-style-checklist.md) | S01、S03—S05、S11 |
| U04 | [`skills/ecm-draft-opinion-letter/SKILL.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-opinion-letter/SKILL.md) | S07、S08；B02、B05、B08 |
| U05 | [`shared/templates/legal-opinion-format.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/legal-opinion-format.md) | S07；B01、B06 |
| U06 | [`shared/templates/work-report-format.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/work-report-format.md) | S10、S12；B02 |
| U07 | [`shared/templates/legal-memo-format.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/legal-memo-format.md) | S03、S09、S10 |
| U08 | [`skills/ecm-qc-shareholders-meeting-witness/references/anti-misjudgment.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-qc-shareholders-meeting-witness/references/anti-misjudgment.md) | S12；R01—R04 |
| U09 | [`skills/ecm-draft-opinion-letter/references/consistency-checklist.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-opinion-letter/references/consistency-checklist.md) | S09、S11；R04 |
| U10 | [`skills/ecm-draft-report-assembly/references/editorial-basis-template.md`](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-report-assembly/references/editorial-basis-template.md) | S07；场景写法、B09 |

## 继承方式与明确纠正

S规则位于 [style-principles.md](references/style-principles.md)，B规则位于 [auditor-boundaries.md](references/auditor-boundaries.md)，R规则位于 [review-method.md](references/review-method.md)。这些编号是本版编排，不是上游编号。

继承的是具体写作与防误判方法，而不是原库全部文字。对强制风险量化、机械禁用合理/可能、凭简称猜全称、未标年份即过时、核查清单写成完成、风险标签映射结论、格式不合格即丢问题、日期一律对齐等规则，均作了明确纠正。法律模板的本所称谓、合法有效结论、签字身份和承诺没有移植。

样本范围、差异与错报、重要性、已/拟状态、正式报告固定表述和内外沟通是审计适配补充；句段连接及全部虚构教学例为本版编写或从前版自检后保留。不是声称这些内容全部出自上游，也不是根据少量样本证明规则普遍有效。

官方公开披露和专业文件仅校准语言与边界，不作为任何真实项目事实或结论依据；无PDF、商业材料或客户资料随技能分发。不捆绑上游外部docx/pdf/xlsx，不依赖其模型或商业服务。完整研究、逐条映射和验证在仓库文档中，日常写作不必加载。
