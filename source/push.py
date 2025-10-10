#!/usr/bin/env python3
"""Deploy helper (simple):
- Run `hexo clean` and `hexo g` (use local node_modules hexo when available)
- Commit current source with a timestamped message and push to `data` branch
- Create an orphan branch, replace repository root with `public/` contents,
  then force-push that orphan to `origin/main` to update GitHub Pages.

Usage (run from repository root):
    python .\source\push.py

Warning: this script will switch branches and overwrite working tree files.
Make sure you saved or committed any important changes.
"""
from __future__ import annotations
import subprocess
import sys
import shutil
from datetime import datetime
from pathlib import Path


def run(cmd, cwd: str | None = None, shell: bool = False):
    # cmd can be a list or a string. When shell=True we pass a string to the shell.
    if isinstance(cmd, (list, tuple)) and not shell:
        print('> ' + ' '.join(cmd))
        subprocess.run(cmd, check=True, cwd=cwd)
    else:
        # ensure we have a string for shell execution
        cmdstr = cmd if isinstance(cmd, str) else ' '.join(cmd)
        print('> ' + cmdstr)
        subprocess.run(cmdstr, check=True, cwd=cwd, shell=True)


def find_hexo_cmd(repo: Path) -> str | None:
    win = repo / 'node_modules' / '.bin' / 'hexo.cmd'
    unix = repo / 'node_modules' / '.bin' / 'hexo'
    if win.exists():
        return str(win)
    if unix.exists():
        return str(unix)
    return None


def main() -> None:
    repo = Path.cwd()
    public = repo / 'public'
    if not repo.exists():
        print('错误：找不到当前工作目录', file=sys.stderr)
        sys.exit(1)

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Deploy: {ts}'

    # 1) hexo clean && hexo g
    hexo_cmd = find_hexo_cmd(repo)
    try:
        if hexo_cmd:
            run([hexo_cmd, 'clean'])
            run([hexo_cmd, 'g'])
        else:
            # on Windows npx may be a ps1 script, use shell=True
            run('npx hexo clean', shell=True)
            run('npx hexo g', shell=True)
    except subprocess.CalledProcessError:
        print('Hexo 构建失败，取消部署', file=sys.stderr)
        sys.exit(1)

    # 2) commit current source and push to data branch
    try:
        run(['git', 'add', '-A'])
        try:
            run(['git', 'commit', '-m', msg])
        except subprocess.CalledProcessError:
            # allow empty commit (no changes)
            run(['git', 'commit', '--allow-empty', '-m', msg])
        run(['git', 'push', 'origin', 'HEAD:refs/heads/data'])
    except subprocess.CalledProcessError:
        print('将源码推送到 data 分支失败', file=sys.stderr)
        sys.exit(1)

    # 3) publish public by creating an orphan branch and force-push to main
    if not public.exists():
        print('警告：public/ 不存在，跳过 public 推送')
        return

    try:
        # record current branch
        cur_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError:
        print('无法读取当前分支，取消 public 推送', file=sys.stderr)
        return

    orphan = f'publish-orphan-{datetime.now().strftime("%Y%m%d%H%M%S")}'

    try:
        # create orphan branch
        run(['git', 'checkout', '--orphan', orphan])
        run(['git', 'reset', '--hard'])

        # remove all files except .git
        for p in Path.cwd().iterdir():
            if p.name == '.git':
                continue
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

        # copy public content to repo root
        for item in public.iterdir():
            dest = Path.cwd() / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        run(['git', 'add', '-A'])
        try:
            run(['git', 'commit', '-m', msg])
        except subprocess.CalledProcessError:
            run(['git', 'commit', '--allow-empty', '-m', msg])

        run(['git', 'push', 'origin', f'{orphan}:refs/heads/main', '--force'])

    except subprocess.CalledProcessError as exc:
        print('public 推送失败：', exc, file=sys.stderr)
        try:
            run(['git', 'checkout', cur_branch])
        except Exception:
            pass
        sys.exit(1)
    finally:
        # restore and delete orphan
        try:
            run(['git', 'checkout', cur_branch])
        except subprocess.CalledProcessError:
            print('恢复原分支失败，请手动检查仓库状态', file=sys.stderr)
        try:
            run(['git', 'branch', '-D', orphan])
        except subprocess.CalledProcessError:
            pass

    print('完成：源码已推 data 分支；public 已强制推到 origin/main')


if __name__ == '__main__':
    main()
