#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import shutil


dotfile_folder = '~/code/dotfiles'
dotfiles = {
    # file in dotfile_folder : destination
    'gitconfig': '~/.gitconfig',
    'githelpers': '~/.githelpers',
    'gitignore': '~/.gitignore',
    'ncmpcpp_config': '~/.config/ncmpcpp/config',
    'screenrc': '~/.screenrc',
    'skel': '~/.vim/skel',
    'vimrc': '~/.vimrc',
    'xinitrc': '~/.xinitrc',
    'Xresources': '~/.Xresources',
    'zshrc': '~/.zshrc',
}

ok = '\33[32m::\33[1;0m'
error = '\33[31m::\33[1;0m'


def ask_overwrite(dst):
    choice = input('{} Overwrite {}? [y|N] '.format(ok, dst)).lower()
    if choice in ['yes', 'y']:
        return True
    return False


def list_dotfiles():
    max_length = max(len(value) for value in dotfiles.values())

    # sort output by lowercase value
    for src, dst in sorted(dotfiles.items(), key=lambda x: x[1].lower()):
        print('{0:{1}} <- {2}'.format(dst, max_length,
                                      os.path.join(dotfile_folder, src)))


def main():
    if args.list:
        list_dotfiles()
        sys.exit()

    for key, value in sorted(dotfiles.items(), key=lambda x: x[0].lower()):
        src = os.path.join(os.path.expanduser(dotfile_folder), key)
        dst = os.path.expanduser(value)

        # continue if source file does not exist
        if not os.path.exists(src):
            print('{} {} does not exist'.format(error, src))
            continue

        # continue if src already symlinked to dst
        if os.path.realpath(dst) == src:
            if args.verbose:
                print('{} {} already linked to {}'.format(
                    ok, os.path.basename(src), dst))
            continue

        # create symlink if destination file does not exist
        if not os.path.exists(dst):
            os.symlink(src, dst)
            print('{} Linked {} to {}'.format(ok, src, dst))
            continue

        # unless force option is set, ask for overwrite if destination exists
        if args.force or ask_overwrite(dst):
            shutil.rmtree(dst, ignore_errors=True)
            os.symlink(src, dst)
            print('{} Linked {} to {}'.format(ok, src, dst))
            continue
        else:
            print('{} Skipped {}'.format(error, dst))
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Symlink dotfiles.')
    parser.add_argument(
            '-f', '--force',
            dest='force',
            help='overwrite existing symlinks without asking',
            default=False,
            action='store_true')
    parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            help='verbose output',
            default=False,
            action='store_true')
    parser.add_argument(
            '-l', '--list',
            dest='list',
            help='list dotfiles and exit',
            default=False,
            action='store_true')
    args = parser.parse_args()
    main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
