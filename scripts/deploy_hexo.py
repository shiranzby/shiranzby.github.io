#!/usr/bin/env python3
r"""
deploy_hexo.py

用途：在 Windows PowerShell 下自动化 Hexo 的常规发布流程：
  1. （可选）hexo clean
  2. hexo generate
  3. 将生成的静态内容与源码一起提交并推送到远端分支，或使用 `hexo d` 自动部署

用法示例（PowerShell）：
  python .\scripts\deploy_hexo.py --message "更新博客" 

常用选项：
  --no-clean        跳过 `hexo clean`
  --use-deploy      使用 `hexo d` 而非手动 git push
  --branch BR       推送到的分支（默认: main）
  --remote-url URL  若本地未配置 origin，可传入远端仓库 URL 并配合 --init 使用
  --init            当没有 git 仓库时，初始化 git 并添加 origin（需要同时指定 --remote-url）

假设：本地环境已安装 hexo、git，并可在 PATH 中直接调用。若没有，请先安装并配置好 git/hexo。
"""

import argparse
import os
import subprocess
import sys
from shutil import which


DRY_RUN = False


def run(cmd, cwd=None, check=True):
    """Run a shell command and stream output. If DRY_RUN is True, just print the command."""
    print(f"> {cmd}")
    if DRY_RUN:
        # Return a CompletedProcess-like object with returncode 0
        return subprocess.CompletedProcess(args=cmd, returncode=0)
    result = subprocess.run(cmd, shell=True, cwd=cwd, text=True)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def has_executable(name):
    return which(name) is not None


def is_git_repo(path):
    try:
        subprocess.run('git rev-parse --is-inside-work-tree', shell=True, cwd=path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def get_current_branch(path):
    try:
        out = subprocess.check_output('git branch --show-current', shell=True, cwd=path, text=True)
        return out.strip() or None
    except subprocess.CalledProcessError:
        return None


def has_remote_origin(path):
    try:
        subprocess.check_output('git remote get-url origin', shell=True, cwd=path, text=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    parser = argparse.ArgumentParser(description='Hexo 常规流程部署脚本（clean -> generate -> git push/hexo d）')
    parser.add_argument('--no-clean', action='store_true', help='跳过 hexo clean')
    parser.add_argument('--use-deploy', action='store_true', help='使用 hexo d 进行部署（代替 git commit/push）')
    parser.add_argument('--branch', default='main', help='推送目标分支（默认: main）')
    parser.add_argument('--dry-run', action='store_true', help='仅打印将要运行的命令，不实际执行')
    parser.add_argument('--remote-url', help='若本地没有 origin，可传入远端 URL（配合 --init）')
    parser.add_argument('--init', action='store_true', help='当不存在 git 仓库时进行 git init 并配置 origin（需同时指定 --remote-url）')
    parser.add_argument('--message', default='更新: Hexo 站点', help='git commit 消息')
    parser.add_argument('--hexo-cmd', default='hexo', help='hexo 可执行命令（默认: hexo）')
    parser.add_argument('--cwd', default='.', help='在指定路径下运行（默认: 当前目录）')

    args = parser.parse_args()
    root = os.path.abspath(args.cwd)

    # enable dry-run flag globally
    global DRY_RUN
    DRY_RUN = bool(args.dry_run)

    print(f"工作目录: {root}")

    # 检查 hexo 可用
    if not has_executable(args.hexo_cmd.split()[0]):
        print(f"警告: 找不到可执行的 '{args.hexo_cmd}'. 请确认 hexo 已安装并在 PATH 中。")
        # 继续但许多操作会失败

    # 1. clean
    try:
        if not args.no_clean:
            print('\n==> 运行 hexo clean')
            run(f'{args.hexo_cmd} clean', cwd=root)
        else:
            print('\n==> 跳过 hexo clean')

        # 2. generate
        print('\n==> 运行 hexo generate')
        run(f'{args.hexo_cmd} g', cwd=root)

        if args.use_deploy:
            print('\n==> 使用 hexo d 部署')
            run(f'{args.hexo_cmd} d', cwd=root)
            print('\n部署完成（hexo d）')
            return 0

        # 3. Git: add, commit, push
        print('\n==> 检查 git 仓库状态')
        if not is_git_repo(root):
            if args.init:
                if not args.remote_url:
                    print('错误: 要自动初始化 git 并推送，需要传入 --remote-url')
                    return 2
                print('为当前目录初始化 git 仓库...')
                run('git init', cwd=root)
                run('git add -A', cwd=root)
                run(f'git commit -m "initial commit"', cwd=root)
                run(f'git remote add origin {args.remote_url}', cwd=root)
            else:
                print('错误: 当前目录不是 git 仓库。要自动初始化并设置远端，请使用 --init --remote-url <URL>，或手动运行 git init/配置远端后重试。')
                return 3

        # ensure branch
        branch = get_current_branch(root) or args.branch
        print(f'将推送到分支: {branch}')

        # check remote
        if not has_remote_origin(root):
            if args.remote_url:
                print('检测到无 origin，添加远端...')
                run(f'git remote add origin {args.remote_url}', cwd=root)
            else:
                print('错误: 未检测到 remote origin，请先配置远端（或传入 --remote-url）')
                return 4

        # git add & commit
        print('\n==> git add/commit')
        run('git add -A', cwd=root)
        # commit may fail if no changes; don't treat that as fatal
        try:
            run(f'git commit -m "{args.message}"', cwd=root)
        except subprocess.CalledProcessError:
            print('提示: 没有需要提交的改动（或 commit 被拒绝），继续尝试 push')

        # push
        print('\n==> git push')
        # set upstream if needed
        try:
            run(f'git push origin {branch}', cwd=root)
        except subprocess.CalledProcessError:
            print('尝试使用 -u 选项创建上游分支并推送')
            run(f'git push -u origin {branch}', cwd=root)

        print('\n全部完成。')
        return 0

    except subprocess.CalledProcessError as e:
        print(f'命令执行失败: {e.cmd} (exit {e.returncode})')
        return e.returncode


if __name__ == '__main__':
    sys.exit(main())
