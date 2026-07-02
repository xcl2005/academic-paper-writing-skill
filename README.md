<div align="center">

# Academic Paper Writing Skill

**证据优先的专业学术级别论文、毕业设计、文献综述、rebuttal 与答辩工作流。**

<a href="https://github.com/xcl2005/academic-paper-writing-skill/stargazers"><img src="https://img.shields.io/github/stars/xcl2005/academic-paper-writing-skill?style=flat-square" alt="GitHub stars"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/network/members"><img src="https://img.shields.io/github/forks/xcl2005/academic-paper-writing-skill?style=flat-square" alt="GitHub forks"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT license"></a>
<img src="https://img.shields.io/badge/Agent%20Skills-Codex%20%7C%20Claude-111827?style=flat-square" alt="Agent Skills for Codex and Claude">
<img src="https://img.shields.io/badge/Integrity-No%20Fake%20Papers-0F766E?style=flat-square" alt="No fake papers">
<img src="https://img.shields.io/badge/Formats-MD%20%7C%20YAML%20%7C%20CSV-7C3AED?style=flat-square" alt="Markdown YAML CSV">

简体中文 · [English](README_EN.md)

[快速开始](#-快速开始) · [为什么需要](#-为什么需要) · [能力亮点](#-能力亮点) · [Codex / Claude](#-codex--claude-code) · [工作流](#-工作流) · [完整性规则](#-完整性规则)

</div>

## 🔥 最新定位

这个仓库不是一段“学术写作提示词”，而是一套可安装的 Agent Skill：它把论文、毕业设计、综述、实验规划、rebuttal、答辩材料拆成可验证的模块，让 agent 在写作前先处理来源、证据、claim、实验、学校要求和完整性风险。

适用于 Codex、Claude Code，以及遵循 Agent Skills 目录结构的其他 agent。Claude Code 可以用同一个 `SKILL.md`，但安装路径和直接调用方式不同，见下方 [Codex / Claude Code](#-codex--claude-code)。

## ✨ 为什么需要

学术写作最容易出问题的地方不是措辞，而是证据链断裂：论文没核验、SOTA 被夸大、实验结果被提前写成已完成、学校模板或导师要求被凭空补全。

**Academic Paper Writing Skill** 的原则是先建立可审查的中间产物，再进入最终 prose。它默认使用 primary sources、claim-to-evidence mapping 和完整性检查，降低虚构引用、虚构结果、过度承诺和毕业要求误判的风险。

## 👨‍💻 适用场景

| 场景 | 适合做什么 |
|---|---|
| 研究论文 | 选题、related work、novelty/SOTA 检查、实验矩阵、投稿前完整性审计 |
| 文献综述 | 构建 literature matrix，按方法、数据集、claim、局限和相关性整理来源 |
| Rebuttal / revision | 模拟审稿、回应矩阵、证据补强、措辞降调 |
| 本科论文 / 毕设 | 需求发现、scope ladder、开题/中期/终稿/答辩材料 |
| 混合项目 | 先满足毕业要求，再判断是否值得升级为 paper / portfolio |

## 🎯 能力亮点

| | 能力 |
|---|---|
| 🔍 | 文献矩阵：追踪已验证论文、方法、数据集、claim 和相关性 |
| 🧪 | 实验矩阵：记录 metric、baseline、dataset、ablation 和结果状态 |
| 🧭 | Novelty / SOTA 检查：强结论前先核验 prior work |
| 🔗 | Claim ledger：每个强主张必须映射到证据 |
| 🛡️ | 完整性检查：区分计划、初步结果、已完成结果，不伪造学校要求 |
| 🎓 | 本科论文路线：开题、中期、终稿、毕业设计和答辩证据包 |

## 📦 快速开始

### Codex 用户

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.agents/skills/academic-paper-writing-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
git clone https://github.com/xcl2005/academic-paper-writing-skill.git "$HOME\.agents\skills\academic-paper-writing-skill"
```

调用方式：

```text
使用 $academic-paper-writing-skill 帮我做这篇论文的文献矩阵和 novelty 检查。
```

### Claude Code 用户

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.claude/skills/academic-paper-writing-skill
```

项目级安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git .claude/skills/academic-paper-writing-skill
```

直接调用：

```text
/academic-paper-writing-skill 帮我把毕业设计题目拆成开题报告范围和证据清单
```

### 初始化工作区

```bash
# 创建研究论文工作区
python scripts/init_project.py --out paper_workspace --type research_paper

# 创建本科论文 / 毕业设计工作区
python scripts/init_project.py --out thesis_workspace --type undergraduate_thesis

# 验证 skill 结构
python scripts/validate_skill.py
```

## 🔁 Codex / Claude Code

| 项目 | Codex | Claude Code |
|---|---|---|
| 共享结构 | `skill-name/SKILL.md`，可带 `modules/`、`templates/`、`scripts/` | 同左 |
| 用户级路径 | `~/.agents/skills/academic-paper-writing-skill` | `~/.claude/skills/academic-paper-writing-skill` |
| 项目级路径 | `.agents/skills/academic-paper-writing-skill` | `.claude/skills/academic-paper-writing-skill` |
| 自动触发 | 依赖 `description` 与当前任务匹配 | 依赖 `description` 与当前任务匹配 |
| 显式调用 | `$academic-paper-writing-skill ...` | `/academic-paper-writing-skill ...` |
| README 入口 | 默认中文 `README.md`，英文见 `README_EN.md` | 同一仓库链接即可 |

Claude.ai / Claude API 通常需要把 skill 作为自定义 skill 上传或通过 Skills API 注册；GitHub clone 路径主要面向本地 Claude Code 与 Codex。

## 🧭 工作流

| 模式 | 适用 | 主要输出 |
|---|---|---|
| `research_paper` | 论文、related work、实验、rebuttal、revision | literature matrix、novelty check、experiment matrix、claim ledger |
| `undergraduate_thesis` | 开题、中期、毕业论文、毕业设计、答辩 | requirement log、scope ladder、graduation evidence map |
| `hybrid_capstone_research` | 先毕业设计，后续升级论文 / 作品集 | thesis MVP、evidence package、research upgrade plan |

### 控制流程

| 步骤 | 决策点 | 行为 |
|---:|---|---|
| 1 | 选择项目类型 | 设置 `research_paper`、`undergraduate_thesis` 或 `hybrid_capstone_research` |
| 2 | 判断阶段 | 识别选题、文献、novelty、实验、写作、revision、rebuttal、答辩或打包 |
| 3 | 最小模块加载 | 只读当前任务需要的模块，加上 core invariants |
| 4 | 生成结构化产物 | 需要证据追踪时先做矩阵和 ledger，再写正文 |
| 5 | 验证强主张 | 将 claim 映射到论文、实验、实现证据、测试、证明或官方要求 |
| 6 | 完整性检查 | 区分计划、初步结果、已完成结果；不编造学校 / 导师 / rubric 要求 |
| 7 | 起草或修订 | 在证据记录可检查后，再写最终 prose 或 rebuttal |
| 8 | 人类复核 | 投稿、署名、伦理、学校合规和答辩结论必须由人确认 |

### 模块路由

| 任务 | 通常加载的模块 |
|---|---|
| 文献综述 | `00_core_invariants`, `01_agent_orchestrator`, `06_literature_engine`, `11_integrity_reproducibility_guard` |
| Novelty / SOTA 检查 | `07_novelty_verification_and_scoring`, `11_integrity_reproducibility_guard` |
| 实验规划 | `09_experiment_matrix_engine`, `11_integrity_reproducibility_guard` |
| 图表规划 | `10_figure_table_engine` |
| Rebuttal / 模拟审稿 | `13_simulated_review_rebuttal`, `11_integrity_reproducibility_guard` |
| 本科论文需求发现 | `04_requirement_discovery`, `14_undergraduate_thesis_engine`, `11_integrity_reproducibility_guard` |

## 🗂️ 产物

| 文件 | 用途 |
|---|---|
| `templates/literature_matrix.csv` | 已验证文献、方法、数据集、claim、相关性 |
| `templates/novelty_verification.csv` | 将你的 idea 与已有工作对照 |
| `templates/experiment_matrix.csv` | metric、baseline、dataset、ablation、结果状态 |
| `templates/claim_ledger.csv` | 让每个强主张可审查 |
| `templates/integrity_checklist.md` | 写作前发现虚构、夸大或无证据表达 |
| `templates/graduation_evidence_map.csv` | 毕设 / 本科论文证据包 |

Markdown、YAML 和 CSV 是规范工作格式；Word、PDF、Excel、slides 是导出格式。

## 🛡️ 完整性规则

- 不编造论文。
- 不编造 SOTA。
- 不编造结果。
- 不编造学校、导师、rubric、模板、答辩或工作量要求。
- 优先使用 primary sources。
- 强 claim 必须映射到证据。
- 投稿、署名、伦理、学校合规必须由人复核。

## 🛠️ 质量检查

```bash
python scripts/validate_skill.py
python scripts/validate_readme_quality.py
```

## 📁 仓库结构

```text
.
|-- SKILL.md
|-- skill_manifest.yaml
|-- modules/
|-- templates/
|-- schemas/
|-- scripts/
|-- examples/
|-- README.md
`-- README_EN.md
```

## 🔎 搜索关键词

Academic writing AI, research paper workflow, literature review matrix, thesis writing assistant, graduation project, rebuttal assistant, claim evidence mapping, research integrity, Codex skills, Claude Code skills, Agent Skills.

## 📄 许可证

MIT
