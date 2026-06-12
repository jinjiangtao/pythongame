# Trae Session 工具

获取 Trae sessionId、历史轨迹和当前对话的命令行工具。

## 安装步骤

1. **编译程序**
   ```powershell
   .\build.ps1
   ```

2. **配置环境变量**
   ```powershell
   .\setup-env.ps1
   ```

3. **重启终端** 使环境变量生效

## 使用方法

### 显示所有信息（sessionId + 历史轨迹 + 当前对话）
```powershell
trae-session
```

### 仅显示 sessionId
```powershell
trae-session --session
```

### 仅显示历史轨迹
```powershell
trae-session --history
```

### 仅显示当前对话
```powershell
trae-session --current
```

### 以 JSON 格式输出
```powershell
trae-session --json
trae-session --session --json
trae-session --history --json
trae-session --current --json
```

## 环境变量要求

程序需要以下环境变量：
- `TRAE_SESSION_ID`: Trae 会话 ID
- `TRAE_HOME`: Trae 主目录（用于查找历史轨迹和当前对话文件）
