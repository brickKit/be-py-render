# be/py-render

渲染外壳（Python）。代码只有入口与成员清单，承载逻辑在 be-sdk-python 的 `besdk.shell`。

## 代码地图

| 路径 | 内容 |
| --- | --- |
| `be_py_render/__init__.py` | 外壳的身份与装进来的成员（各成员包导出的定义） |
| `be_py_render/__main__.py` | 入口 |
| `tests/test_members.py` | 装进来的成员与版本必须等于 `component.yaml` 的 `shell.members` |
| `pyproject.toml`、`uv.lock` | 成员按标签取（不从本地路径装） |
| `Dockerfile` | 镜像 |

## 构建与测试

`uv sync && uv run pytest`；镜像 `docker build .`；在装配项目里 `brickkit build be/py-render`。成员在外壳里的行为由 `be-acceptance` 的测试与剖面在部署好的格里检验。

## 设计取舍

- 成员按标签从 Git 装，`uv.lock` 锁定；启动器按安装的分发元数据核对版本，拒绝从本地路径装的成员（PEP 610）。
- 外壳自己不迁移；成员的迁移用成员自己的镜像。

## 易错点

| 绝不 | 症状 | 为什么 |
| --- | --- | --- |
| 改了成员的标签不改 `component.yaml` 的 `shell.members`（或反过来） | `tests/test_members.py` 失败；漏过时 BrickKit 或启动器拒绝 | 三者必须一致（项目易错点：外壳的成员清单、编进来的成员与依赖锁） |
| 发布的镜像里从本地路径装成员 | 启动器拒绝，除非 `SHELL_ALLOW_REPLACE` | 版本号不再代表装进来的代码 |
| 声明改了不重建镜像 | `up` 拒绝：镜像里的成员与声明不符 | 镜像标签记下装进来的成员 |

## 改代码前自查

- 成员的标签、`shell.members` 与成员的定义版本是否一致？
- 外壳版本升了吗（每次改动都升版本）？
- 镜像重建了吗？

<!-- brickkit:managed:begin lang=zh -->
<!-- 由 brickkit 维护（init、add、remove、upgrade、skills update）：这对标记之间的改动会被覆盖 -->

## BrickKit

这是一个 BrickKit 组件：平台只读 `component.yaml`。它依赖的规则：

- `configSchema` 的键就是代码读的环境变量名。不能用保留名：`COMPONENT_ID`、`COMPONENT_VERSION`、`PORT`、`BRICKKIT_SERVED_MEMBERS`、`BRICKKIT_SERVED_MEMBERS_CONFIG`，以及任何 `*_ENDPOINT`。
- 依赖写精确版本。依赖的地址以 `<ID>_ENDPOINT` 注入；缺席的可选依赖根本没有这个变量，读的时候要带兜底。
- `/healthz` 只查本进程，不查依赖。迁移命令用同一个镜像跑，遇到不认识的参数必须直接失败；`local.migrationCommand` 从源码跑同一条迁移，给 `mode: local` 用。
- `BRICKKIT.md` 会随版本进入每个使用它的项目，在那里是脱离仓库单独读的：跟代码一起改，不放相对链接。
- 发版：改 `metadata.version`，提交、推送，`brickkit release`。`brickkit lint` 会检查清单和这些文档——在项目里、在这个目录下跑，只查这个组件（`--all` 查整个项目）。
- 完整规则在 `brickkit-component` 技能里（装了技能的项目或仓库根目录下的 `.claude/skills/brickkit-component/SKILL.md`；`brickkit skills update` 会装上）；参数问 `brickkit <命令> --help`；BrickKit 自己的文档用 `brickkit docs` 看。
<!-- brickkit:managed:end -->
