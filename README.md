[//]: # "Academic Paper Writing Skill is an evidence-first Agent Skill for research ideation, academic search, literature review, statistics, scientific writing, peer review, rebuttals, theses, and paper-to-presentation workflows."

<div align="center">

<p>
  <img src="./assets/hero.png" alt="Academic Paper Writing Skill research workflow" width="860">
</p>

# Academic Paper Writing Skill

**把科研从一次性生成，变成可追溯、可检查、可交付的工作流。**<br>
面向 Codex、Claude Code 和兼容 Agent Skills 的智能体，覆盖选题、检索、综述、研究设计、统计、绘图、写作、审稿、投稿与论文汇报。

<p>
  <a href="https://github.com/xcl2005/academic-paper-writing-skill/stargazers"><img src="https://img.shields.io/github/stars/xcl2005/academic-paper-writing-skill?style=flat-square&color=F2B134" alt="GitHub stars"></a>
  <a href="https://github.com/xcl2005/academic-paper-writing-skill/releases"><img src="https://img.shields.io/github/v/release/xcl2005/academic-paper-writing-skill?style=flat-square&color=167D9A" alt="Latest release"></a>
  <a href="https://github.com/xcl2005/academic-paper-writing-skill/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/xcl2005/academic-paper-writing-skill/ci.yml?branch=main&style=flat-square" alt="CI status"></a>
  <a href="https://github.com/xcl2005/academic-paper-writing-skill/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-2F6F5E?style=flat-square" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Agent%20Skills-Codex%20%7C%20Claude-24292F?style=flat-square" alt="Codex and Claude Code Agent Skill">
</p>

**简体中文** · [English](README_EN.md)

[快速开始](#-快速开始) · [核心能力](#-核心能力) · [Skill 一览](#-专业-skill-一览) · [工作方式](#-一次典型任务) · [证据优先](#-证据优先) · [示例](#-模板与示例)

<sub>如果它让你的研究工作更可靠，欢迎点一个 Star，让更多研究者找到它。</sub>

</div>

## 为什么值得使用

大模型很容易写出流畅段落，真正困难的是让每个结论经得起追问：文献是否真实、检索是否充分、实验是否真的完成、统计是否匹配设计、图表是否能追溯到数据、投稿材料是否彼此一致。

**Academic Paper Writing Skill** 不把“生成一篇论文”当成单次写作任务。它会根据你当前的研究阶段组织证据、记录未知项、调用合适的专业能力，并在进入正文或交付前检查关键产物。

| 你现在有什么 | 可以直接交给它的任务 | 你会得到什么 |
|---|---|---|
| 一个模糊方向 | 生成候选问题、可证伪预测、最小研究与风险比较 | 选题组合、决策记录、检索计划 |
| 一批论文或关键词 | 建立检索协议、筛选记录、精读笔记与证据综合 | 文献矩阵、研究空白、引用边界 |
| 数据、实验设想或已有结果 | 明确 estimand、样本、模型、诊断和敏感性分析 | 研究设计、统计分析计划、实验矩阵 |
| 草稿、图表或审稿意见 | 核验 claim、修订表达、模拟审稿并逐条回应 | 可追溯稿件、图表 brief、rebuttal matrix |
| 一篇接近完成的论文 | 检查投稿包并提炼成组会、答辩或会议汇报 | submission checklist、presentation brief、PPT 交付要求 |

## 🚀 快速开始

### 1. 安装到 Codex

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git \
  ~/.agents/skills/academic-paper-writing-skill
```

<details>
<summary><b>Windows PowerShell</b></summary>

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
git clone https://github.com/xcl2005/academic-paper-writing-skill.git `
  "$HOME\.agents\skills\academic-paper-writing-skill"
```

</details>

### 2. 直接描述研究任务

```text
使用 $academic-paper-writing-skill 帮我把“面向科研问答的 RAG 评测”发展成一篇可执行的研究计划。
先给出候选问题和检索方案，区分已核验事实、论文原文主张与推断；不要编造引用或实验结果。
```

不需要记住内部模块或固定命令。你可以从选题、已有论文、数据、草稿、审稿意见或学校要求中的任意位置开始。

<details>
<summary><b>安装到 Claude Code</b></summary>

用户级安装：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git \
  ~/.claude/skills/academic-paper-writing-skill
```

项目级安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git \
  .claude/skills/academic-paper-writing-skill
```

调用示例：

```text
/academic-paper-writing-skill 审计这篇论文，并把每条主要问题映射到证据、修改位置和待办动作。
```

</details>

## 🧭 一次典型任务

假设你提出：

```text
我想研究多语言 RAG 的引用可靠性。请帮我完成选题收敛、文献综述、实验设计和论文框架；
目前没有实验结果，所有未核验文献都要明确标记。
```

Skill 不会立刻拼出一篇看似完整的论文。它会按当前证据和目标选择必要能力，并留下可检查的中间产物：

| 阶段 | 它会做什么 | 可检查输出 |
|---|---|---|
| 界定问题 | 澄清研究对象、范围、假设、未知项和停止条件 | idea portfolio、project state、decision log |
| 建立证据 | 保存精确查询式、来源、筛选理由、论文 claim 和局限 | search protocol、screening log、literature matrix |
| 设计研究 | 明确单位、estimand、对照、偏差、样本、指标与分析计划 | study design、analysis plan、experiment matrix |
| 组织表达 | 把段落、图表和结论连接到来源、数据或分析 | claim ledger、figure brief、terminology ledger |
| 审查交付 | 执行阶段门禁、模拟审稿、投稿包或汇报渲染检查 | integrity report、rebuttal matrix、submission package |

流程会随任务变化。只做综述时不会强行进入实验；只有审稿意见时也不会重新跑完整选题流程。

## 🧩 核心能力

| | 能力 | 质量标准 |
|---|---|---|
| 💡 | **选题与科研头脑风暴** | 独立生成候选问题，记录假设、可证伪预测、最小研究、风险与选择理由 |
| 🔎 | **学术检索与引用管理** | 保存数据库、查询式、日期、限制、失败和去重记录；优先核验 primary sources |
| 📚 | **论文精读与文献综述** | 区分 narrative、rapid、scoping 与 systematic review，保留筛选和质量评估边界 |
| 🧪 | **研究设计与统计分析** | 明确观察、分配和分析单位，报告效应量、区间、假设、诊断、多重比较与缺失数据 |
| 📊 | **科研绘图与数据追溯** | 先定义 figure claim 和最终尺寸，再检查色盲可读性、源数据、可编辑文件与导出效果 |
| ✍️ | **论文写作、润色与翻译** | 保护数字、公式、引用、术语和 claim 强度，按目标期刊或报告规范组织文本 |
| 🧐 | **模拟审稿与逐条回复** | 分离 reviewer assessment 与 author response，为每个问题建立稳定 ID 和证据指针 |
| 📦 | **投稿、数据声明与论文汇报** | 核对 manuscript、supplement、references、data/code、portal preview，并支持 paper-to-PPT |

## 🛡️ 证据优先

这个 skill 的重点不是让文字更像论文，而是让研究记录足以支撑文字。

- **来源可追溯**：区分已核验事实、论文作者的主张、agent 推断、假设和用户提供的信息。
- **强结论有依据**：novelty、SOTA、因果、效果和合规性结论必须连接到来源、数据、分析、实验或官方要求。
- **研究状态不混淆**：planned、exploratory、preliminary、achieved 和 externally reported results 分开记录。
- **不完整就明确阻断**：缺少来源、证据冲突、关键表格为空或状态未确认时，降调、保留占位或停止最终 prose。
- **人类保留最终决定**：投稿、署名、伦理、consent、受限数据、学校合规和最终结论需要人工确认。

> [!IMPORTANT]
> 本项目不会替你编造论文、DOI、SOTA、实验结果、数据仓库、学校要求或审稿回复中的完成事项。它也不替代研究者、导师、统计师、伦理委员会或期刊编辑的专业判断。

## 🌐 专业 Skill 一览

**18 个可选 Skill，来自 3 个开源仓库。** 每个 Skill 对应明确的科研板块，点击名称可查看它的完整说明；名称下方是来源仓库。

> Star 是**来源仓库**的动态热度，不是单个 Skill 的独立 Star，也不代表已全部安装。这里展示的是已配置的可选 provider 接口。

### 选题、检索与综述

| 板块 | Skill / 来源 | 标签 | 仓库 Stars |
|---|---|---|---|
| 统筹 | [academic-research-suite](https://github.com/Imbad0202/academic-research-skills-codex/blob/main/skills/academic-research-suite/SKILL.md)<br><sub>[Academic Research Suite](https://github.com/Imbad0202/academic-research-skills-codex)</sub> | 阶段管理 · 项目编排 | [![GitHub stars](https://img.shields.io/github/stars/Imbad0202/academic-research-skills-codex?style=flat-square&label=stars)](https://github.com/Imbad0202/academic-research-skills-codex/stargazers) |
| 选题 | [scientific-brainstorming](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-brainstorming/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | 假设 · 反方评估 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |
| 检索 | [nature-academic-search](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-academic-search/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 多源检索 · 引用核验 | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |
| 检索 | [paper-lookup](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/paper-lookup/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | DOI · 开放获取 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |
| 综述 | [literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | 系统综述 · PRISMA | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |

### 研究设计、统计与绘图

| 板块 | Skill / 来源 | 标签 | 仓库 Stars |
|---|---|---|---|
| 设计 | [experimental-design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | 对照 · 随机化 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |
| 统计 | [statistical-analysis](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/statistical-analysis/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | 模型 · 诊断 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |
| 统计 | [statistical-power](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/statistical-power/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | 样本量 · 检验效能 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |
| 绘图 | [nature-figure](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-figure/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 期刊图表 · 导出 | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |
| 绘图 | [scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | 多面板 · 可读性 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |

### 论文写作与润色

| 板块 | Skill / 来源 | 标签 | 仓库 Stars |
|---|---|---|---|
| 写作 | [nature-writing](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-writing/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 投稿初稿 · LaTeX | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |
| 写作 | [scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | IMRaD · 报告规范 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |
| 润色 | [nature-polishing](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-polishing/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 学术英语 · 保真 | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |

### 审稿、回复与交付

| 板块 | Skill / 来源 | 标签 | 仓库 Stars |
|---|---|---|---|
| 审稿 | [nature-reviewer](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-reviewer/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 多视角 · 阻断项 | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |
| 审稿 | [peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/peer-review/SKILL.md)<br><sub>[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)</sub> | 方法 · 复现性 | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat-square&label=stars)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) |
| 回复 | [nature-response](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-response/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 逐条回复 · 修改定位 | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |
| 数据 | [nature-data](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-data/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 可用性声明 · FAIR | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |
| 汇报 | [nature-paper2ppt](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-paper2ppt/SKILL.md)<br><sub>[Nature Skills](https://github.com/Yuan1z0825/nature-skills)</sub> | 论文转 PPT · 渲染 | [![GitHub stars](https://img.shields.io/github/stars/Yuan1z0825/nature-skills?style=flat-square&label=stars)](https://github.com/Yuan1z0825/nature-skills/stargazers) |

完整输入、输出和验收契约见 [`capability_registry.yaml`](capability_registry.yaml)。第三方 Skill 保持独立安装、独立版本和独立许可证，本仓库不复制或捆绑其代码。

## 🔌 可插拔的专业能力

不必先装齐这些 Skill 才能开始，本仓库为每项能力都提供内置流程。选择针对**当前任务**进行，不会把整个项目永久绑定到某个仓库或期刊风格。

1. 用户明确指定的 provider 优先。
2. 未指定时，根据任务、目标格式、语言和已安装状态选择。
3. 选中后读取对应 Skill 的完整说明，执行其领域细节、排版、导出与 QA 标准。
4. 输出必须通过能力验收；不可用、不适配或验收失败时回退内置流程。
5. 不会静默安装第三方 Skill，也不会擅自向外部服务发送未发表稿件或受限数据。

## 🗂️ 你会得到什么

| 产物 | 用途 |
|---|---|
| `research_idea_portfolio.csv` | 比较候选问题、预测、最小研究、最近工作、风险和选择理由 |
| `search_protocol.md` / `screening_log.csv` | 复现数据库检索、去重、纳排标准和筛选决定 |
| `paper_reading_note.md` / `literature_matrix.csv` | 记录单篇论文证据，并跨研究综合方法、结果、冲突和局限 |
| `statistical_analysis_plan.md` / `experiment_matrix.csv` | 固化 estimand、样本量、模型、指标、诊断、消融与结果状态 |
| `data_provenance.csv` / `figure_brief.md` | 追踪数据来源、权限、变换、图表 claim、尺寸和导出要求 |
| `claim_ledger.csv` / `integrity_checklist.md` | 将强主张映射到证据，并在写作或投稿前发现阻断项 |
| `simulated_review.md` / `rebuttal_matrix.md` | 保存审稿问题、严重度、证据、准确修改位置与回应状态 |
| `submission_package_checklist.md` / `presentation_brief.md` | 核对投稿文件，并把论文论证转化为组会、答辩或会议汇报 |

Markdown、YAML 和 CSV 是便于审查与版本控制的规范格式；DOCX、PDF、XLSX 和 PPTX 可以作为最终交付格式，实际检索、计算与文件导出取决于智能体当前可用的工具。

## 💬 常用提示词

### 从模糊方向开始

```text
使用 $academic-paper-writing-skill 围绕“AI 辅助同行评审”提出 6 个彼此独立的研究问题。
对每个问题给出可证伪预测、最小可行研究、关键 prior work、失败风险和选择理由；先不要写论文正文。
```

### 做可复现的文献综述

```text
使用 $academic-paper-writing-skill 为这个主题设计 scoping review。
保存数据库、精确查询式、检索日期、纳排标准、去重与筛选日志；无法访问全文的论文不要假装已经核验。
```

### 审计已有稿件

```text
使用 $academic-paper-writing-skill 检查这份稿件的引用、统计、图表和强主张。
按 blocking / major / minor 分级，并为每个问题给出原文位置、证据指针和最小修复动作。
```

### 回复审稿意见

```text
使用 $academic-paper-writing-skill 建立逐条 rebuttal matrix。
不要把计划修改写成已经完成；每条回复必须指向证据、准确修改位置，或明确列为待办。
```

## 📚 模板与示例

- [本科论文开题证据工作流](examples/undergraduate-thesis-proposal-demo/README.md)
- [文献矩阵示例](examples/outputs/rag-evaluation-literature-matrix.sample.csv)
- [Claim ledger 示例](examples/outputs/rag-evaluation-claim-ledger.sample.csv)
- [Novelty 检查示例](examples/outputs/rag-evaluation-novelty-check.sample.md)
- [被证据门禁阻断的 related work 示例](examples/outputs/output-related-work-blocked.sample.md)
- [完整能力覆盖与设计依据](docs/CAPABILITY_COVERAGE.md)

也可以生成一个完全离线、可检查的示例工作区：

```bash
python scripts/demo_academic_workflow.py \
  --mode undergraduate_thesis \
  --out demo_workspace
```

初始化自己的项目：

```bash
python scripts/init_project.py --out paper_workspace --type research_paper
python scripts/init_project.py --out thesis_workspace --type undergraduate_thesis
```

## ✅ 阶段检查

当项目需要明确 handoff 时，可以检查当前阶段是否真的完成，而不是只检查文件是否存在：

```bash
python scripts/check_stage_gate.py paper_workspace --gate ideation
python scripts/check_stage_gate.py paper_workspace --gate literature
python scripts/check_stage_gate.py paper_workspace --gate analysis
python scripts/check_stage_gate.py paper_workspace --gate drafting
python scripts/check_stage_gate.py paper_workspace --gate submission
python scripts/check_stage_gate.py paper_workspace --gate presentation
```

失败信息会指出缺失文件、空记录、未确认状态或阻断证据，供下一轮工作继续处理。

## 🔒 完整性边界

适合：研究规划、论文精读、文献综述、实验和统计设计、科研绘图、论文写作与修订、rebuttal、投稿检查、本科论文、毕业设计、答辩和论文汇报。

不适合：无证据代写、伪造引用或数据、隐藏研究局限、规避伦理与学校要求、替代作者对最终稿件和提交内容负责。

涉及未发表手稿、同行评审材料、个人信息、受限数据或保密项目时，请先确认允许使用的工具和数据边界。

## 🧪 项目验证

<details>
<summary><b>运行维护者检查</b></summary>

```bash
python scripts/validate_skill.py
python scripts/validate_capability_registry.py
python scripts/test_provider_resolution.py
python scripts/test_stage_gate.py
python scripts/validate_readme_quality.py
python scripts/pre_prose_check.py examples/generated-demo-workspace --expect-block
```

GitHub Actions 会同时验证工作区初始化、证据状态、强 claim 阻断、provider fallback、阶段门禁和示例产物漂移。

</details>

## 🤝 贡献

欢迎提交 [Issue](https://github.com/xcl2005/academic-paper-writing-skill/issues) 或 [Pull Request](https://github.com/xcl2005/academic-paper-writing-skill/pulls)。优先欢迎以下贡献：

- 可复现、去标识化的真实科研案例；
- 新学科、期刊或报告规范的验收标准；
- 检索、统计、图表、引用与导出质量测试；
- 新 specialist skill 的 capability adapter，而不是永久硬编码依赖。

提交前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md) 和 [`SECURITY.md`](SECURITY.md)。

## 📄 许可证

[MIT](LICENSE)。可选第三方 skill 不随本仓库安装，其代码、内容和许可证归各自项目。
