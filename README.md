<div align="center">

# Academic Paper Writing Skill

**接口式、证据优先的科研工作流：从选题、检索、统计和绘图，到写作、审稿、投稿与论文汇报。**

<a href="https://github.com/xcl2005/academic-paper-writing-skill/stargazers"><img src="https://img.shields.io/github/stars/xcl2005/academic-paper-writing-skill?style=flat-square" alt="GitHub stars"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/network/members"><img src="https://img.shields.io/github/forks/xcl2005/academic-paper-writing-skill?style=flat-square" alt="GitHub forks"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/xcl2005/academic-paper-writing-skill/ci.yml?branch=main&style=flat-square" alt="CI status"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/releases"><img src="https://img.shields.io/github/v/release/xcl2005/academic-paper-writing-skill?style=flat-square" alt="Latest release"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT license"></a>
<img src="https://img.shields.io/badge/Agent%20Skills-Codex%20%7C%20Claude-111827?style=flat-square" alt="Codex and Claude Code">
<img src="https://img.shields.io/badge/workflow-evidence--first-0F766E?style=flat-square" alt="Evidence first">
<img src="https://img.shields.io/badge/providers-pluggable-7C3AED?style=flat-square" alt="Pluggable providers">

简体中文 · [English](README_EN.md)

[快速开始](#-快速开始) · [能力接口](#-能力接口) · [工作标准](#-工作标准) · [模块路由](#-模块路由) · [质量检查](#-质量检查)

</div>

## 🔥 这是什么

这不是一段“帮我写论文”的长 prompt，也不是把十几个外部 skill 写死的调用清单。

它由三层组成：

| 层 | 作用 |
|---|---|
| 内部基线 | 保留并增强原有的文献矩阵、novelty/SOTA、ROI、实验矩阵、claim ledger、完整性、本科论文、review/rebuttal 等成熟功能 |
| 能力接口 | 把选题、检索、统计、绘图、写作、润色、审稿、数据声明、论文转 PPT 定义成稳定的输入/输出契约 |
| 可插拔 provider | 检测到适合的专业 skill 时读取并采用其完整细节；缺失、失败或不适配时回退内部模块 |

因此，项目既能使用成熟专业 skill 的极致细节，又不会永久依赖某一个仓库、名称、工具或期刊风格。

## ✨ v2.0

- 新增 13 个科研能力接口和 18 个可选 provider 映射。
- 新增选题与问题设计、系统检索与筛选、研究设计/统计/数据、投稿与论文汇报四个内部模块。
- 新增 `capability_registry.yaml`，按任务、目标、语言、格式和已安装状态选择 provider。
- 新增 `resolve_capability.py`，可查看当前会使用专业 skill 还是内部 fallback。
- 新增阶段门禁，检查产物是否真正填写并达到 handoff 条件。
- 保留原有三种项目类型、七个 mode、全部核心模块和 pre-prose 校验。

## 🧩 能力接口

外部 provider 都是可选项，不会静默安装。选中后，agent 必须完整读取对应 `SKILL.md` 及当前流程要求的资源，使用它的详细领域、排版、导出和 QA 标准。

| 能力 | 优先 provider | 内部 fallback | 关键验收 |
|---|---|---|---|
| 🧭 全流程统筹 | `academic-research-suite` | agent orchestrator + mode router | 阶段、证据边界、产物和人类决策可追踪 |
| 💡 选题与科研头脑风暴 | `scientific-brainstorming` | research ideation module | 独立生成、假设、反方压力测试、决策记录 |
| 🔎 学术检索与引用管理 | `nature-academic-search`, `paper-lookup` | scholarly search module | 查询式、来源、时间、失败、去重和覆盖边界可复现 |
| 📚 文献综述与证据综合 | `literature-review` | literature engine | 筛选、质量评估、研究矩阵、分歧和局限可追踪 |
| 🧪 研究设计与统计 | `experimental-design`, `statistical-analysis`, `statistical-power` | study design/statistics module | estimand、效应量、区间、假设、多重比较和诊断完整 |
| 📊 科研绘图与表格 | `nature-figure`, `scientific-visualization` | figure/table engine | 最终尺寸、色盲可读、数据追溯、可编辑源文件和导出 QA |
| ✍️ 论文写作 | `nature-writing`, `scientific-writing` | writing adapter | 数字、引用、术语、claim 强度和 reporting guideline 一致 |
| 📝 润色与翻译 | `nature-polishing` | writing adapter | 不改变事实、公式、引用、结果方向和技术术语 |
| 🧐 模拟审稿 | `nature-reviewer`, `peer-review` | review/rebuttal engine | concern ID、证据指针、严重度、blocking 判断和修改路径 |
| 💬 审稿回复 | `nature-response` | review/rebuttal engine | 每条意见映射到证据、准确修改位置或明确未决动作 |
| 🗃️ 数据与代码可用性 | `nature-data` | delivery + integrity modules | repository、许可、版本、access route 和 FAIR 信息不虚构 |
| 🎤 论文转汇报 | `nature-paper2ppt` | delivery/presentation module | 真实 PPTX、论证主线、图表裁切、speaker notes 和渲染检查 |

完整定义见 [`capability_registry.yaml`](capability_registry.yaml)，设计说明见 [`docs/CAPABILITY_COVERAGE.md`](docs/CAPABILITY_COVERAGE.md)。

## 🧱 工作标准

能力覆盖只是起点，v2.0 同时吸收成熟科研 skill 的执行标准：

| 环节 | 最低工作标准 |
|---|---|
| 选题 | idea 先独立生成再收敛；每项包含可证伪预测、最小研究、最近工作、风险与选择理由 |
| 检索 | 保存数据库、精确查询式、字段/时间限制、运行日期、结果数、失败、去重和排除理由 |
| 综述 | 明确 rapid / narrative / scoping / systematic；不能用不完整检索冒充系统综述 |
| 研究设计 | 定义观察、分配和分析单位，estimand、sampling、controls、confounding、missingness 与 bias |
| 统计 | 预先区分 confirmatory / exploratory；报告 effect size、uncertainty、diagnostics、multiplicity 与 deviation |
| 绘图 | 绘图前定义 claim、数据、统计标注、最终物理尺寸和输出格式；最终必须 render 后目视检查 |
| 写作 | drafting 与 polishing 分离；数字、引用、公式、术语和 claim strength 是受保护事实 |
| 审稿 | reviewer assessment 与 author response 分离；问题必须有稳定 ID、原文指针和证据指针 |
| 投稿 | manuscript、图表、supplement、references、声明、data/code 和 portal preview 互相一致 |
| 汇报 | 以论文论证为主线，不照搬章节顺序；figure 是证据，speaker notes 和 package QA 是交付的一部分 |

## 📦 快速开始

Codex / Claude Code 共用同一个 `SKILL.md`、能力 registry 和内部模块；安装路径与显式调用语法不同。

### Codex

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.agents/skills/academic-paper-writing-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
git clone https://github.com/xcl2005/academic-paper-writing-skill.git "$HOME\.agents\skills\academic-paper-writing-skill"
```

调用示例：

```text
使用 $academic-paper-writing-skill 帮我从选题开始做一篇可投稿论文。
先给出候选方向和检索计划，不要编造文献；统计、绘图和最终排版优先调用最合适的已安装专业 skill。
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.claude/skills/academic-paper-writing-skill
```

直接调用：

```text
/academic-paper-writing-skill 帮我审计这篇论文，并为每条主要问题建立证据和修改记录
```

### 检查 provider

```bash
python scripts/resolve_capability.py --list
python scripts/resolve_capability.py research_ideation --json
python scripts/resolve_capability.py scientific_visualization --tag nature --json
```

返回 `use_installed_provider` 时会显示具体 `SKILL.md`；返回 `use_internal_fallback` 时继续使用本仓库对应模块。

## 🧭 工作流

没有固定的长流程。每次调用都按当前任务组合最少能力：

| 步骤 | 决策与行为 |
|---:|---|
| 1 | 设置 project type、stage、目标、证据边界和缺失输入 |
| 2 | 从 registry 识别一个或多个 capability |
| 3 | 保留用户指定 provider；否则按目标标签、已安装状态和优先级解析 |
| 4 | 读取内部 baseline；若选中 provider，再完整读取其 `SKILL.md` 和相关资源 |
| 5 | 用 `capability_handoff.yaml` 传递输入、受保护事实、权限和输出契约 |
| 6 | 生成矩阵、ledger、计划、代码或真实交付文件 |
| 7 | 执行 capability acceptance、stage gate、pre-prose 或 artifact QA |
| 8 | 通过后进入下一能力；失败则保留问题、回退或请求必要证据 |

### 模块路由

| 任务 | 主要内部模块 |
|---|---|
| 项目统筹 | `01_agent_orchestrator`, `02_mode_router`, `22_capability_provider_router` |
| 选题 | `18_research_ideation_and_question_design`, `07_novelty_verification_and_scoring`, `08_research_roi_scope` |
| 检索与综述 | `20_scholarly_search_screening_and_references`, `06_literature_engine` |
| 研究设计与分析 | `19_study_design_statistics_and_data`, `09_experiment_matrix_engine` |
| 图表 | `10_figure_table_engine` |
| 写作与润色 | `12_writing_style_adapter`, `11_integrity_reproducibility_guard` |
| 审稿与回复 | `13_simulated_review_rebuttal`, `11_integrity_reproducibility_guard` |
| 投稿与汇报 | `21_research_delivery_and_presentation` |
| 本科论文 | `04_requirement_discovery`, `14_undergraduate_thesis_engine` |
| 外部 skill 治理 | `03_external_skill_gateway`, `17_external_skill_acceptance_tests` |

## 🗂️ 产物

| 文件 | 用途 |
|---|---|
| `research_idea_portfolio.csv` | 候选选题、证据、预测、最小研究、风险与决策 |
| `search_protocol.md` / `screening_log.csv` | 可复现检索、筛选、去重和排除记录 |
| `paper_reading_note.md` / `literature_matrix.csv` | 论文精读、来源边界与跨研究综合 |
| `novelty_verification.csv` / `roi_matrix.csv` | prior-work 对照、novelty 风险和投入产出判断 |
| `statistical_analysis_plan.md` | estimand、样本量、模型、假设、区间、多重比较与敏感性分析 |
| `data_provenance.csv` / `experiment_matrix.csv` | 数据来路、权限、变换、实验状态与复现信息 |
| `figure_brief.md` / `terminology_ledger.csv` | 科学图表契约和全文术语一致性 |
| `claim_ledger.csv` / `integrity_checklist.md` | 强主张证据映射与 pre-prose 完整性门禁 |
| `simulated_review.md` / `rebuttal_matrix.md` | 可追溯审稿和逐条回复 |
| `submission_package_checklist.md` / `presentation_brief.md` | 投稿包、论文汇报、组会或答辩交付 |

## ✅ 阶段门禁

```bash
python scripts/init_project.py --out paper_workspace --type research_paper
python scripts/check_stage_gate.py paper_workspace --gate ideation
python scripts/check_stage_gate.py paper_workspace --gate literature
python scripts/check_stage_gate.py paper_workspace --gate analysis
python scripts/check_stage_gate.py paper_workspace --gate drafting
python scripts/check_stage_gate.py paper_workspace --gate submission
python scripts/check_stage_gate.py paper_workspace --gate presentation
```

门禁失败会列出缺失文件、空表或仍为 `draft` 的产物。失败代表下一步工作，不代表可以补造数据或来源。

## 🔁 原功能兼容

| 保留项 | 状态 |
|---|---|
| `research_paper`, `undergraduate_thesis`, `hybrid_capstone_research` | 保留 |
| Literature Matrix、Novelty Verification、Experiment Matrix、Figure Design | 保留并增强 |
| Claim Ledger、Integrity Audit、Pre-Prose Gate | 保留 |
| Simulated Review / Rebuttal | 保留并增强角色分离和证据指针 |
| Requirement Discovery、Scope Ladder、Graduation Evidence Map | 保留 |
| External Skill Gateway / Acceptance Tests | 保留并升级为 provider interface |
| 旧 demo、fixtures、generated reports、CI drift checks | 保留 |

`scripts/validate_skill.py` 会把这些旧 project types、mode、模块和脚本作为 backward-compatibility 契约检查。

## 🛡️ 完整性规则

### Integrity-first by default

- 不编造论文、作者、DOI、venue、SOTA、leaderboard、数据、结果或学校要求。
- 区分 verified fact、paper claim、agent inference、assumption 和 user-provided information。
- 强 claim 必须映射到来源、数据、分析、实验、实现、测试、证明或官方要求。
- planned、exploratory、preliminary、achieved 和 externally reported results 必须分开。
- 不把 rapid scan 说成 systematic review，不把显著性说成实际重要性或因果。
- 未经授权，不把未发表稿件、peer-review 材料、个人或受限数据交给外部 provider。
- 投稿、署名、伦理、consent、受限数据、学校合规和最终判断必须由人确认。

当证据状态为 `needs_recheck`、`missing_source`、`unknown`、`unsupported` 或 `blocked` 时，最终 prose 必须降调、保留占位或阻断。

## 🛠️ 质量检查

```bash
python scripts/validate_skill.py
python scripts/validate_capability_registry.py
python scripts/validate_readme_quality.py
python scripts/validate_evidence_status.py templates examples/outputs examples/fixtures examples/generated-demo-workspace
python scripts/pre_prose_check.py examples/generated-demo-workspace --expect-block
```

CI 还会验证初始化工作区、provider fallback、旧 demo、中文强 claim、生成报告漂移和阶段门禁。

## 📁 仓库结构

```text
.
|-- SKILL.md
|-- skill_manifest.yaml
|-- capability_registry.yaml
|-- agents/
|-- modules/
|-- templates/
|-- schemas/
|-- scripts/
|-- examples/
|-- docs/
|-- README.md
`-- README_EN.md
```

## 🔎 搜索关键词

Academic writing AI, research workflow, scientific brainstorming, academic search, literature review, systematic review, statistical analysis, scientific visualization, Nature writing, paper polishing, peer review, reviewer response, data availability, paper to PPT, thesis writing assistant, claim evidence mapping, research integrity, Codex skills, Claude Code skills, Agent Skills.

## 📄 许可证

MIT。外部 provider 不随本仓库安装，其代码、内容和许可证仍归各自项目；本仓库只维护接口、路由、内部 fallback 和验收标准。
