#!/usr/bin/env python3
"""部署辅助（增量 + 可强制刷新）
- 运行 `hexo clean` 和 `hexo g` 生成 `public/`
- 提交源码并推送到 `data` 分支
- 增量发布：使用本地 `.deploy_git` 作为发布仓库缓存，提交 `public/` 到远端 `main`（不再 --force）
    - 由于保留了历史，推送将是增量（只上传变更的对象），大幅减少流量
    - 若本次没有任何文件变化，仍会创建空提交以触发 GitHub Pages 再发布，实现“强制刷新”

用法（在仓库根目录运行）:
        python ./push.py
"""
from __future__ import annotations
import subprocess
import sys
import shutil
from datetime import datetime
from pathlib import Path


def run(cmd, cwd: str | None = None, shell: bool = False):
    # cmd 可以是 list 或 str；当 shell=True 时传入字符串执行。
    if isinstance(cmd, (list, tuple)) and not shell:
        print('> ' + ' '.join(cmd))
        subprocess.run(cmd, check=True, cwd=cwd)
    else:
        # ensure we have a string for shell execution
        cmdstr = cmd if isinstance(cmd, str) else ' '.join(cmd)
        print('> ' + cmdstr)
        subprocess.run(cmdstr, check=True, cwd=cwd, shell=True)

def clean_dir_keep_git(path: Path) -> None:
    """删除给定目录下除 .git 外的所有内容。"""
    for item in path.iterdir():
        if item.name == '.git':
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def copy_tree(src: Path, dst: Path) -> None:
    """将 src 下的内容复制到 dst（覆盖同名文件）。"""
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            # 确保父目录存在
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def main() -> None:
    repo = Path.cwd()
    public = repo / 'public'
    if not repo.exists():
        print('错误：找不到当前工作目录', file=sys.stderr)
        sys.exit(1)

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Deploy: {ts}'

    try:
        run('hexo clean', shell=True)
        run('hexo g', shell=True)
    except subprocess.CalledProcessError:
        print('Hexo 构建失败，取消部署', file=sys.stderr)
        sys.exit(1)

    # 2) 提交源码并推送到 data 分支
    try:
        run(['git', 'add', '-A'])
        try:
            run(['git', 'commit', '-m', msg])
        except subprocess.CalledProcessError:
            # 允许空提交（无改动）
            run(['git', 'commit', '--allow-empty', '-m', msg])
        run(['git', 'push', 'origin', 'HEAD:refs/heads/data'])
    except subprocess.CalledProcessError:
        print('将源码推送到 data 分支失败', file=sys.stderr)
        sys.exit(1)

    # 3) 发布 public 到 main（使用持久化的 .deploy_git 仓库进行增量推送）
    if not public.exists():
        print('警告：public/ 不存在，跳过 public 推送')
        return

    # 读取远端 origin URL
    try:
        origin_url = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        print('无法读取远端 origin URL，取消 public 推送', file=sys.stderr)
        return

    deploy_dir = repo / '.deploy_git'
    deploy_dir.mkdir(exist_ok=True)

    try:
        # 如果 .deploy_git 不是一个 git 仓库，初始化并关联远端
        if not (deploy_dir / '.git').exists():
            run(['git', 'init'], cwd=str(deploy_dir))
            run(['git', 'remote', 'add', 'origin', origin_url], cwd=str(deploy_dir))
            run(['git', 'config', 'user.name', 'auto-deploy'], cwd=str(deploy_dir))
            run(['git', 'config', 'user.email', 'auto-deploy@local'], cwd=str(deploy_dir))
            # 统一换行符，避免 Windows 上的 CRLF 提示与不必要差异
            run(['git', 'config', 'core.autocrlf', 'false'], cwd=str(deploy_dir))
            run(['git', 'config', 'core.eol', 'lf'], cwd=str(deploy_dir))

        # 获取远端 main 分支最新状态（若不存在将忽略错误）
        try:
            run(['git', 'fetch', 'origin', 'main'], cwd=str(deploy_dir))
            # 基于远端 main 创建/重置本地 main
            run(['git', 'checkout', '-B', 'main', 'origin/main'], cwd=str(deploy_dir))
        except subprocess.CalledProcessError:
            # 远端还没有 main：使用孤儿分支
            run(['git', 'checkout', '--orphan', 'main'], cwd=str(deploy_dir))

        # 清空工作区（保留 .git），复制 public 内容
        clean_dir_keep_git(deploy_dir)
        copy_tree(public, deploy_dir)

        # 提交并推送（无变更时也做空提交以触发 Pages 刷新）
        run(['git', 'add', '-A'], cwd=str(deploy_dir))
        try:
            run(['git', 'commit', '-m', msg], cwd=str(deploy_dir))
        except subprocess.CalledProcessError:
            # 无变更时强制空提交，保证触发部署，达到“强制刷新”目的
            run(['git', 'commit', '--allow-empty', '-m', msg], cwd=str(deploy_dir))

        # 正常推送（不 --force），这样是增量上传
        run(['git', 'push', 'origin', 'main'], cwd=str(deploy_dir))

    except subprocess.CalledProcessError as exc:
        print('public 推送失败：', exc, file=sys.stderr)
        sys.exit(1)

    print('完成：源码已推 data 分支；public 已增量推送到 origin/main')


if __name__ == '__main__':
    main()
