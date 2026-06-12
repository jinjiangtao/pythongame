使用 Python 开发一个图形界面程序，功能类似于 Postman 的 API 测试工具。

技术栈要求：

· GUI框架：CustomTkinter
· HTTP请求库：requests
· 异步处理：QThread 防止界面卡顿

核心功能：

1. 支持 HTTP 方法：GET、POST、PUT、DELETE、PATCH
2. URL 地址输入框，支持请求参数拼接
3. 请求 Headers 管理（表格形式，可动态增删键值对）
4. 请求 Body 支持：
   · None（无Body）
   · form-data（表单）
   · x-www-form-urlencoded
   · raw（JSON / Text）
5. 响应展示区：
   · 状态码、响应时间、响应大小
   · 响应 Headers（可折叠/树形展示）
   · 响应 Body（支持 JSON 语法高亮和格式化）
6. 请求历史记录（左侧列表，点击可加载历史请求）
7. 集合/环境变量管理（可选进阶功能）

布局要求：

· 左侧：历史记录列表 + 集合列表（可折叠）
· 右侧上部：请求配置区（方法、URL、Headers、Body）
· 右侧下部：响应展示区（标签页切换）

技术要求：
· 网络请求必须在工作线程中执行，避免阻塞 UI
· 支持请求取消功能
· 支持超时设置
· 支持保存/导入/导出请求配置（JSON 格式）
. 文件不能写到同一个文件中，方便后面扩展。
. 代码可以直接运行， 缺少啥依赖，任务过程都安装上。

