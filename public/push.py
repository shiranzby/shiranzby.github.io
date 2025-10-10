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



def main() -> None:
    repo = Path.cwd()
    public = repo / 'public'
    if not repo.exists():
        print('错误：找不到当前工作目录', file=sys.stderr)
        sys.exit(1)

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Deploy: {ts}'

    # 1) hexo clean && hexo g (直接使用 shell 中的 hexo，用户已确认可用)
    try:
        run('hexo clean', shell=True)
        run('hexo g', shell=True)
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

    # Use git worktree to stage public content in a detached worktree and push it
    import tempfile

    tmpdir = Path(tempfile.mkdtemp(prefix='publish_worktree_'))
    try:
        # create an orphan branch in the worktree
        run(['git', 'worktree', 'add', '--detach', str(tmpdir), orphan])

        # copy public content into the worktree
        for item in public.iterdir():
            dest = tmpdir / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        # commit and push from the worktree
        run(['git', 'add', '-A'], cwd=str(tmpdir))
        try:
            run(['git', 'commit', '-m', msg], cwd=str(tmpdir))
        except subprocess.CalledProcessError:
            run(['git', 'commit', '--allow-empty', '-m', msg], cwd=str(tmpdir))
        run(['git', 'push', 'origin', f'{orphan}:refs/heads/main', '--force'], cwd=str(tmpdir))

    except subprocess.CalledProcessError as exc:
        print('public 推送失败：', exc, file=sys.stderr)
        sys.exit(1)
    finally:
        # remove the worktree and temporary dir
        try:
            run(['git', 'worktree', 'remove', str(tmpdir), '--force'])
        except subprocess.CalledProcessError:
            pass
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass

    print('完成：源码已推 data 分支；public 已强制推到 origin/main')


if __name__ == '__main__':
    main()
