#!/usr/bin/env python3
"""部署辅助（简洁）
- 运行 `hexo clean` 和 `hexo g` 生成 `public/`
- 提交源码并推送到 `data` 分支
- 在临时独立仓库中提交 `public/` 并强推到 `origin/main`（发布用），运行后不会在本地留下临时分支

用法（在仓库根目录运行）:
    python ./source/push.py

注意：脚本会进行强推到远端 main，请提前确认备份或接受覆盖风险。
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

    # 3) 发布 public 到 main（使用临时独立仓库，不在主仓库留下分支）
    if not public.exists():
        print('警告：public/ 不存在，跳过 public 推送')
        return

    try:
    # 记录当前分支（仅做信息用途）
        cur_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError:
        print('无法读取当前分支，取消 public 推送', file=sys.stderr)
        return

    orphan = f'publish-orphan-{datetime.now().strftime("%Y%m%d%H%M%S")}'

    # 使用临时独立仓库发布 public/：在临时目录初始化仓库，提交 public 后强推到 origin/main，
    # 推送完成后删除临时目录，避免在本地留下分支或 worktree 引用。
    import tempfile

    tmpdir = Path(tempfile.mkdtemp(prefix='publish_tmprepo_'))
    try:
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

        # 在临时目录初始化仓库并关联 origin
        run(['git', 'init'], cwd=str(tmpdir))
        run(['git', 'remote', 'add', 'origin', origin_url], cwd=str(tmpdir))
        # 设置临时仓库的提交身份
        run(['git', 'config', 'user.name', 'auto-deploy'], cwd=str(tmpdir))
        run(['git', 'config', 'user.email', 'auto-deploy@local'], cwd=str(tmpdir))

        # 复制 public 内容到临时仓库
        for item in public.iterdir():
            dest = tmpdir / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        # 在临时仓库提交并强推到 origin/main；不会在主仓库留下引用
        run(['git', 'add', '-A'], cwd=str(tmpdir))
        try:
            run(['git', 'commit', '-m', msg], cwd=str(tmpdir))
        except subprocess.CalledProcessError:
            run(['git', 'commit', '--allow-empty', '-m', msg], cwd=str(tmpdir))

        # 强制推送临时仓库的 HEAD 到 origin/main（与之前行为一致）
        run(['git', 'push', 'origin', 'HEAD:refs/heads/main', '--force'], cwd=str(tmpdir))

    except subprocess.CalledProcessError as exc:
        print('public 推送失败：', exc, file=sys.stderr)
        sys.exit(1)
    finally:
        # 删除临时目录
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass

    print('完成：源码已推 data 分支；public 已强制推到 origin/main')


if __name__ == '__main__':
    main()
