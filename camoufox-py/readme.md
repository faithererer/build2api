# Camoufox 多实例自动化工具 (YAML 配置版)

这是一个 Python 脚本，用于使用 [Camoufox](https://camoufox.com/) 库，通过一个简单易读的 `config.yaml` 文件来并发运行多个独立的浏览器实例。

## 功能

*   **YAML 集中配置**：所有运行参数（代理、无头模式、实例列表）都集中在单一的 `config.yaml` 文件中，无需命令行参数。
*   **全局与局部设置**：可以设置全局配置，并为特定实例覆盖这些配置，提供了极大的灵活性。
*   **多实例并发**：通过一个配置文件定义并启动任意数量的浏览器实例。
*   **独立进程**：每个浏览器实例都在其自己的进程中运行，确保了稳定性和隔离性。
*   **独立 Cookie**：为每个实例指定不同的 Cookie 文件，实现多账户同时在线。

## 安装

### 1. 先决条件

*   Python 3.8+
*   pip

### 2. 安装依赖

您需要安装 `camoufox`、`pyyaml`（用于解析配置文件）以及可选的 `geoip`。

```bash
pip install -U "camoufox[geoip]" pyyaml
```

安装包后，您需要下载 Camoufox 浏览器本身：

```bash
camoufox fetch
```

### 3. (可选) 在 Linux 上安装虚拟显示

为了在 Linux 上获得最佳的无头浏览体验 (`headless: virtual`)，建议安装 `xvfb`。

```bash
# 对于 Debian/Ubuntu
sudo apt-get install xvfb

# 对于 Arch Linux
sudo pacman -S xorg-server-xvfb
```

## 用法

### 1. 准备 Cookie 文件

为每个您想运行的账户准备一个 `cookie.json` 文件。例如，`user1_cookie.json`, `user2_cookie.json` 等, 放在cookies/ 文件夹下。

### 2. 创建 `config.yaml` 配置文件

在项目根目录创建一个名为 `config.yaml` 的文件。这是控制整个脚本行为的核心。

**`config.yaml` 示例:**

```yaml
# 全局设置，将应用于所有实例，除非在特定实例中被覆盖
global_settings:
  # 无头模式: true (标准无头), false (有头), or 'virtual' (虚拟显示, 推荐)
  headless: virtual
  
  # 全局代理 (可选)。如果大多数实例都使用同一个代理，请在这里设置。
  # 格式: "http://user:pass@host:port"
  proxy: null # "http://user:pass@globalproxy.com:8080"

# 要并发运行的浏览器实例列表
instances:
  # 实例 1: 使用全局设置
  - cookie_file: "user1_cookie.json"
    url: "https://aistudio.google.com/apps/drive/your_project_id_1"

  # 实例 2: 覆盖全局设置，使用自己的代理并以有头模式运行
  - cookie_file: "user2_cookie.json"
    url: "https://aistudio.google.com/apps/drive/your_project_id_2"
    headless: false # 覆盖全局设置，此实例将显示浏览器窗口
    proxy: "http://user:pass@specific-proxy.com:9999" # 使用特定代理

  # 实例 3: 另一个使用全局设置的例子
  - cookie_file: "user3_cookie.json"
    url: "https://some-other-website.com/"
    # 此处未指定 headless 或 proxy，因此它将使用 global_settings 中的值
```

### 3. 运行脚本

现在，运行脚本非常简单，只需提供配置文件的路径即可。

```bash
python3 run_camoufox.py config.yaml
```

脚本将会读取 `config.yaml`，并根据您的配置启动所有定义的浏览器实例。

### 4. 停止脚本

脚本会一直运行，直到您手动停止它。在运行脚本的终端中按 `Ctrl+C`，主程序会捕获到信号并终止所有正在运行的浏览器子进程。