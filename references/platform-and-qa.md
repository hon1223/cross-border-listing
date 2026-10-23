# 目标平台与校验

## 规则获取

不在通用技能中固定永久字符上限或统一图片要求。写作时查目标国家、类目、字段的现行官方规则，或用户提供的有效品类模板。区分硬性上限、建议长度与编辑偏好；API schema 限制不一定等于页面显示规则。记录原始来源、日期与计数单位。

|目标|优先核对的官方入口与字段|
|---|---|
|Amazon|对应站点 Seller Central 帮助、类目模板；标题、bullet points、description、generic keywords、类目属性。Backend 限制若以 bytes 计，不能以字符替代。A+ 仅在用户需要且具备适用条件时输出。|
|Walmart|对应 US/CA Marketplace Learn 的 Product details/content policy、具体 Item Spec；product name、key features、site description 与必要属性。不把 CA 当 US，不套用 Amazon 五点长度，不凭第三方技能固定标题 75 字符或一律 10 条。|
|eBay|Seller Center/开发者当前字段说明；title、item specifics、description。确认 HTML 支持与限制，不默认套用其他平台的后台词。|
|Shopify/独立站|Shopify Help Center 的产品与搜索引擎展示字段；产品标题/正文与 SEO title/meta description 分开。SEO 建议展示长度不冒充平台硬上限；不默认加与现有主题重复的结构化数据。|
|Etsy|Etsy Help/Seller Handbook 的当前标题、标签、属性与描述要求；确认 tags 的数量/长度及本地语言，不靠堆砌重复词。|
|其他平台|查目标市场 Seller Center 官方规则/模板，再映射字段，缺证据的规则标待核实。|

能获取公开官方文档时无需登录卖家后台。无法核实某字段限制时可以交付注明限制待核实的保守草稿，不声称可直接成功上架，不自行发明限制。产品事实审核仍必须先完成。

## 机械计数工具

需要批量/有上限字段时运行：

```text
python <skill目录>/scripts/check_fields.py <fields.json>
```

输入格式如下；演示上限只是演示，不能当任何平台的规定：

```json
{
  "fields": [
    {"name":"title","text":"Example product","unit":"chars","max":100,"rule_source":"填写已核实来源与日期"},
    {"name":"search_terms","text":"example","unit":"utf8_bytes","max":20,"rule_source":"填写已核实来源与日期"},
    {"name":"description","text":"Example description.","unit":"words"}
  ]
}
```

每条卖点/每个标签独立计数。无已核实上限时省略 min/max，结果为 counted_only，不能说已通过平台限制。chars 为 Unicode code point 数（含空格）；UTF-8 bytes 计算编码后字节数；words 为 Unicode 非空白分词，仅适合按空格分词的语言粗计。若平台定义不同，采用平台的算法而不是本工具。

脚本退出码 0 表示已提交规则无违反，1 表示长度不符，2 表示输入不合法。独立检查事实、变体、禁用声明及语义，不能用计数通过替代人工审稿。禁止把自定义 QA 分数宣传成平台 Listing Quality 分数、排名或转化效果。
