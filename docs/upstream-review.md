# 上游研究记录

研究日期：2026-09-22。来源仓库已由项目发起者明确确认。固定提交为 `42b295ffbd9a8d7b07eef11ec653c1d375862d13`，提交时间2026-06-16T10:20:38Z。文件通过GitHub连接器按文件/行区间读取；没有执行整仓克隆、没有通读所有技能、没有取得原始训练语料。

[固定提交](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/commit/42b295ffbd9a8d7b07eef11ec653c1d375862d13)的维护记录描述了基于8份见证意见结果反馈的第四轮迭代。本版把它视作维护者记录的实践线索，不把它当成独立效果证明；没有核定全库的素材数量、提炼轮次或跨模型效果。

下列12个文件分别列出实际查看范围；10个与写作/复核相关，另2个处理依赖和许可。blob SHA来自GitHub返回的文件元数据，只有U12另作了本地字节级Git blob校验。

## U01｜`shared/templates/senior-lawyer-execution-standards.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/senior-lawyer-execution-standards.md)

- Git blob SHA：`59d08a8b4d0c843610a156f5f55577f689dda5f8`。
- 实际查看范围：全文可见。
- 源材料支持的观察：证据追溯、缺口显性化、跨文件一致性与任务边界。
- 本版处理：继承机制；不导入发行障碍判断和法律规则库。

## U02｜`skills/ecm-qc-disclosure-review/references/disclosure-style-checklist.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-qc-disclosure-review/references/disclosure-style-checklist.md)

- Git blob SHA：`e0a66d10cc09c011613899c5763b49aba92c5cbd`。
- 实际查看范围：1—160行，返回至文件末尾。
- 源材料支持的观察：六类披露表达审查：夸大、笼统、模糊、矛盾、缩写、引用。
- 本版处理：作为正向表达骨架；纠正机械禁词、自动认定矛盾、猜全称与未标年份即过时。

## U03｜`skills/ecm-draft-disclosure-review/references/disclosure-style-checklist.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-disclosure-review/references/disclosure-style-checklist.md)

- Git blob SHA：`8ab482947420314c263596463bc86fd03781f3da`。
- 实际查看范围：1—145行，第一至第九节。
- 源材料支持的观察：用具体事实代评价、风险具体化、时间数字与资料一致性。
- 本版处理：保留表达目标；不强制风险数字/概率，不继承默认法律定性。

## U04｜`skills/ecm-draft-opinion-letter/SKILL.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-opinion-letter/SKILL.md)

- Git blob SHA：`1ae96a21e6e36adfc514cd711efaf3770d8b7abc`。
- 实际查看范围：60—215行选读；关注实务加固、Step 2—5及输出契约。
- 源材料支持的观察：来源限定、事实/工作/意见组织、已知特殊事项保留。
- 本版处理：改为审计写作；删除清单到完成记录、风险等级到意见的自动映射。

## U05｜`shared/templates/legal-opinion-format.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/legal-opinion-format.md)

- Git blob SHA：`cf5607e79abfa9ed3df4481543fb7ae575e16c2f`。
- 实际查看范围：70—225行，第三至第八节相关内容。
- 源材料支持的观察：按职能组织正文；条件和例外的写法。
- 本版处理：不搬五段固定骨架、统一本所、法律结论、签字承诺。

## U06｜`shared/templates/work-report-format.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/work-report-format.md)

- Git blob SHA：`6e351c60256127a77312fbb0f54dae50c8899460`。
- 实际查看范围：50—335行选读；返回到文件末尾。
- 源材料支持的观察：来源、发现、工作、判断分开；交叉引用与语言表达。
- 本版处理：保留功能和定位方法；不移植版式和“主观词替换为经核查”。

## U07｜`shared/templates/legal-memo-format.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/shared/templates/legal-memo-format.md)

- Git blob SHA：`f105bbbcba8354da9b7b32fc0644105325e2d8f4`。
- 实际查看范围：第一至第八节及第九节开头可见；返回尾部截断。
- 源材料支持的观察：文种区别、首次释义、金额分子分母、单位期间、避免假精度。
- 本版处理：保留数字与引用方法；字体、法条编号和免责声明模板不作通用强制。

## U08｜`skills/ecm-qc-shareholders-meeting-witness/references/anti-misjudgment.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-qc-shareholders-meeting-witness/references/anti-misjudgment.md)

- Git blob SHA：`8e62a998639bb35babb34750eb857623cfee88d8`。
- 实际查看范围：第一部分、第二部分可见内容与第三部分全文；分段读取1—165、165—310行。
- 源材料支持的观察：段落职能防误删、自动编号不可凭纯文本、术语精确、批注可读性和相关性。
- 本版处理：将防误判机制改编为审计复核方法；不移植律师业务结论或Word脚本。

## U09｜`skills/ecm-draft-opinion-letter/references/consistency-checklist.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-opinion-letter/references/consistency-checklist.md)

- Git blob SHA：`f4d2abe096131fea8e89dd85b0ad6edf437ae829`。
- 实际查看范围：1—155行；七层校验及常见不一致。
- 源材料支持的观察：元信息、范围、释义、结论与已知问题对应。
- 本版处理：不一律强制不同文书日期相同，不自动选工作报告日期，不按风险色生成意见。

## U10｜`skills/ecm-draft-report-assembly/references/editorial-basis-template.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/skills/ecm-draft-report-assembly/references/editorial-basis-template.md)

- Git blob SHA：`ef59dc94a9a9e7a365530c286bc3c6b94df1af40`。
- 实际查看范围：1—200行，返回至文件末尾。
- 源材料支持的观察：概况、身份、编制基础与使用范围分开；计划和条件表达。
- 本版处理：只提取组织方法；不复制律师资质、审批清单、签字、使用授权及未来出具承诺。

## U11｜`docs/dependencies.md`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/docs/dependencies.md)

- Git blob SHA：`1fba098e7c965e626c87c66c170ddb63b021eb2b`。
- 实际查看范围：1—110行，返回至文件末尾。
- 源材料支持的观察：上游说明外部通用Skill另有许可、不随仓库分发。
- 本版处理：仅用于确定不捆绑外部依赖；未另行穷尽核验其描述的产品能力和第三方许可。

## U12｜`LICENSE`

[固定版本文件](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/blob/42b295ffbd9a8d7b07eef11ec653c1d375862d13/LICENSE)

- Git blob SHA：`fdb09f36c442491f6c69832c67ff09260ecde213`。
- 实际查看范围：完整文本；本地复制字节另行校验Git blob SHA。
- 源材料支持的观察：MIT完整许可、版权和原附加声明。
- 本版处理：原样随技能分发；不据此决定新增内容许可证。


## 阅读范围与限制

仓库主版本说明与某个技能的版本号不是同一层面；本版以提交哈希锁定来源，不用“最新版”“成熟版”代替版本定位。没有把未读字段填成已读；选读和截断范围明确列出。

U11描述的外部产品命令和许可限制未作独立全面法律核查，本次不采用其安装命令、不分发这些依赖，因此不依赖该描述对外作许可承诺。

原始客户材料、上游真实业务示例及个人联系方式未复制进教学案例。上述公开源文件包含的机构/业务名称仅保留在外部链接中，不作为本包业务事实。对来源中的所有法律结论，本次未进行逐条有效性认证。
