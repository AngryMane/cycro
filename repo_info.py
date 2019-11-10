import git
import lizard
import os
from collections import namedtuple
from timeout_decorator import timeout, TimeoutError

from const import *

FunctionInfo = namedtuple(
    "FunctionInfo", ("lang", "nloc", "ccn", "token", "line", "name", "proj")
)


class RepositoryInfo:
    def __init__(self, url, project_name, lang_name):
        self.__url = url
        self.__lang_name = lang_name
        self.__proj_name = project_name
        self.__git_dir_path = Const.PROJECTS_PATH + "/" + project_name
        self.__result_file = Const.RESULT_PATH + "/" + self.__proj_name

    @timeout(120)
    def __git_clone__(self):
        if os.path.exists(self.__git_dir_path):
            return
        self.__repo = git.Repo.clone_from(self.__url, self.__git_dir_path)

    def __build_lizard_command(self):
        command = "lizard"
        command += " "

        command += "-l"
        command += " "
        command += self.__lang_name
        command += " "

        command += "--csv"
        command += " "

        command += self.__git_dir_path
        command += " "

        command += " > "
        command += self.__result_file

        return command

    def analayze(self):
        print("start " + "analyze " + self.__proj_name)
        try:
            # self.__git_clone__()
            pass
        except TimeoutError:
            print("git clone time out.")
            return
        command = self.__build_lizard_command()
        # os.system(command)

    def get_func_infos(self):
        if not os.path.exists(self.__result_file):
            print("result file not exist")
            return []
        print("start " + "get_func_infos " + self.__proj_name)
        with open(self.__result_file) as result_file:
            func_infos = result_file.readlines()
        func_infos = [func_info.replace('"', "") for func_info in func_infos]
        func_infos = [func_info.split(",") for func_info in func_infos]
        func_infos = list(filter(lambda x: len(x) >= 8, func_infos))
        func_infos = list(filter(lambda x: x[0].isnumeric(), func_infos))
        func_infos = list(filter(lambda x: x[1].isnumeric(), func_infos))
        func_infos = list(filter(lambda x: x[2].isnumeric(), func_infos))
        func_infos = list(filter(lambda x: x[3].isnumeric(), func_infos))
        ret = [
            FunctionInfo(
                self.__lang_name,
                int(func_info[0]),
                int(func_info[1]),
                int(func_info[2]),
                int(func_info[3]),
                func_info[7],
                self.__proj_name,
            )
            for func_info in func_infos
        ]
        return ret
