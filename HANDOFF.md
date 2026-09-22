# 安装与维护交接

AuditSpeakStyle 0.2.0。项目新增内容已采用 MIT，署名为 herecythrone and AuditSpeakStyle contributors；上游许可、版权及归属声明完整保留。

## 文件范围

[MANIFEST.sha256](MANIFEST.sha256)列示发布文件，清单自身另计。现有仓库可能包含未发布资料；更新时逐文件比较，不目录级覆盖、不重置或清理未提交内容。安装时复制 skills/audit-speak-style 完整目录，包括 PROVENANCE.md 和 LICENSES 两份许可，不覆盖旧 audit-writing-cn。

## 验证

在干净发布副本运行：

```bash
python scripts/validate.py
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/validate.py --check-manifest
```

44例参考答案不等于44次模型实测。工具测试、作者自检、小规模模型测试分别报告，见 [原始包验证报告](docs/validation-report.md) 和 [后续模型测试](docs/model-smoke-tests.md)。含额外文件的开发仓库不能为了严格清单检查而删除这些文件；改版后在干净发布副本更新清单。

## 操作范围

安装、修改、提交和发布按用户当前授权执行。公开材料中不包括开发交接提示、私有参考快照、客户材料、凭证或本机路径。未来文风修改需重新验证，不把一次通过当作长期保证。
