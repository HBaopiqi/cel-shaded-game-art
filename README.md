# 三渲二角色制作 · Toon Character Workflow

一个供 AI 助手使用的角色制作与排错 skill，由 HBaopiqi 根据 Arc System Works 技术美术本村・C・純也的五份分享独立整理。它把《GUILTY GEAR》系列的制作经验整理成八个可单独查阅的主题，适合建模师、绑定师和技术美术拿着自己的资产来问。

**从一个具体问题开始。** 比如角色站着时膝盖正常，一蹲就变薄，继续刷权重还有用吗？这套 skill 会先让你锁定出问题的动作帧，在副本里试关节轴心，再比较同一顶点完全随大腿和完全随小腿时的位置。在双骨线性混合蒙皮下，如果目标轮廓落在两点连线之外，继续调这两个权重就到不了。此时才值得比较改布线和加辅助骨的成本。[拓扑与蒙皮](skills/toon-character-workflow/references/03-topology-skinning.md)

*A Chinese-first Agent Skill for building and troubleshooting cel-shaded game characters. Install it below and ask in your preferred language. A standalone Markdown edition is available for assistants that accept documents.*

## 安装

在**要使用这套 skill 的项目**里运行以下命令。安装器会识别本机的客户端，如果出现选择界面，勾选你的 agent。需要 Node.js 和 Git。

```sh
npx skills add HBaopiqi/toon-character-workflow --skill toon-character-workflow
```

也可以指定客户端，例如只装给 Claude Code。加 `-g` 可改为当前用户的全局安装，加 `--copy` 可直接复制文件。安装器支持的其他客户端见 [skills CLI 名单](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。

```sh
npx skills add HBaopiqi/toon-character-workflow --skill toon-character-workflow -a claude-code
```

使用带 `gh skill` 命令的 GitHub CLI，也可以在目标 Git 项目中安装。例如安装给 Codex：

```sh
gh skill install HBaopiqi/toon-character-workflow toon-character-workflow --agent codex --scope project
```

**手动安装。** 下载并解压 [技能 ZIP](https://github.com/HBaopiqi/toon-character-workflow/releases/latest/download/toon-character-workflow.zip)，把里面的整个 `toon-character-workflow` 文件夹放入下表目录。从仓库克隆或下载源码时，找到 [SKILL.md](skills/toon-character-workflow/SKILL.md)，复制它所在的整个文件夹。以 Claude Code 为例，安装后的入口为 `.claude/skills/toon-character-workflow/SKILL.md`。

| 客户端 | 项目内可手动安装的目录 | 官方说明 |
| --- | --- | --- |
| Codex | `.agents/skills/` | [OpenAI Docs](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `.claude/skills/` | [Claude Code](https://code.claude.com/docs/en/skills) |
| Cursor | `.cursor/skills/` | [Cursor](https://cursor.com/docs/skills) |
| GitHub Copilot（VS Code） | `.github/skills/` | [VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills) |
| Gemini CLI | `.gemini/skills/` | [Gemini CLI](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `.opencode/skills/` | [OpenCode](https://opencode.ai/docs/skills/) |

**通过附件使用。** 下载 [单文件 Markdown](https://github.com/HBaopiqi/toon-character-workflow/releases/latest/download/toon-character-workflow.md)，发给能读附件的助手，再写「按这份工作流分析我的角色，用中文回答」。纯文本对话也可以粘贴入口和相关章节。这种方式在当前对话提供上下文。自动发现和安装取决于宿主是否支持 [Agent Skills](https://agentskills.io/specification)。

## 第一次使用

在目标项目新开一次会话。可以直接描述症状，也可以用客户端的显式调用方式，例如 Codex 的 `$toon-character-workflow` 或 Claude Code 的 `/toon-character-workflow`。带上目标镜头、失败姿势和一张对照图，通常就足以开始排查。

| 可以这样问 | 查阅方向 |
| --- | --- |
| 正脸和侧脸都像原画，但三分之四侧脸显得太宽。先看哪条轮廓？ | [造型与面部](skills/toon-character-workflow/references/01-modeling-face.md) |
| 脸部阴影静止时很干净，张嘴后出现脏块。 | [法线与阴影](skills/toon-character-workflow/references/02-normals.md) |
| 深蹲时膝盖变薄，护膝还穿进了裤子。怎样区分轴心、拓扑和权重？ | [拓扑与蒙皮](skills/toon-character-workflow/references/03-topology-skinning.md) · [骨骼放置](skills/toon-character-workflow/references/04-bone-placement.md) |
| 转手腕时整段前臂一起拧，怎样验证扭转骨？ | [绑定与辅助骨](skills/toon-character-workflow/references/05-rigging.md) |
| 用着切线空间法线贴图，硬边描边却裂开了。哪条数据可以用？ | [描边工程](skills/toon-character-workflow/references/06-outline-engineering.md) |
| 斜看袖口时，内壁有一条线浮在布料上。 | [描边美术控制](skills/toon-character-workflow/references/07-outline-art.md) |
| DCC 的动作和描边都正常，导入引擎后却变了，应该保留哪些对照？ | [验证与交付](skills/toon-character-workflow/references/08-validation-handoff.md) |

## 来源与许可

五份中文版讲义共 330 页。索引按中文版 PDF 的文件页序引用，提供五份 ASW Academy 日文原讲义的直达链接。公开发行物只收录独立整理的工作流、笔记、索引和维护工具。原讲义、译稿、插图、游戏资产与商标的权利属于各自权利人。[来源与逐页索引](skills/toon-character-workflow/references/00-sources.md)

工作流、笔记与索引由 HBaopiqi 按 **CC BY 4.0** 授权。复用时保留署名、来源与许可链接，改编时注明修改。仓库的 Python 脚本和持续集成配置采用 **MIT**。[内容许可](LICENSE) · [代码许可](scripts/LICENSE)

## 维护与打包

在仓库根目录运行以下命令，需要 Python 3.9 及以上版本，只使用标准库。技能本身是静态文件，日常使用无需 Python。

```sh
python scripts/validate_package.py
python scripts/build_release.py
```

校验器检查技能入口、引用和 330 页的区间覆盖。打包脚本把可安装 ZIP 和独立 Markdown 写入 `dist/`。角色在目标 DCC、引擎和设备上的表现，需用实际资产另行验证。
