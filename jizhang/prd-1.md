使用 Python + CustomTkinter + sqlite3 开发个人记账管理系统桌面GUI程序，严格遵循MVC架构分层开发，模块化、低耦合、中文显示正常无乱码，界面简洁现代美观。

仅实现以下3个核心功能：
1. 用户系统：登录、注册，密码使用哈希加密存储，一人一账本，不同用户数据完全隔离。
2. 分类管理：收入/支出分类自定义管理，支持新增、修改、删除、查询，分类归属对应用户。
3. 账单管理：账单新增、修改、删除、查询，账单字段包含：收支类型、分类、金额、备注、付款方式、日期，归属对应用户。

项目结构（严格MVC）：
- main.py                 程序入口，启动登录界面
- model/                  模型层（无GUI，纯数据、数据库、业务逻辑）
  - db.py                 数据库基类：连接、关闭、执行、查询、事务
  - user_model.py         用户模型：注册、登录、密码加密、数据隔离
  - category_model.py     分类模型：增删改查，关联用户
  - bill_model.py         账单模型：增删改查，关联用户
- view/                   视图层（纯GUI，无业务、无数据库代码）
  - login_view.py         登录注册界面
  - main_view.py          主界面，页面切换
  - category_view.py      分类管理界面
  - bill_view.py          账单管理界面
- controller/             控制器层（连接View与Model）
  - user_controller.py    用户登录注册控制
  - category_controller.py 分类管理控制
  - bill_controller.py    账单管理控制
- config.py               全局配置：数据库名、窗口大小、主题、路径
- tests/
  - test_db.py
  - test_user.py
  - test_category.py
  - test_bill.py

强制开发约束：
1. MVC严格分离：View只做界面，不写业务与数据库；Model只做数据与逻辑，不引用GUI；Controller处理事件、调用模型、刷新视图。
2. 用户数据隔离：每个用户只能看到、管理自己的分类与账单。
3. 密码必须哈希加密存储，不保存明文。
4. 表单校验：金额必须正数、非空判断、合法日期，异常弹窗提示。
5. 中文显示正常，无乱码。
6. 数据库文件与程序同目录，程序启动时自动创建表，不存在则自动创建。
7. 程序关闭时自动安全关闭数据库连接。
8. 代码规范、注释清晰、分文件编写、可直接运行。
9. 支持使用 pyinstaller 打包成单文件 exe，无Python环境也可运行。
10. 使用CustomTkinter实现现代简洁GUI，操作流畅、布局合理、提示友好。