# AuditSpeakStyle

**把资本市场专业文本的具体、平实、紧凑和可追溯，转化为审计人员能直接使用的中文表达。**

版本：**0.2.0｜来源基础纠偏版**。新增内容采用 [MIT](LICENSE)。

公开仓库：[herecythrone/AuditSpeakStyle](https://github.com/herecythrone/AuditSpeakStyle)。下载代码后将 `skills/audit-speak-style` 完整目录用于安装。

本版以已确认的 **A-market-ecm-lawyer-plugin** 中披露表达、文书组织、一致性和防误判材料为主要蓝本，作实质改编，再补充审计身份与场景边界。它不是把律师换成会计师，也不是只有“不要越界”的清单。采用的文件、固定版本和改动理由见 [ATTRIBUTION.md](ATTRIBUTION.md) 与 [逐项改编映射](docs/adaptation-map.md)。

## 用途

起草、润色或审阅底稿记录、会计师说明、监管回复、邮件与微信。先把主体、事项、时间、数字、来源和逻辑写清，再检查事实、程序状态和结论有没有被悄悄改变。已有好文本少改；有依据的判断直接表达；不为了正式而写长句。

不用于单独查数、对账、编程、审计程序设计或准则问答；混合任务只接管写作部分。不执行审计、不代替专业判断、不出具鉴证意见，不自动学习客户材料、写记忆、发布或修改仓库。

## 入口与参考

[SKILL.md](skills/audit-speak-style/SKILL.md)为短入口。参考按需读取，不要求每次加载研究与测试文档：

| 文件 | 内容 |
|---|---|
| [正向写法](skills/audit-speak-style/references/style-principles.md) | 六部分、12条规则：事实替评价、具体风险、清楚口径、逻辑组织、来源和术语等 |
| [审计身份适配](skills/audit-speak-style/references/auditor-boundaries.md) | 主体、执行状态、样本、差异、重要性、外部意见与报告固定表述 |
| [场景写法](skills/audit-speak-style/references/scenarios.md) | 底稿、正式说明、监管回复、工作沟通，以及同一事实的四种载体 |
| [复核方法](skills/audit-speak-style/references/review-method.md) | 逐义比较、段落功能、防误判和具体可读的修改意见 |
| [30组对照案例](skills/audit-speak-style/references/examples.md) | 完整前提、前后文和改进边界，全部为虚构教学案例 |

## 先看一段成文

**虚构教学案例**：2025年末同一范围应收明细表1,240万元、汇总表1,200万元。30万元差异已查明为汇总漏列；财务负责人称另10万元与筛选条件有关，尚未验证。

原稿：“差40万，都是汇总的问题，账没问题。”

正文：
> 2025年12月31日，同一范围的应收明细表与汇总表金额分别为1,240万元和1,200万元，相差40万元。项目组已查明，其中30万元为汇总表漏列一笔期末记录所致；据财务负责人说明，其余10万元差异与汇总表的筛选条件有关，该解释尚待验证。

数值、方向和信息顺序更清楚；已查明的原因直接写，未验证的解释保留来源。不用一句“账没问题”吞掉未决差异。给定事实不支持的结论，另作简短提示，不在正文后靠免责声明补救。

## 安装和调用

项目展示名为AuditSpeakStyle；机器名称及技能目录为audit-speak-style。核心不绑定模型、商业服务或个人路径。

**直接在支持读文件的对话中用**：提供skills/audit-speak-style完整目录的内容，要求先读入口再按需读参考，并给待改文字。仅提供一个本机路径或ZIP名称，不代表对方实际已读文件；这种方式不是宿主自动安装。

**Codex项目级安装**：根据核验日[官方文档](https://developers.openai.com/codex/skills)，将完整技能复制到项目.agents/skills下；仓库的skills目录本身只是交付源。以下PowerShell应在解压项目根目录运行，目标存在则停止：

```powershell
$source = Join-Path (Get-Location) 'skills/audit-speak-style'
$parent = Join-Path (Get-Location) '.agents/skills'
$target = Join-Path $parent 'audit-speak-style'
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) {
    throw '请在AuditSpeakStyle项目根目录运行。'
}
if (Test-Path -LiteralPath $target) {
    throw '目标已存在；先比较差异，不执行覆盖安装。'
}
New-Item -ItemType Directory -Force -Path $parent | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Recurse
```

用户级安装可将$parent改为`Join-Path $HOME '.agents/skills'`；两种位置择一，保留防覆盖检查。安装时必须一起携带PROVENANCE.md及LICENSES。不要覆盖旧audit-writing-cn。多个写作技能重叠时优先显式指定：

```text
$audit-speak-style
请润色下面的审计说明，直接给可用正文；若纠正了实质含义，请另作一句提示。
[提供待改文字与必要的事实前提]
```

仅核对了[Agent Skills格式规范](https://agentskills.io/specification)及Codex官方目录/调用说明；后续已在 Windows 核对安装文件，并在 Codex 新对话中以 Luna、Terra 低推理强度各执行六题显式调用测试；仍发现把拟进行请求写成已完成动作等问题。**未验证自动触发或普遍行为可靠性**，不承诺其他宿主或模型表现一致。见 [小规模测试说明](docs/model-smoke-tests.md)。

## 验证

```bash
python scripts/validate.py
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/validate.py --check-manifest
```

工具仅依赖Python3.10及以上标准库。静态检查覆盖包结构、UTF-8/LF、受限YAML、相对链接、案例字段、规则/来源/测试引用及上游许可字节；不判断每条中文结论是否正确。

[44例行为测试](tests/cases.md)含完整输入、参考答案与硬性失败；[作者逐义自检](tests/author-review.md)不是独立模型测试。可用`python scripts/prepare_eval.py --out local-runs/blind-inputs`导出不含参考答案的请求，**不会调用模型**。案例与教学示例有重叠，不代表未见任务的泛化评估。

实际命令、结果和未验证部分见 [验证报告](docs/validation-report.md)。完整性清单为 [MANIFEST.sha256](MANIFEST.sha256)。

## 来源与许可

上游身份与MIT许可已经确认，完整声明已随技能保留，无需再向原作者申请单独许可。新增内容经项目发起者确认采用 MIT，署名为 herecythrone and AuditSpeakStyle contributors；根 LICENSE 及随安装保留的新增内容许可均已加入。具体状态见 [许可说明](docs/license-decision.md)。不捆绑上游外部docx/pdf/xlsx。

[上游研究](docs/upstream-review.md)记录12个文件的查看范围和固定提交；[官方样本研究](docs/source-research.md)区分成功读取、选读、截图失败与未获取材料，不声称通读完整招股书或穷尽核实准则。公开样本不作为真实项目结论依据，原任务附件、旧版私有快照、客户资料和个人路径不进入本包。

[迁移评估](docs/migration.md)说明旧版的保留、改写和舍弃；[HANDOFF.md](HANDOFF.md)用于本地落盘。原始交接报告保留其当时验证范围；当前公开版的许可和测试范围以本 README、许可说明及小规模测试说明为准。
