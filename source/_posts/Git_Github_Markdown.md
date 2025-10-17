---
title: Git & GitHub & Markdown &刷课
date: 2025-10-17 11:17
tags: 技术,教程
---

# Git & GitHub & Markdown &刷课

## **环境准备**

### Chrome 浏览器下载

**推荐使用国内 Cent Browser：**

- [官方下载地址(官网)](https://www.centbrowser.cn/)

- 继承谷歌内核稳定流畅的优点同时，与 Chrome 基本操作界面别无二致, 并加入其他常用功能

**推荐使用谷歌 Chrome 浏览器：**

- [官方下载地址（需科学上网）](https://www.google.com/chrome/)
- 或搜索“Chrome 浏览器下载国内镜像”获取国内最新可用链接。

### VPN 与机场

#### VPN 是什么？机场是什么？

- **VPN**：虚拟专用网络，最初是企业、学校等用于远程安全访问内部资源。后来大家习惯把“翻墙”工具称为 VPN，但实际上 VPN 协议并不专属于翻墙，比如 WireGuard、OpenVPN 等真正网络层的 VPN 协议。
- **机场**：是专门提供“科学上网”服务的平台。机场主租用大量 VPS（国外服务器），搭建 SS、SSR、Vmess、Trojan 等代理协议节点，用户买流量后通过代理软件（如 Clash、小火箭等）连接机场获得自由访问外网的能力。
- **区别与关系**：VPN 是网络层代理，机场多用应用层/会话层代理。大多数商业 VPN 广告多且贵，体验和性价比远不如机场。

#### 为什么叫“机场”？

因为最早的代理工具 Shadowsocks 图标是一架小飞机，大家就把这种代理服务叫做“机场”。



机场并不是一个单一的服务器或网站，而是由许多分布在国内外的节点组成，具备分布式、多协议、动态更新和多种抗干扰技术，能灵活应对各种封锁与干扰。即使部分节点被墙，用户只需刷新订阅或等待机场主修复即可继续使用。

下面分几条简要解释：

1. **多节点分散部署**
   机场通常在国内外部署了很多服务器（节点），即使部分节点被墙封锁，其他节点仍可正常工作，不会导致整个机场服务瘫痪。
2. **协议混淆与加密**
   机场使用的代理协议（如 SS、Trojan、Vmess 等）都具备流量加密和混淆能力，能有效隐藏翻墙行为，使防火墙难以精准识别和封锁。
3. **动态更换节点和订阅**
   机场可以随时更换服务器 IP、端口、协议等参数，用户通过订阅链接自动获取最新节点信息，及时绕开已被封锁的节点。
4. **中转与专线技术**
   很多机场采用“国内中转”、“隧道”、“专线”等技术，使流量出境路线更加隐蔽和多样化，提高抗封锁能力。
5. **高防与灾备机制**
   优质机场会购买高防护服务器、备用线路、CDN 加速等服务，即使遭遇攻击或封锁，也能迅速切换恢复服务。

#### 协议科普

- **SS/SSR**：Shadowsocks 及其分支 SSR，轻量级加密代理，速度快，兼容性好。
- **Vmess/VLESS**：V2Ray 框架的协议，功能丰富，支持多种混淆和传输方式。
- **Trojan**：基于 HTTPS，伪装成正常网页流量，抗封锁能力强。
- **Hy2/Reality/Tuic**：新一代协议，多用于自建直连，机场较少支持，安全性更高。
- **传统 VPN 协议**：如 PPTP、L2TP/IPSec、OpenVPN、WireGuard 等，主要用于网络层代理，穿透性和安全性各有不同。

#### 机场线路名词解释

- **规则**：只有国外网站走代理，节省流量
- **全局**：所有流量都走代理
- **直连**：用户设备直接连境外代理服务器，速度受限、极易被墙。
- **中转**：流量先到国内中转服务器，再转发到境外代理服务器。可以优化速度和稳定性，降低被墙风险。
- **隧道**：国内服务器入口+境外服务器（如香港 CMI），流量经过 TLS 加密再转发，更安全。
- **专线（IEPL/IPLC）**：点对点物理线路，低延迟，不经过公网，最稳定但成本高，机场多用 IEPL。
- **BGP**：边界网关协议，优化多运营商之间的互联访问速度和稳定性。
- **前置**：中转入口前再加一台国内机器，抗通报/墙封。
- **转发**：多个机场共享中转资源，速度和稳定性差，常见于小机场。
- **流量倍率**：部分机场设置倍率，如 2 倍率表示实际消耗 2 倍流量。
- **系统代理**：大多数应用（如浏览器）自动走代理，部分软件需手动设置
- **TUN 模式/虚拟网卡**：创建虚拟网卡，实现真正全局代理，解决部分应用不走代理的问题
- **自动选择/故障转移：** 自动选择延迟最低节点，但可能频繁切换 IP，容易被某些网站风控

#### 线路体验优先级

同样带宽下，体验优先级：  

**IEPL 专线中转 > 隧道中转 > 公网中转（如广东移动/湖南联通） > 直连**

![image-20251016175400498](/images/Git_Github_Markdown/Git_Github_Markdown_1.png)

##### 1. 直连机场

- **流程**：用户设备 → 宽带运营商 → 境内防火墙/QoS 限速 → 直接连接境外 VPS/服务器 → 国际互联网
- **特点**：没有经过国内中转节点，直接出海。速度受限、易被墙，体验和稳定性都较差，适合流量小、只偶尔使用者。

##### 2. 普通中转机场

- **流程**：用户设备 → 宽带运营商 → 境内中转 VPS → 境内防火墙/QoS 限速 → 境外 VPS → 国际互联网
- **特点**：增加了一个国内中转节点，优化了出海速度和稳定性。成本较低，但中转节点易受干扰，遇到高峰期或被墙会影响体验。

##### 3. BGP 中转机场

- **流程**：用户设备 → 宽带运营商 → BGP 中转服务器（多线接入、跨运营商优化） → 境内防火墙/QoS 限速 → 境外 VPS → 国际互联网
- **特点**：BGP 中转节点支持多运营商线路，自动选择最优路径，提升了全国范围的访问速度和稳定性。更适合多地区用户，成本比普通中转高。

##### 4. IPLC 中转机场

- **流程**：用户设备 → 宽带运营商 → 境内中转 VPS → IPLC 专线传输 → 境外 VPS → 国际互联网
- **特点**：IPLC（国际专线）是物理专用通道，数据从境内直接通过专线传到境外，几乎不经过防火墙和公网，速度、稳定性和安全性最高，但价格也最贵。适合对速度和稳定性要求极高的用户或企业。

---

#### 推荐客户端工具

- **Windows/Mac/Android**：首选 Clash 系列（Clash for Windows、Clash Verge、Clash Meta、Flclash、Clash Party、Sparkle 等）
- **iOS**：首选小火箭（Shadowrocket，付费）。

#### 客户端使用流程简述

1. 下载并安装客户端软件
2. 在机场后台获取订阅链接（通常一键复制）
3. 导入到客户端
4. 打开系统代理或虚拟网卡（TUN 模式），实现全局或分流科学上网
5. 常见问题：分流规则设置、系统代理/TUN 模式选择、节点测速与切换

---

#### 机场购买与使用流程

#### 如何购买机场

- 注册账号（推荐 Gmail/Outlook 邮箱，不建议 QQ 邮箱，避免实名风险）
- 选择套餐，付款（部分机场支持试用套餐）
- 获取订阅链接，导入代理软件
- 按照机场提供的小白教程操作，几乎所有机场都有详细的使用说明

![三色图](/images/Git_Github_Markdown/Git_Github_Markdown_2.webp)

#### 小白教程

最小白的教程，适合第一次买机场的，

先注册，注意的点是验证码邮件可能会在邮箱垃圾箱里面。
如果有试用先试用，没试用就去购买套餐。

1）我们以随便某个 v2board 机场为例子，因为现在很多机场都是用的 v2board 页面。
**第一步：购买套餐：点击购买订阅–选择你想要的套餐–付款**
[![购买订阅](https://jichangtuijian.com/uploads/jichangjiaochen/v1.webp)](https://jichangtuijian.com/uploads/jichangjiaochen/v1.webp)
[![选择套餐](https://jichangtuijian.com/uploads/jichangjiaochen/v2.webp)](https://jichangtuijian.com/uploads/jichangjiaochen/v2.webp)

**第二步：下载代理软件**，这里以 Clash for windows 为例子

**第三步：导入订阅：回到仪表盘–点击一键订阅–导入到你的 Clash 客户端中**
[![仪表盘](https://jichangtuijian.com/uploads/jichangjiaochen/v3.webp)](https://jichangtuijian.com/uploads/jichangjiaochen/v3.webp)
[![导入订阅](https://jichangtuijian.com/uploads/jichangjiaochen/v4.webp)](https://jichangtuijian.com/uploads/jichangjiaochen/v4.webp)
导入订阅后
[![导入订阅后](https://jichangtuijian.com/uploads/jichangjiaochen/v5.webp)](https://jichangtuijian.com/uploads/jichangjiaochen/v5.webp)

后面看 clash 教程

2）另一个常见面板的：sspanel 前端面板的也是类似的。购买套餐-导入订阅

**购买订阅**
[![购买订阅](https://jichangtuijian.com/uploads/jichangjiaochen/s1.webp)](https://jichangtuijian.com/uploads/jichangjiaochen/s1.webp)
**回到首页导入订阅**
[![导入订阅](https://jichangtuijian.com/uploads/jichangjiaochen/s2.webp)](https://jichangtuijian.com/uploads/jichangjiaochen/s2.webp)

具体详细操场教程可以参考各个机场的使用教程，每个机场基本都有小白教程的。

#### 节点和订阅相关问题

- 节点不能用时，先检查流量套餐是否到期或用尽，再刷新订阅或重新复制订阅链接
- 校园网或公司网可能封端口或 DNS 异常，影响机场使用
- 机场官网和订阅地址常变，因 GFW 污染 DNS，老牌机场处理经验更丰富

---

#### 线路技术与常见问题详解

##### 机场官网慢/打不开？

- 多数机场官网套了 Cloudflare CDN，隐藏真实 IP，防止被墙，访问速度慢需要科学上网

##### 为什么有些机场便宜？

- 便宜线路（如月抛）、多人共享、直连节点、不买中转、割韭菜跑路风险高

##### 为什么流量消耗快？

- 流量倍率设置、自动选择高倍率节点、系统更新等走代理流量

##### 为什么机场界面都很像？

- 大多数机场用开源面板（V2board、SSpanel），前端界面相似是正常现象

##### 为什么延迟测试异常？

- 部分机场劫持延迟测试，仅到中转入口（非真实国际延迟），可更换延迟测试 URL 验证

##### 机场能否打游戏？

- 不推荐机场打游戏，延迟高、UDP 支持差，建议用专业游戏加速器（如 UU 加速器）。部分机场有专线游戏节点，但不保证稳定

---

#### 机场安全性与合规问题

#### 翻墙是安全吗？

- 你猜
- 低调，不要键政，不要绑定实名信息
- 机场主肉身墙外更安全，选老牌大机场，月付为佳
- 被抓多因机场主肉身墙内、高调、实名收款、境内推广

#### 机场跑路怎么办？

- 灰色产业，跑路风险高，优先选择老牌、肉身墙外的机场主，推荐月付。跑路后只能更换机场

#### 白嫖机场安全吗？

- 免费机场体验差或安全风险高，仅试用阶段可考虑，长期建议付费正规机场



---

## Git 与 GitHub

- **Git**：核心工具，记录代码修改历史，创建分支，合并分支等。
- **GitHub/Gitee**：代码托管平台，方便协作、展示作品、参与开源项目。、



1. Git 版本控制基础
   - 安装与配置（Windows/Mac/Linux）
   - 常用命令演示
2. GitHub 账号注册与界面介绍
   - 教育邮箱注册技巧
   - 仓库、Issue、PR 等基本功能
3. GitHub 教育认证与 Copilot 白嫖流程
   - Copilot 是什么
   - 认证与激活详细步骤
4. 基础实战：远程仓库协作、Fork、PR 操作演示



### Git 是什么

**Git 就像一本“时光机日记本”📖**  

每段代码的改动，Git 都会帮你记录下来，随时可以“穿越回过去”查找任何时间点的代码状态。

- **主要特点：**
  1. **版本控制**：每次提交都像写新日记，保存开发成果。
  2. **分支管理**：分支如同章节，可以并行开发互不干扰。
  3. **分布式**：每个人都有完整的“时光机日记本”，即使没有网络也能工作。

---

### Git 与 GitHub SSH Key 配置与使用

#### 1. 配置个人信息

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```
- 设置后每次提交都会自动带上你的署名。

#### 2. 生成 SSH 密钥

```bash
ssh-keygen -t rsa -b 4096 -C "你的邮箱@example.com"
```
- -t rsa ：使 ⽤ RSA 算法 ⽣ 成密钥。
- 一路回车即可，密钥默认保存在 `~/.ssh/` 目录。

#### 3. 查看并复制公钥内容

```bash
cat ~/.ssh/id_rsa.pub
```
- 复制输出的内容（全部内容）。

#### 4. 添加公钥到远程仓库

- **GitHub**：Settings > SSH and GPG keys > New SSH key，粘贴公钥并保存。
- **Gitee**：设置 > 安全设置 > SSH 密钥，粘贴公钥并保存。

#### 5. 测试连接

- GitHub：`ssh -T git@github.com`
- Gitee：`ssh -T git@gitee.com`

- 第一次会提示“Are you sure you want to continue connecting”，输入 yes
- 若看到 `Hi 用户名! You've successfully authenticated...` 表示成功！

#### 6. 多平台/多账户密钥配置（进阶）

- 多台电脑、多个平台可分别生成密钥并添加到账户。
- 如需配置多个密钥，在 `~/.ssh/config` 文件中添加：

```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa

Host gitee.com
  HostName gitee.com
  User git
  IdentityFile ~/.ssh/id_rsa_gitee
```

### Git 命令

#### 基本操作

```bash
# 初始化仓库（只需一次）
git init

# 克隆远程仓库到本地
git clone <仓库地址>

# 查看当前状态
git status

# 查看历史提交记录
git log
```

#### 文件操作

```bash
# 添加所有更改到暂存区
git add .

# 添加指定文件到暂存区
git add 文件名

# 从暂存区移除文件
git reset 文件名
```

#### 提交/保存更改

```bash
# 提交到本地仓库
git commit -m "提交说明"
```

#### 与远程仓库交互

```bash
# 关联远程仓库（只需一次）
git remote add origin <仓库地址>

# 推送到远程仓库
git push

# 推送到远程指定分支（第一次推送用）
git push -u origin main

# 从远程仓库拉取最新内容
git pull
```

#### 分支管理

```bash
# 查看所有分支
git branch

# 创建新分支
git branch 新分支名

# 切换分支
git checkout 分支名

# 创建并切换到新分支
git checkout -b 新分支名

# 删除本地分支
git branch -d 分支名

# 查看远程分支
git branch -r

# 拉取远程分支并创建本地分支
git checkout -b 本地分支名 origin/远程分支名

# 删除远程分支
git push origin --delete 分支名
```

#### 撤销与恢复

```bash
# 撤销工作区的修改（让文件恢复到上一次commit的状态）
git checkout -- 文件名

# 撤销暂存区的修改（把已add的文件撤回到工作区）
git reset HEAD 文件名

# 撤销最近一次commit但保留修改（回退到上一次commit，修改内容还在）
git reset --soft HEAD^

# 丢弃最近一次commit和修改（慎用，修改会丢失）
git reset --hard HEAD^

# 恢复被删除的文件（找回误删的文件）
git checkout HEAD -- 文件名
```

#### 查看与对比

```bash
# 查看本地和远程分支对应关系
git branch -vv

# 查看远程地址
git remote -v

# 查看某个文件的修改内容
git diff 文件名

# 查看暂存区和上一次commit的区别
git diff --cached

# 查看某个文件的历史修改记录
git log 文件名

# 对比本地分支与远程分支的差异
git diff main origin/main
```

#### 标签（Tag）

```bash
# 打标签
git tag v1.0

# 推送标签到远程
git push origin v1.0

# 查看所有标签
git tag
```

#### 合并与冲突

```bash
# 合并分支
git merge 另一个分支名

# 解决冲突后，添加并提交
git add .
git commit -m "fix conflict"
```

---

> **提示：**
>
> - 不会的命令可以用 `git help 命令名` 查看帮助。
> - 日常开发建议多用 `git status` 和 `git log` 观察当前状态。
> - 日常开发推荐分支模型，每个功能新建分支，开发完成合并主线

---

### Git 常用命令速查表

| 功能             | 命令                                                         | 说明                                 |
| ---------------- | ------------------------------------------------------------ | ------------------------------------ |
| 配置用户名和邮箱 | `git config --global user.name "你的名字"` <br> `git config --global user.email "你的邮箱"` | 设置“署名”，每次提交都标记贡献者     |
| 初始化仓库       | `git init`                                                   | 新建“时光机日记本”，准备记录代码版本 |
| 添加文件到暂存区 | `git add 文件名` 或 `git add .`                              | 把修改内容放到“草稿区”               |
| 提交到本地仓库   | `git commit -m "提交说明"`                                   | 草稿正式进入日记本，并附说明         |
| 推送到远程仓库   | `git push origin 分支名`                                     | 把本地代码同步到远程仓库             |
| 克隆远程仓库     | `git clone 仓库地址`                                         | 下载别人的代码到本地                 |
| 查看状态         | `git status`                                                 | 检查当前代码变化情况                 |
| 查看提交历史     | `git log`                                                    | 查看代码记录，回顾“时间线”           |
| 创建分支         | `git branch 分支名`                                          | 新功能独立章节                       |
| 切换分支         | `git checkout 分支名`                                        | 从一个章节切换到另一个章节           |
| 合并分支         | `git merge 分支名`                                           | 不同章节内容合并到主线               |
| 拉取远程代码     | `git pull origin 分支名`                                     | 从远程仓库获取最新代码               |

---

### GitHub 入门详解

#### 1. GitHub 是什么？

- **GitHub** 是全球最大的开源代码托管平台，基于 Git 版本控制，方便开发者协作、分享和展示项目。
- 在 GitHub 上，你可以：
  - 托管自己的项目代码，并进行版本管理
  - 查找和参与全球开源项目
  - 与他人协作开发（团队项目、开源贡献）
  - 展示个人作品，提升技术影响力

#### 2. GitHub 账号注册与界面介绍

- [GitHub 注册入口](https://github.com/)

- 不建议直接使用教育邮箱注册

  > 我们学校的教育邮箱是   学号@stu.nchu.edu.cn
  >
  > 教育认证可额外绑定教育邮箱，可获取学生认证福利（如 Copilot 免费使用）

- 注册流程：填写邮箱、用户名、密码 → 邮箱验证 → 完善个人资料

##### GitHub 主要界面说明
- **Repositories（仓库）**：项目代码的存放地，每个仓库包含代码、文档、历史记录等
- **Issues**：用于提交问题、建议、任务分解，方便项目管理和交流
- **Pull Requests（PR）**：代码协作的核心，提交代码修改请求，项目维护者审核后合并
- **Fork**：复制别人的项目到你的账户，方便独立开发或贡献代码
- **Star**：收藏项目，方便日后查找
- **Actions**：自动化 CI/CD 工具，帮助自动测试和部署

#### 3. GitHub 教育认证与 Copilot 白嫖流程

- **GitHub Copilot**：AI 智能编程助手，自动补全代码、生成函数/注释，提升开发效率
- **教育认证步骤**：
  1. 注册并登录 GitHub 账号
  2. 访问 [GitHub Education](https://education.github.com/) 页面，点击“Get benefits”或“Apply for Student Developer Pack”
  3. 根据提示填写教育邮箱、学生身份等信息，提交认证
  4. 通过后可免费开通 Copilot（[Copilot 激活入口](https://github.com/settings/copilot)）

#### 4. GitHub 基础实战流程

- **远程仓库协作流程**：
  1. Fork 项目到个人账户
  2. Clone 仓库到本地
  3. 新建分支，进行开发
  4. 提交并推送修改到远程分支
  5. 发起 Pull Request，等待项目维护者审核合并
  6. 参与 Issues 讨论，跟进项目进展

- **常见协作场景**：
  - 团队开发：多人协作同一项目，分工明确，分支合并
  - 开源贡献：发现项目问题或有新功能建议，可提交 PR 或 Issue
  - 个人作品：将自己的代码托管公开，展示技术实力

#### 5. GitHub 常用术语补充

- **Commit**：每一次代码提交
- **Branch**：分支，独立开发环境
- **Merge**：合并分支
- **Release**：项目发布版本
- **Webhook**：自动通知外部服务

---

### Gitee 入门详解

#### 1. Gitee 是什么？

- **Gitee（码云）**：中国主流的代码托管平台，支持 Git 管理，适合国内团队、企业使用。
- 优势：
  - 国内访问速度快，无需科学上网
  - 支持私有仓库免费（适合团队或企业项目）
  - 与中国开发者生态结合紧密（对接企事业单位、开源中国等）

#### 2. Gitee 账号注册与界面介绍

- [Gitee 注册入口](https://gitee.com/)
- 支持手机号、邮箱注册
- 注册流程：填写信息 → 验证 → 完善个人资料

##### Gitee 主要界面说明
- **项目（Project）**：代码仓库
- **问题（Issue）**：项目问题追踪与任务管理
- **合并请求（Pull Request）**：代码协作
- **收藏、Fork、Watch**：功能与 GitHub 类似
- **Gitee Pages**：静态网站托管（个人博客/项目文档）

#### 3. Gitee SSH Key 配置与项目协作

- SSH Key 配置流程与 GitHub 类似（见上方）
- 项目协作流程：
  1. 创建或 Fork 仓库
  2. Clone 到本地
  3. 新建分支开发，提交并推送
  4. 发起合并请求
  5. 参与 Issue 讨论

#### 4. Gitee 特色功能

- 支持企业版和团队协作
- 支持中国主流第三方登录（微信、支付宝等）
- 支持私有仓库免费，适合企业内部项目管理

---

### 第五部分：GitHub 和 Gitee 的核心功能对比

| 功能         | GitHub              | Gitee                |
| ------------ | ------------------- | -------------------- |
| Fork         | 复制项目到个人账户  | 同样支持复制项目     |
| Star         | 收藏项目            | 同样支持收藏项目     |
| Watch        | 订阅项目动态        | 支持订阅             |
| Issues       | 提交问题或建议      | 问题追踪支持更本地化 |
| Pull Request | 提交代码修改和合并  | 类似功能             |
| Actions      | 自动化 CI/CD 工作流 | 不支持 Actions       |
| Pages        | 静态网站托管        | 提供类似功能         |
| Releases     | 发布稳定版本        | 同样支持发布功能     |
| Webhooks     | 自动消息通知        | 支持类似功能         |

****

### 总结

- **Git**：本地代码管理和版本控制工具
- **GitHub**：全球开源协作、作品展示和技术交流平台
- **Gitee**：国内主流代码托管平台，适合本地团队和企业项目协作

**建议：**

- 日常学习和开源项目优先用 GitHub，参与国际技术社区
- 团队/企业项目可选用 Gitee，便于国内协作和访问
- 熟练掌握 Git 命令和 SSH 配置，提升协作效率

****

## Typora 与 Markdown

### Typora 使用教程

#### 安装和激活

- 下载 Typora 安装包，运行后一路点击 OK 即可完成安装。
- 如果需要激活，将文件夹中的 **winmm.dll** 移动到 Typora 的安装路径下（如 D:\Program Files\Typora）。注意此步骤需关闭 Typora 软件，否则会报错。

![image-20251017092741839](/images/Git_Github_Markdown/Git_Github_Markdown_3.png)

---

#### 插件使用

- 推荐安装 [typora_plugin](https://github.com/obgnail/typora_plugin)：可以显著优化 Typora 的使用体验，按官方文档安装即可。
- 论文工具[typora-latex-theme](https://github.com/Keldos-Li/typora-latex-theme)：对于没有学过office三件套或WPS的同学大有帮助。

---

#### 建议配置

##### 侧边栏设置

- 建议将侧边栏打开，便于查看和管理文档结构。
- 在 Typora 主界面点击右下角的 `显示/隐藏侧边栏` 按钮即可。

![image-20251017093303047](/images/Git_Github_Markdown/Git_Github_Markdown_4.png)

---

##### 文件配置

- 进入 Typora 菜单栏 `文件 -> 偏好设置`，进行文件相关配置。
- 推荐按照下图设置，便于文档管理与文件归档。

![image-20251017093318594](/images/Git_Github_Markdown/Git_Github_Markdown_5.png)

---

##### 编辑器配置

- 推荐启用智能缩进、自动补全 Markdown 字符、统一行尾符号等功能，提升编辑效率，减少语法出错。

![image-20251017093327185](/images/Git_Github_Markdown/Git_Github_Markdown_6.png)

---

##### 图片配置

- 插入图片时，建议选择自动复制图片到当前 md 文件同名的 assets 文件夹下，方便文档迁移和分享。  
- 推荐勾选：  
  - 自动上传图片到 assets 文件夹
  - 优化图片路径显示
  - 生成图片相对路径  
- 图片插入后，建议压缩图片或生成缩略图，减少文档体积。

![image-20251017093345944](/images/Git_Github_Markdown/Git_Github_Markdown_7.png)

---

##### Markdown 配置

我们在这里可以配置markdown的语法相关，我的建议是全部勾上（除了那个首行缩进<这是个人喜好

\>），一定勾选上那个图表，这样可以让typora对mermaid等图表代码直接进行渲染，下面的公式编号还是看个人情况，这里就不过多说了

- 建议开启 Typora 对 mermaid 图表和数学公式的支持，方便画流程图和写公式。
- 推荐设置常用语法快捷键，提升编辑效率。

![image-20251017093521861](/images/Git_Github_Markdown/Git_Github_Markdown_8.png)

---

#####  导出配置

- 可根据个人需求设置 PDF 导出参数，包括页面大小、边距等。
- 支持设置 YAML 头信息（如 title、author），导出时自动识别并加到对应位置。

![image-20251017093617999](/images/Git_Github_Markdown/Git_Github_Markdown_9.png)

---

##### 外观配置

- 推荐使用「经典」模式，字体大小和主题可按个人习惯调整，支持多种主题切换（如 HappySimple、Jetbrains Mono Theme 等）。

![image-20251017093703523](/images/Git_Github_Markdown/Git_Github_Markdown_10.png)

- 主题获取途径：
  - [Themes Gallery – Typora](https://theme.typora.io/)
  - GitHub 搜索 typora theme

---

##### 通用配置

![image-20251017093728150](/images/Git_Github_Markdown/Git_Github_Markdown_11.png)

- 建议关闭自动检查更新和开发版更新，稳定性更好。
- 可自定义快捷键，提升操作效率。

---

#### 主题美化

- 推荐主题：
  - **Neil Jetbrains Mono Theme**：适合 Jetbrains 系 IDE 用户，字体美观，界面简洁。
  - **HappySimple**：视觉舒适，适合日常写作和学习。

---

### Markdown 使用教程

#### 一、什么是 Markdown？

Markdown 是一种轻量级的标记语言，设计用于让普通文本具有丰富的格式表现，同时保留文案内容的易读性和易写性。通过简单直观的标记符号实现文档格式化，广泛应用于技术文档、博客文章、电子邮件、笔记和协作文档等。

---

#### 二、为什么选择 Markdown？

1. **简单直观**：语法易学易用，常见标记符号即可快速上手。
2. **跨平台支持**：兼容多种工具和平台，如 GitHub、Notion、VS Code、Jupyter Notebook 等。
3. **多格式输出**：可转为 HTML、PDF、Word 等多种格式，满足不同需求。
4. **专注创作**：无需复杂排版工具，专注内容本身，提升写作效率。

---

#### 三、Markdown 语法详解

##### 1. 标题

使用 `#` 符号表示标题，支持六级标题，`#` 的数量代表标题级别。

```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```
---

##### 2. 段落与换行

普通文本直接书写即可。若需换行，在行尾添加两个空格。

```markdown
这是一段文字，行尾加两个空格后换行。  
这是下一行。
```
---

##### 3. 强调

支持斜体和加粗，以及两者组合。

```markdown
*斜体* 或 _斜体_
**加粗** 或 __加粗__
***斜体加粗*** 或 ___斜体加粗___
```

效果：
- *斜体*
- **加粗**
- ***斜体加粗***

---

##### 4. 列表

支持无序列表和有序列表。

###### 无序列表

使用 `-`、`*` 或 `+` 作为标记符。

```markdown
- 项目一
- 项目二
  - 子项目一
  - 子项目三
* 项目三
```

效果：
- 项目一
- 项目二
  - 子项目一
  - 子项目三
- 项目三

###### 有序列表

使用数字加点 `1.`，数字顺序可不连续，最终会按顺序渲染。

```markdown
1. 项目一
2. 项目二
   1. 子项目一
   2. 子项目二
```

效果：
1. 项目一
2. 项目二
   1. 子项目一
   2. 子项目二

---

##### 5. 链接

添加超链接：

```markdown
[链接文字](链接地址)
[google](https://www.google.com)
```

带标题提示：

```markdown
[链接文字](链接地址 "标题提示")
[google](https://www.google.com "谷歌搜索")
```

效果如下：
[Google](https://www.google.com)
[Google](https://www.google.com "谷歌搜索")

---

##### 6. 图片

添加图片与链接类似，只需在前面加一个 `!`。

```markdown
![图片描述](图片地址)
![鹿乃.jpg](https://s2.loli.net/2024/10/27/I1iqvzVtnxEYuaT.jpg)
```

---

##### 7. 引用

引用使用 `>` 进行标记，支持嵌套引用。

```markdown
> 这是一个引用。
>> 这是嵌套引用。
```

效果：
> 这是一个引用。
> > 这是嵌套引用。

---

##### 8. 代码块

###### 行内代码

用反引号（`）包裹。

```markdown
`这是行内代码` 示例。
```

效果：`这是行内代码` 示例。

###### 多行代码块

用三个反引号（```）包裹，可指定语言高亮。

```markdown
``` python
def hello():
    print("Hello, Markdown!")
```
```

效果如下：

```python
def hello():
    print("Hello, Markdown!")
```

---

##### 9. 表格

使用 `|` 和 `-` 创建表格。

```markdown
| 表头1 | 表头2 | 表头3 |
|-------|-------|-------|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |
```

效果：
| 表头 1 | 表头 2 | 表头 3 |
| ----- | ----- | ----- |
| 数据 1 | 数据 2 | 数据 3 |
| 数据 4 | 数据 5 | 数据 6 |

---

##### 10. 分隔线

用三个或更多的 `-`、`*` 或 `_` 创建分隔线。

```markdown
---
***
___
```

#### 效果如下：

****

#### 任务列表

用 `- [ ]` 创建未完成任务，`- [x]` 创建已完成任务。

```markdown
- [ ] 任务一
- [x] 任务二
- [ ] 任务三
```

效果：
- [ ] 任务一
- [x] 任务二
- [ ] 任务三

---

##### 12. 公式

支持 LaTeX 数学公式（部分编辑器/平台需开启支持）。

```markdown
$\frac{a}{b}$
```

效果：$\frac{a}{b}$

---

##### 13. mermaid 绘图

支持流程图、时序图等（需平台支持）。

```markdown
graph TD
A[串口中断接收] --> B{中断号判断}
B -->|USART1 或 USART2| C[堆栈寄存器压入\n]
C --> B
```

---

### Typora 快捷键速查表

| 功能            | 快捷键（Windows）   | 快捷键（Mac）     | 说明                           |
| --------------- | ------------------- | ----------------- | ------------------------------ |
| 加粗            | Ctrl + B            | Cmd + B           | 选中内容加粗                   |
| 斜体            | Ctrl + I            | Cmd + I           | 选中内容斜体                   |
| 插入标题        | Ctrl + 1 ~ Ctrl + 6 | Cmd + 1 ~ Cmd + 6 | 对应一级至六级标题             |
| 插入无序列表    | Ctrl + Shift + U    | Cmd + Shift + U   | 快速插入无序列表               |
| 插入有序列表    | Ctrl + Shift + O    | Cmd + Shift + O   | 快速插入有序列表               |
| 插入任务列表    | Ctrl + Shift + C    | Cmd + Shift + C   | 插入 `- [ ]` 任务项            |
| 插入代码块      | Ctrl + Shift + K    | Cmd + Option + K  | 插入三反引号代码块（块级代码） |
| 插入行内代码    | Ctrl + E            | Cmd + E           | 插入行内代码（单反引号）       |
| 插入图片        | Ctrl + Shift + I    | Cmd + Shift + I   | 打开插入图片对话框             |
| 插入链接        | Ctrl + K            | Cmd + K           | 插入超链接                     |
| 插入引用        | Ctrl + Shift + Q    | Cmd + Shift + Q   | 插入引用 >                     |
| 插入表格        | Ctrl + T            | Cmd + T           | 打开插入表格面板               |
| 插入公式        | Ctrl + Shift + M    | Cmd + Shift + M   | 插入公式块（$$）               |
| 插入Mermaid图   | Ctrl + Shift + G    | Cmd + Shift + G   | 插入mermaid绘图代码块          |
| 切换专注模式    | F8                  | F8                | 切换专注模式（Focus Mode）     |
| 打开/关闭侧边栏 | Ctrl + /            | Cmd + /           | 显示或隐藏左侧目录栏           |
| 查找            | Ctrl + F            | Cmd + F           | 查找文本                       |
| 替换            | Ctrl + H            | Cmd + Option + F  | 查找并替换文本                 |
| 保存            | Ctrl + S            | Cmd + S           | 保存文档                       |
| 导出            | Ctrl + Shift + E    | Cmd + Shift + E   | 导出为PDF、HTML等格式          |
| 打开偏好设置    | Ctrl + ,            | Cmd + ,           | 打开Typora设置                 |
| 新建文档        | Ctrl + N            | Cmd + N           | 新建一个空白文档               |
| 打开文档        | Ctrl + O            | Cmd + O           | 打开本地文档                   |
| 关闭文档        | Ctrl + W            | Cmd + W           | 关闭当前标签页                 |

> **提示：**  
> Typora 支持自定义快捷键，部分功能可在 “偏好设置” > “快捷键”中自定义。  
> 常用操作如插入代码块、插入图片、切换侧边栏等快捷键建议多加练习，提升效率。



---

## 插件与刷课脚本部分

### 一、浏览器插件简介

#### 1. 什么是浏览器插件？

浏览器插件（扩展）是一种可以为浏览器增加新功能的小型程序。它们能够帮助用户实现自动化、界面美化、广告屏蔽、脚本自定义等功能，极大提升日常上网体验和效率。

---

#### 2. 油猴（Tampermonkey）与篡改猴（Violentmonkey）简介与对比

**油猴（Tampermonkey）** 和 **篡改猴（Violentmonkey）** 都是浏览器端最主流的用户脚本管理器插件，能够让用户轻松安装、管理和运行自定义脚本（如刷课、自动答题、网页优化等）。

|          | 油猴（Tampermonkey）        | 篡改猴（Violentmonkey）    |
| -------- | --------------------------- | -------------------------- |
| 兼容性   | Chrome/Edge/Firefox/Safari  | Chrome/Edge/Firefox/Opera  |
| 界面     | 功能丰富，设置选项更多      | 界面简洁，轻量，易用       |
| 脚本支持 | 支持几乎所有主流用户脚本    | 支持大部分脚本，兼容性优秀 |
| 开发者   | 国外团队                    | 国外团队（有国人参与）     |
| 推荐场景 | 需要高级管理/脚本较多的用户 | 追求简洁/轻量的用户        |

**小结：**
- 油猴（Tampermonkey）适合大多数用户，功能更全，兼容性最好，推荐新手优先选择。
- 篡改猴（Violentmonkey）更轻量，界面简洁，资源占用更低。

---

#### 3. 安装方法

**a. Chrome 浏览器：**
- 推荐前往 [crx搜搜插件网](https://www.crxsoso.com/search) 搜索「Tampermonkey」或「Violentmonkey」并下载安装（国内无需科学上网）。

  > 聚合了 Chrome、Edge、Firefox 各类插件和油猴脚本，国内访问速度快，适合查找各类扩展和脚本。

- 也可去 [Chrome Web Store](https://chrome.google.com/webstore/) 安装（需科学上网）。

**b. Edge 浏览器：**
- 可在 Edge 插件商店或 crx搜搜 搜索并安装。

**c. Firefox 浏览器：**
- 前往 [Firefox 附加组件](https://addons.mozilla.org/) 搜索并安装。

---

### OCS网课助手与刷课脚本

#### OCS网课助手简介

OCS网课助手是一款专为网课平台（如超星、智慧树、学堂在线等）开发的刷课插件，能实现自动播放、刷视频、自动答题等功能，大大提高网课学习效率。适合需要快速完成网课任务的同学。

- **官网/项目主页**：[OCS网课助手](https://docs.ocsjs.com/)
- **主要功能**：
  - 自动刷视频、自动答题、自动过考试
  - 支持多个主流网课平台
  - 可配合题库使用（如教材/言溪题库等）

#### 言溪题库简介

- **官网主页**：[言溪题库](https://tk.enncy.cn/)

- 提供超星、智慧树等平台的题目答案，可提升刷课和自动答题的正确率。
- 常见用法：在 OCS 等刷课插件设置里绑定题库接口，或手动查找题目答案。

#### WE Learn & U校园刷课脚本与教程

- **EOC 一站式刷课脚本合集**：[EOC项目主页](https://ssmjae.github.io/EOC/)
  - 该网站提供了针对多种主流校园网课平台（如 WE Learn、U校园等）的刷课脚本及详细教程。
  - 主要功能包括：
    - 自动刷视频、自动答题、自动完成作业、考试辅助等
    - 支持多平台、多类型课程的自动化处理
    - 提供详细的安装流程、脚本下载链接、常见问题解答
  - 网站内容持续更新，适合自助查找和学习刷课自动化工具

**使用建议：**
- 进入 EOC 项目主页后，根据你的网课平台（如 WE Learn、U校园）选择对应脚本和教程，按照页面说明进行安装和使用。
- 建议优先使用油猴（Tampermonkey）或篡改猴（Violentmonkey）插件进行脚本管理，确保兼容性和脚本运行稳定。
- 脚本仅供学习和便捷课程管理使用，切勿用于违规用途。

---

**实用建议：**

- 插件和脚本建议只从知名平台和官方渠道下载，避免安全风险。
- 使用脚本前请详细阅读说明，注意账号安全，不要泄露个人信息。
- 刷课脚本仅供学习交流，勿用于违规用途。

