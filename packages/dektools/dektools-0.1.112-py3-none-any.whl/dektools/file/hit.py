import os
import re
import shutil
import tempfile

from igittigitt import IgnoreParser
from .path import normal_path, new_empty_path
from .operation import read_lines, merge_move, remove_path, write_file, list_dir, sure_dir


class FileHitChecker:
    def __init__(self, src_dir, *ignore_file_list, rules=None):
        self.src_dir = normal_path(src_dir)
        self.parser = IgnoreParser()
        for ignore_file in ignore_file_list:
            for rule in read_lines(normal_path(os.path.join(src_dir, ignore_file)), skip_empty=True, default=''):
                if not rule.startswith('#'):
                    self.parser.add_rule(rule, src_dir)
        if rules:
            for rule in rules:
                self.parser.add_rule(rule, src_dir)

    @property
    def shutil_ignore(self):
        return self.parser.shutil_ignore

    def is_hit(self, path):
        path = normal_path(path)
        return self.parser.match(path)

    def is_hit_strict(self, path):
        cursor = normal_path(path)
        positive = False
        while cursor != self.src_dir:
            if self.parser._match_negation_rules(cursor):
                return False
            positive = positive or self.parser._match_rules(cursor, os.path.isfile(cursor))
            cursor = os.path.dirname(cursor)
        if positive:
            return True
        return False

    def walk(self, func):
        def wrapper(path):
            for fn in os.listdir(path):
                fp = os.path.join(path, fn)
                func(fp, self.is_hit_strict(fp), fp[len(self.src_dir) + 1:])
                if os.path.isdir(fp):
                    wrapper(fp)

        if os.path.exists(self.src_dir):
            wrapper(self.src_dir)

    def merge_dir(self, dest, ignores=None):
        dp = new_empty_path(dest)
        self.write_dir(dp, ignores)
        merge_move(dest, dp)
        remove_path(dp)

    def write_dir(self, dest=None, ignores=None):
        def shutil_ignore(base_dir, file_names):
            result = set()
            for ignore in ignores:
                if base_dir.endswith(ignore):
                    result |= set(file_names)
                elif ignore in file_names:
                    result |= {ignore}
            return result | self.parser.shutil_ignore(base_dir, file_names)

        ignores = ignores or []
        if dest is None:
            dest = tempfile.mkdtemp()
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        shutil.copytree(self.src_dir, dest, ignore=shutil_ignore)
        return dest


class ReHitChecker:
    @classmethod
    def form_file(cls, *filepaths):
        lines = []
        for filepath in filepaths:
            for x in read_lines(filepath, skip_empty=True):
                if not x.startswith('#'):
                    lines.append(x)
        return cls(lines)

    def __init__(self, lines):
        self.lines = lines

    def test(self, test):
        for item in self.lines:
            r = re.search(item, test)
            if r:
                return item
        return None

    def includes(self, array):
        for item in array:
            if self.test(item) is not None:
                yield item

    def excludes(self, array):
        for item in array:
            if self.test(item) is None:
                yield item


def copy_tree_ignore(src, dest=None, ignores=None):
    ignores = ignores or {'.gitignore'}

    def walk(root):
        for ignore in ignores:
            if os.path.isfile(os.path.join(root, ignore)):
                FileHitChecker(root, ignore).write_dir(
                    dest + root[len(src):],
                    ignores={'.git'} if ignore == '.gitignore' else None
                )
                break
        else:
            for pa in list_dir(root):
                if os.path.isdir(pa):
                    walk(pa)
                else:
                    write_file(dest + pa[len(src):], c=pa)

    if not dest:
        dest = tempfile.mkdtemp()
    walk(src)
    return dest
