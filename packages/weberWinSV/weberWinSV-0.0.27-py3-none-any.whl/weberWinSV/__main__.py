# weberWinSV/__main__.py
# python -m weberWinSV 入口程序

import sys
import os
from .CWinSupervisor import StartCWinSupervisor


def _startWinSV(sSettingPyFullFN, sGroupKeyName, sDictVarName):
    sPythonFileName = os.path.basename(sSettingPyFullFN)
    # print(f'_startWinSV.sPythonFileName={sPythonFileName}=')
    StartCWinSupervisor(sSettingPyFullFN, sPythonFileName, sDictVarName, sGroupKeyName)


if __name__ == "__main__":
    # 调用包内的函数或执行其他初始化代码
    sSettingPyFullFN = 'settingsWinSV.py'
    sGroupKeyName = 'GroupId4Run'
    sDictVarName = 'gDictConfigByGroupId'
    if len(sys.argv) >= 2:
        sSettingPyFullFN = sys.argv[1]
        if len(sys.argv) >= 3:
            sGroupKeyName = sys.argv[2]
            if len(sys.argv) >= 4:
                sDictVarName = sys.argv[3]
    else:
        print(r"python -m weberWinSV d:\full\path\settingsWinSV.py")
    _startWinSV(sSettingPyFullFN, sGroupKeyName, sDictVarName)

