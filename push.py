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


def remove_deleted_index_entries(cwd: str | None = None) -> None:
    """从 Git 索引中移除那些已被删除（在索引中但工作区不存在）的文件。

    这样可以避免在后续运行 `git add --renormalize .` 时因为某些文件在工作区缺失而导致的 stat 错误。
    如果没有删除的索引项，函数静默返回。
    """
    # 使用原生 subprocess 调用以捕获输出（run() 会在失败时抛出，
    # 但 ls-files --deleted 在正常情况下会返回 0）
    try:
        proc = subprocess.run(
            ['git', 'ls-files', '--deleted', '-z'],
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
    except subprocess.CalledProcessError:
        # 无法列出已删除文件（非 git 仓库或其他问题），直接返回
        return

    out = proc.stdout
    if not out:
        return

    # 输出以 NUL 分隔
    paths = [p for p in out.split('\0') if p]
    for p in paths:
        # 对于每个路径，从索引中移除（--ignore-unmatch 保证即使路径不存在也不报错）
        try:
            run(['git', 'rm', '--cached', '--ignore-unmatch', p], cwd=cwd)
        except subprocess.CalledProcessError:
            # 若某条移除失败，继续处理其余文件
            print(f'警告：尝试从索引移除 {p} 时失败，继续处理其它文件')

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
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def main() -> None:
    repo = Path.cwd()
    public = repo / 'public'
    images = repo / 'source' / 'images' 
    if not repo.exists():
        print('错误：找不到当前工作目录', file=sys.stderr)
        sys.exit(1)

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Deploy: {ts}'

    try:
        run('hexo clean', shell=True)
        run('hexo g', shell=True)

        if images.exists():
            copy_tree(images, public / 'images')
    except subprocess.CalledProcessError:
        print('Hexo 构建失败，取消部署', file=sys.stderr)
        sys.exit(1)

    # 2) 提交源码并推送到 data 分支
    try:
        # 统一根仓库换行符设置，避免 CRLF 提示
        run(['git', 'config', 'core.autocrlf', 'false'])
        run(['git', 'config', 'core.eol', 'lf'])
        run(['git', 'config', 'core.safecrlf', 'false'])

        # 在运行 git add 之前，检查索引中是否有在工作区被删除的文件，
        # 如果有则列出并询问用户是否确认从索引中移除并继续上传。
        try:
            proc = subprocess.run(
                ['git', 'ls-files', '--deleted', '-z'],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo),
            )
            deleted_out = proc.stdout
        except subprocess.CalledProcessError:
            deleted_out = ''

        if deleted_out:
            deleted_paths = [p for p in deleted_out.split('\0') if p]
            print('\n发现以下在索引中但工作区已删除的文件：')
            for p in deleted_paths:
                print('  -', p)
            # 交互式确认
            ans = input('\n是否从索引中移除这些文件并继续上传？(y/n): ').strip().lower()
            if ans == 'y':
                remove_deleted_index_entries(cwd=str(repo))
            else:
                print('已取消：未执行上传')
                sys.exit(0)

        # 使用 --renormalize 按照 .gitattributes 规范化索引中的换行符（首次执行可能会有少量文件变更）
        run(['git', 'add', '--renormalize', '.'])
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

        # 每次运行都统一换行符设置（避免早期创建的 .deploy_git 没有配置导致的 CRLF 警告）
        run(['git', 'config', 'core.autocrlf', 'false'], cwd=str(deploy_dir))
        run(['git', 'config', 'core.eol', 'lf'], cwd=str(deploy_dir))
        run(['git', 'config', 'core.safecrlf', 'false'], cwd=str(deploy_dir))

        # 获取远端 main 分支最新状态（若失败则尝试回退策略）
        fetch_succeeded = False
        try:
            run(['git', 'fetch', 'origin', 'main'], cwd=str(deploy_dir))
            fetch_succeeded = True
        except subprocess.CalledProcessError:
            # 首次 fetch 失败，可能是 SSH 认证/网络问题，尝试把 remote 切换为 HTTPS 并重试
            print('警告：首次 fetch origin main 失败，尝试将 remote 切换为 HTTPS 并重试')
            https_url = None
            try:
                # origin_url 在外层已读取为字符串
                if origin_url.startswith('git@') and ':' in origin_url:
                    # git@github.com:owner/repo.git -> https://github.com/owner/repo.git
                    host_path = origin_url.split(':', 1)[1]
                    host = origin_url.split('@', 1)[1].split(':', 1)[0]
                    https_url = f'https://{host}/{host_path}'
                elif origin_url.startswith('ssh://'):
                    # ssh://git@github.com/owner/repo.git -> https://github.com/owner/repo.git
                    parts = origin_url.split('://', 1)[1]
                    if '@' in parts:
                        parts = parts.split('@', 1)[1]
                    https_url = 'https://' + parts
                elif origin_url.startswith('https://'):
                    https_url = origin_url
            except Exception:
                https_url = None

            if https_url:
                try:
                    run(['git', 'remote', 'set-url', 'origin', https_url], cwd=str(deploy_dir))
                    run(['git', 'fetch', 'origin', 'main'], cwd=str(deploy_dir))
                    fetch_succeeded = True
                except subprocess.CalledProcessError:
                    print('尝试使用 HTTPS fetch 仍然失败')
            else:
                print('无法将 origin URL 转换为 HTTPS，跳过 HTTPS 重试')

        # 根据 fetch 结果选择 checkout 策略：
        if fetch_succeeded:
            # 基于远端 main 创建/重置本地 main
            run(['git', 'checkout', '-B', 'main', 'origin/main'], cwd=str(deploy_dir))
        else:
            # fetch 失败：优先使用已有本地分支（若存在），否则创建或重置孤儿分支
            try:
                # 如果本地已有 main 分支则切换到该分支并继续
                run(['git', 'rev-parse', '--verify', 'main'], cwd=str(deploy_dir))
                run(['git', 'checkout', 'main'], cwd=str(deploy_dir))
            except subprocess.CalledProcessError:
                # main 不存在，使用孤儿分支
                try:
                    run(['git', 'checkout', '--orphan', 'main'], cwd=str(deploy_dir))
                except subprocess.CalledProcessError as exc:
                    # 无法创建孤儿分支，给出明确错误信息并中止
                    print('无法准备本地 main 分支用于发布（fetch 和创建孤儿分支均失败）：', exc, file=sys.stderr)
                    sys.exit(1)

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
