import re;


str="""
- GitHub中文社区
  "https://www.githubs.cn/"
- Easy的个人主页
  "https://dun.mianbaoduo.com/@easy"
- 开发流程 | Obsidian 插件开发文档
  "https://luhaifeng666.github.io/obsidian-plugin-docs-zh/zh/getting-started/development-workflow.html"
- devbean/obsidian-wordpress: An obsidian plugin for publishing docs to WordPress.
  "https://github.com/devbean/obsidian-wordpress"
- obsidianmd/obsidian-api
  "https://github.com/obsidianmd/obsidian-api"
- zhaohongxuan/obsidian-weread-plugin: Obsidian Weread Plugin is an plugin to sync Weread(微信读书) hightlights and annotations into your Obsidian Vault.
  "https://github.com/zhaohongxuan/obsidian-weread-plugin"
- rosulek/workflowy-clipper: WorkFlowy clipper: Chrome extension
  "https://github.com/rosulek/workflowy-clipper"
"""

reg = r'- ([\s\S]*?)  \"(http.*?)\"'
res=re.findall(reg,str)
for i in res:
    print(i)
print(str)