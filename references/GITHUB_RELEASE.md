# 将 v2 发布到原 GitHub 仓库

原仓库（用户提供）：`https://github.com/hyjcandoit/ai-notion-daily-weekly-monthly-planner`

## 推荐上传步骤

1. 先把原仓库 `main` 备份为 tag 或分支（例如 `v0.1.0-backup`）。
2. 解压本 ZIP，将文件内容复制到原仓库根目录（`SKILL.md`、`README.md`、`QUICKSTART.zh-CN.md`、`LICENSE` 和 CSV 都在根目录，其他目录照原样）。
3. 仔细查看 Diff，确认没有包含任何真实 Notion 数据库 ID、页面 URL、个人任务、API Token 或私密资料。`config.local.yaml` / `*.local.md` / `*.private.md` 都被 `.gitignore` 忽略。
4. 推荐新建 `release/v2.0.0` 分支，提交，开 Pull Request 并审阅；审阅通过后合并到 `main`。
5. 打 Git tag `v2.0.0` 并发布简短 Release Notes（见 `CHANGELOG.md`）。
6. 根据你所使用的 Skill 客户端，从仓库根目录加载 `SKILL.md` 或上传解压后的 Skill 目录。

## 命令行示例

```bash
# 在你自己已有的本地仓库里操作；以下命令不会自动执行
cp -r /path/to/ai-notion-daily-weekly-monthly-planner-v2/. /path/to/your/cloned-repo/
cd /path/to/your/cloned-repo
git checkout -b release/v2.0.0
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
git status
git add SKILL.md README.md QUICKSTART.zh-CN.md CHANGELOG.md LICENSE .gitignore \
  references examples scripts tests notion_tasks_template.csv notion_tasks_template_v2.csv
git commit -m "feat: upgrade Notion planner skill to v2"
git push -u origin release/v2.0.0
```

若 GitHub 授权仅有只读权限，AI 可以分析仓库和准备 ZIP，但无法直接提交。**下载 ZIP 与完成 GitHub 推送是两个不同的动作。**
