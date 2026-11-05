# Cel-Shaded Game Art｜三渲二游戏美术

面向三渲二游戏角色制作的跨软件 Agent Skill，指导 AI 根据目标镜头塑造角色剪影、围绕动作需求规划拓扑与绑定，并解答从蒙皮形变到实时描边的技术问题。

安装后，直接向支持自动选用技能的 Agent 描述角色需求或提出制作问题。修改模型时，Agent 使用当前项目已接入的 3D 软件。

- **「为侧视动作游戏制作一名三渲二剑士，主动作是双手举剑过顶。」** Agent 会先从游戏镜头检查角色与武器的剪影，在低模阶段试摆举剑姿势，再依据肩部形变和袖口穿插的位置调整轴心与布线。
- **「我想让头发的阴影连成整块，可以从球面传递法线吗？」** 助手会解释这种做法怎样改变受光。如果发梢也沿这组法线生成描边，它还会提醒你检查外轮廓，并给出对照方法。[法线与阴影](skills/cel-shaded-game-art/references/02-normals.md)

本项目由 HBaopiqi 根据 Arc System Works 技术美术本村・C・純也关于《GUILTY GEAR》系列的五份分享独立整理。

*An agent skill for cel-shaded game character production across 3D tools. It guides silhouette design for the gameplay camera, topology and rigging for the intended motion, and troubleshooting of shading and outlines.*

## 安装

在**要使用这套 skill 的项目**里运行以下命令。安装器会识别本机的客户端，如果出现选择界面，勾选你的 agent。需要 Node.js 和 Git。

```sh
npx skills add HBaopiqi/cel-shaded-game-art --skill cel-shaded-game-art
```

也可以指定客户端，例如只装给 Claude Code。加 `-g` 可改为当前用户的全局安装，加 `--copy` 可直接复制文件。安装器支持的其他客户端见 [skills CLI 名单](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。

```sh
npx skills add HBaopiqi/cel-shaded-game-art --skill cel-shaded-game-art -a claude-code
```

使用带 `gh skill` 命令的 GitHub CLI，也可以在目标 Git 项目中安装。例如安装给 Codex：

```sh
gh skill install HBaopiqi/cel-shaded-game-art cel-shaded-game-art --agent codex --scope project
```

**手动安装。** 下载并解压 [技能 ZIP](https://github.com/HBaopiqi/cel-shaded-game-art/releases/latest/download/cel-shaded-game-art.zip)，把里面的整个 `cel-shaded-game-art` 文件夹放入下表目录。从仓库克隆或下载源码时，找到 [SKILL.md](skills/cel-shaded-game-art/SKILL.md)，复制它所在的整个文件夹。以 Claude Code 为例，安装后的入口为 `.claude/skills/cel-shaded-game-art/SKILL.md`。

| 客户端 | 项目内可手动安装的目录 | 官方说明 |
| --- | --- | --- |
| Codex | `.agents/skills/` | [OpenAI Docs](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `.claude/skills/` | [Claude Code](https://code.claude.com/docs/en/skills) |
| Cursor | `.cursor/skills/` | [Cursor](https://cursor.com/docs/skills) |
| GitHub Copilot（VS Code） | `.github/skills/` | [VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills) |
| Gemini CLI | `.gemini/skills/` | [Gemini CLI](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `.opencode/skills/` | [OpenCode](https://opencode.ai/docs/skills/) |

**通过附件使用。** 下载 [单文件 Markdown](https://github.com/HBaopiqi/cel-shaded-game-art/releases/latest/download/cel-shaded-game-art.md)，发给能读附件的助手，再写「按这份工作流分析我的角色，用中文回答」。纯文本对话也可以粘贴入口和相关章节。这种方式在当前对话提供上下文。自动发现和安装取决于宿主是否支持 [Agent Skills](https://agentskills.io/specification)。

**从 1.x 升级。** 在原来的项目或用户范围安装 `cel-shaded-game-art`。确认客户端能发现新技能后，可移除 `toon-character-workflow` 并更新项目中显式调用旧标识的指令。[1.x 发行记录](https://github.com/HBaopiqi/cel-shaded-game-art/releases/tag/v1.1.1)

## 第一次使用

在目标项目新开一次会话，直接描述想做的角色或想问的问题。也可以按客户端的方式点名调用，例如 Codex 的 `$cel-shaded-game-art` 或 Claude Code 的 `/cel-shaded-game-art`。排查已有模型时，目标镜头和出问题的姿势最有助于定位。

| 可以这样问 | 查阅方向 |
| --- | --- |
| 正脸和侧脸都像原画，但三分之四侧脸显得太宽。先看哪条轮廓？ | [造型与面部](skills/cel-shaded-game-art/references/01-modeling-face.md) |
| 脸部阴影静止时很干净，张嘴后出现脏块。 | [法线与阴影](skills/cel-shaded-game-art/references/02-normals.md) |
| 深蹲时膝盖变薄，护膝还穿进了裤子。怎样区分轴心、拓扑和权重？ | [拓扑与蒙皮](skills/cel-shaded-game-art/references/03-topology-skinning.md) · [骨骼放置](skills/cel-shaded-game-art/references/04-bone-placement.md) |
| 转手腕时整段前臂一起拧，怎样验证扭转骨？ | [绑定与辅助骨](skills/cel-shaded-game-art/references/05-rigging.md) |
| 用着切线空间法线贴图，硬边描边却裂开了。哪条数据可以用？ | [描边工程](skills/cel-shaded-game-art/references/06-outline-engineering.md) |
| 斜看袖口时，内壁有一条线浮在布料上。 | [描边美术控制](skills/cel-shaded-game-art/references/07-outline-art.md) |
| DCC 的动作和描边都正常，导入引擎后却变了，应该保留哪些对照？ | [验证与交付](skills/cel-shaded-game-art/references/08-validation-handoff.md) |

## 来源与许可

五份中文版讲义共 330 页。索引按中文版 PDF 的文件页序引用，提供五份 ASW Academy 日文原讲义的直达链接。公开发行物只收录独立整理的工作流、笔记、索引和维护工具。原讲义、译稿、插图、游戏资产与商标的权利属于各自权利人。[来源与逐页索引](skills/cel-shaded-game-art/references/00-sources.md)

工作流、笔记与索引由 HBaopiqi 按 **CC BY 4.0** 授权。复用时保留署名、来源与许可链接，改编时注明修改。仓库的 Python 脚本和持续集成配置采用 **MIT**。[内容许可](LICENSE) · [代码许可](scripts/LICENSE)

## 维护与打包

在仓库根目录运行以下命令，需要 Python 3.9 及以上版本，只使用标准库。技能本身是静态文件，日常使用无需 Python。

```sh
python scripts/validate_package.py
python scripts/build_release.py
```

校验器检查技能入口、引用和 330 页的区间覆盖。打包脚本把可安装 ZIP 和独立 Markdown 写入 `dist/`。角色在目标 DCC、引擎和设备上的表现，需用实际资产另行验证。
