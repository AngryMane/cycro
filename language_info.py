import requests

from const import *
from repo_info import *


class LanguageInfo:
    def __init__(self, git_name, lizard_name):
        git_request = Const.REQUEST_TEMPLATE + git_name
        self.__trend_repo_infos = requests.get(git_request).json()
        self.__lizard_name = lizard_name
        self.__repos = [
            RepositoryInfo(
                x[Const.JSON_2_URL], x[Const.JSON_2_NAME], self.__lizard_name
            )
            for x in self.__trend_repo_infos
        ]

    def get_lang_name(self):
        return self.__lizard_name

    def get_trend_repos(self):
        return [
            (x[Const.JSON_2_URL], x[Const.JSON_2_NAME]) for x in self.__trend_repo_infos
        ]

    def get_lang_quolity(self):
        ret = []
        for repo in self.__repos:
            repo.analayze()
            cur_infos = repo.get_func_infos()
            ret.extend(cur_infos)

        return ret


LANGUAGE_INFOS = [
    LanguageInfo("Python", "python"),
    LanguageInfo("C++", "cpp"),
    LanguageInfo("Java", "java"),
    LanguageInfo("C#", "csharp"),
    LanguageInfo("JavaScript", "javascript"),
    LanguageInfo("Swift", "swift"),
    LanguageInfo("Ruby", "ruby"),
    LanguageInfo("PHP", "php"),
    LanguageInfo("Scala", "scala"),
    LanguageInfo("Golang", "go"),
    LanguageInfo("Lua", "lua"),
]
