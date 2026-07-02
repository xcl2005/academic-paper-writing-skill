<div align="center">

# Academic Paper Writing Skill

**面向论文、毕业设计、文献综述、rebuttal 和答辩的证据优先工作流。**

<a href="https://github.com/xcl2005/academic-paper-writing-skill/stargazers"><img src="https://img.shields.io/github/stars/xcl2005/academic-paper-writing-skill?style=flat-square" alt="stars"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/network/members"><img src="https://img.shields.io/github/forks/xcl2005/academic-paper-writing-skill?style=flat-square" alt="forks"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="license"></a>
<img src="https://img.shields.io/badge/Codex-Agent%20Skill-111827?style=flat-square" alt="Codex Agent Skill">
<img src="https://img.shields.io/badge/Policy-No%20Fake%20Papers-0F766E?style=flat-square" alt="No fake papers">

[English](README.md) · 简体中文

[安装](#安装) · [为什么需要](#为什么需要) · [控制流程](#控制流程) · [工作流](#工作流) · [产物](#产物)

</div>

## 为什么需要

学术写作不是“润色几段话”。一个可靠的 agent 必须先处理来源、论点、实验、假设、学校要求和完整性风险，再进入最终写作。

**Academic Paper Writing Skill** 给 Codex 提供模块化学术工作流，重点是避免虚构论文、虚构 SOTA、虚构结果和没有证据支撑的强主张。

## 亮点

| | 能力 |
|---|---|
| 📚 | 文献矩阵，要求来源可验证 |
| 🧠 | 在提出强 novelty/SOTA 结论前做检查 |
| 🧪 | 实验矩阵，记录指标、baseline、数据集和结果状态 |
| 🔗 | claim ledger，把强主张映射到证据 |
| 🎓 | 支持本科论文、毕业设计、proposal、midterm、答辩准备 |
| 🛡️ | 在最终 prose、rebuttal、答辩材料前做完整性检查 |

## 控制流程

这个 skill 是模块化的，因为学术任务差异很大。文献综述、rebuttal、本科开题和完整论文打包，不应该加载同一套长提示词。

| 步骤 | 决策点 | 行为 |
|---:|---|---|
| 1 | 选择项目类型 | 设置 `research_paper`、`undergraduate_thesis` 或 `hybrid_capstone_research`。 |
| 2 | 判断阶段 | 明确当前是选题、文献、novelty、实验、写作、修改、rebuttal、答辩还是打包。 |
| 3 | 最小模块加载 | 只读取当前阶段需要的模块，加上核心 invariants。 |
| 4 | 生成结构化产物 | 需要证据追踪时，先做矩阵和 ledger，再写正文。 |
| 5 | 验证强主张 | 将强 claim 映射到论文、实验、实现证据、测试、证明或官方要求。 |
| 6 | 完整性检查 | 区分计划、初步结果、已完成结果；不编造学校/导师/模板要求。 |
| 7 | 起草或修改 | 在证据记录可检查后，再写最终 prose 或 rebuttal。 |
| 8 | 人类复核 | 投稿、署名、伦理、学校合规和答辩结论必须由人确认。 |

### 模块路由

| 任务 | 通常加载的模块 |
|---|---|
| 文献综述 | `00_core_invariants`, `01_agent_orchestrator`, `06_literature_engine`, `11_integrity_reproducibility_guard` |
| Novelty / SOTA 检查 | `07_novelty_verification_and_scoring`, `11_integrity_reproducibility_guard` |
| 实验设计 | `09_experiment_matrix_engine`, `11_integrity_reproducibility_guard` |
| 图表设计 | `10_figure_table_engine` |
| Rebuttal / 模拟审稿 | `13_simulated_review_rebuttal`, `11_integrity_reproducibility_guard` |
| 本科论文要求发现 | `04_requirement_discovery`, `14_undergraduate_thesis_engine`, `11_integrity_reproducibility_guard` |

### 证据生命周期

| 产物 | 作用 |
|---|---|
| Literature matrix | 追踪已验证论文、方法、数据集、claim 和相关性 |
| Novelty matrix | 将你的 idea 与已有工作对照 |
| Experiment matrix | 记录指标、baseline、数据集、ablation 和结果状态 |
| Claim ledger | 让每个强主张可审计 |
| Integrity checklist | 在最终写作前发现虚构、夸大或无证据表述 |

## 安装

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.agents/skills/academic-paper-writing-skill
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
git clone https://github.com/xcl2005/academic-paper-writing-skill.git "$HOME\.agents\skills\academic-paper-writing-skill"
```

如果 Codex 没有自动刷新 skill 列表，重启 Codex。

## 工作流

| 模式 | 适用 | 输出 |
|---|---|---|
| `research_paper` | 论文、related work、实验、rebuttal、revision | 文献矩阵、novelty 检查、实验矩阵、claim ledger |
| `undergraduate_thesis` | 开题、中期、毕业论文、毕业设计、答辩 | 要求发现记录、scope ladder、graduation evidence map |
| `hybrid_capstone_research` | 先毕业设计，后续升级论文/作品集 | thesis MVP、evidence package、research upgrade plan |

## 快速开始

```bash
# 创建研究论文工作区
python scripts/init_project.py --out paper_workspace --type research_paper

# 创建本科论文/毕业设计工作区
python scripts/init_project.py --out thesis_workspace --type undergraduate_thesis

# 验证 skill 结构
python scripts/validate_skill.py
```

## 产物

- `templates/literature_matrix.csv`
- `templates/novelty_verification.csv`
- `templates/experiment_matrix.csv`
- `templates/claim_ledger.csv`
- `templates/integrity_checklist.md`
- `templates/rebuttal_matrix.md`
- `templates/graduation_evidence_map.csv`
- `templates/project_state.yaml`

Markdown、YAML、CSV 是工作源格式。Word、PDF、Excel、slides 是导出格式。

## 不可破坏的规则

- 不编造论文；
- 不编造 SOTA；
- 不编造结果；
- 不编造学校、导师、rubric、答辩要求；
- 优先使用 primary sources；
- 强 claim 必须映射到证据；
- 投稿、署名、伦理、学校合规必须由人复核。

## 值得阅读的文件

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 入口和 non-negotiable invariants |
| `skill_manifest.yaml` | 项目类型、阶段、模式和模块路由 |
| `modules/00_core_invariants.md` | 完整性基线 |
| `modules/06_literature_engine.md` | 文献综述工作流 |
| `modules/07_novelty_verification_and_scoring.md` | Novelty 和 SOTA 检查 |
| `modules/14_undergraduate_thesis_engine.md` | 本科论文/毕业设计路线 |

## 项目质量检查

```bash
python scripts/validate_readme_quality.py
```

检查会阻止 README 中出现大尺寸 banner、生成式图表、残留 hero/workflow SVG 引用，以及缺失安装/完整性说明。

## 搜索关键词

Academic writing AI, research paper workflow, literature review matrix, thesis writing assistant, graduation project, rebuttal assistant, claim evidence mapping, research integrity, Codex skills, Agent Skills.

## Version

`8.0.0-final-candidate`

## License

MIT
