# 保存历史数据
import json
import logging
import os
import sys

import pytest

from baseapi.Fileoption import Fileoption


def save_history(history_dir, dist_dir):
    if not os.path.exists(os.path.join(dist_dir, "history")):
        Fileoption.create_dirs(os.path.join(dist_dir, "history"))
    else:
        # 遍历报告report下allure-report下的history目录下的文件
        for file in os.listdir(os.path.join(dist_dir, "history")):
            old_data_dic = {}
            old_data_list = []
            # 1、从report下allure-report下的history目录下的文件读取最新的历史纪录
            with open(os.path.join(dist_dir, "history", file), 'rb') as f:
                new_data = json.load(f)
            # 2、从Report下的history(历史文件信息存储目录)读取老的历史记录
            try:
                with open(os.path.join(history_dir, file), 'rb') as fr:
                    old_data = json.load(fr)

                    if isinstance(old_data, dict):
                        old_data_dic.update(old_data)
                    elif isinstance(old_data, list):
                        old_data_list.extend(old_data)
            except Exception as fe:
                print("{}文件查找失败信息：{}，开始创建目标文件！！！".format(history_dir, fe))
                Fileoption.create_file(os.path.join(history_dir, file))
                # 3、合并更新最新的历史纪录到report下的history目录对应浏览器目录中
            with open(os.path.join(history_dir, file), 'w') as fw:
                if isinstance(new_data, dict):
                    old_data_dic.update(new_data)
                    json.dump(old_data_dic, fw, indent=4)
                elif isinstance(new_data, list):
                    old_data_list.extend(new_data)
                    json.dump(old_data_list, fw, indent=4)
                else:
                    print("旧历史数据异常")


# 导入历史数据
def import_history_data(history_save_dir, result_dir):
    if not os.path.exists(history_save_dir):
        print("未初始化历史数据！！！进行首次数据初始化!!!")
    else:
        # 读取历史数据
        for file in os.listdir(history_save_dir):
            # 读取最新的历史纪录
            with open(os.path.join(history_save_dir, file), 'rb') as f:
                new_data = json.load(f)
            # 写入目标文件allure-result中，用于生成趋势图
            # Fileoption.create_file(os.path.join(result_dir, "history", file))
            try:
                with open(os.path.join(result_dir, "history", file), 'w') as fw:
                    json.dump(new_data, fw, indent=4)
            except Exception as fe:
                print("文件查找失败信息：{}，开始创建目标文件".format(fe))


# 运行命令参数配置
def run_all_case():
    # 测试结果文件存放目录
    result_dir = os.path.abspath("./Report/allure-result")
    # 测试报告文件存放目录
    report_dir = os.path.abspath("./Report/allure-report")
    # 本地测试历史结果文件存放目录，用于生成趋势图
    history_dir = os.path.abspath("./Report/history")
    # Fileoption.create_dirs(history_dir)
    # 定义测试用例features集合
    # allure_features = ["--allure-features"]
    # allure_features_list = [
    #     'Register_page_case',
    #     'Login_page_case'
    # ]
    # allure_features_args = ",".join(allure_features_list)
    # # 定义stories集合
    # allure_stories = ["--allure-stories"]
    # allure_stories_args = ['']
    allure_path_args = ['--alluredir', result_dir, '--clean-alluredir']
    test_args = ['-s', '-q', '--reruns', '2', '--reruns-delay', '1', '--count', '3', '-n', '3']
    # 添加['--ff']先运行上次失败用例，后运行其他用例
    # 添加['--lf']只运行上次failed和error用例
    # 添加['--reruns', 1','--reruns-delay','5'] 失败自动重新跑1次，间隔5秒
    # 添加['--count=10'] 重复执行用例，重复10遍
    run_args = test_args + allure_path_args
    print(f"run_args的完整参数：{run_args}")
    # 使用pytest.main
    pytest.main(run_args)
    # 导入历史数据
    import_history_data(history_dir, result_dir)
    # 生成allure报告，需要系统执行命令--clean会清楚以前写入environment.json的配置
    cmd = 'allure generate ./Report/allure-result -o ./Report/allure-report --clean'
    logging.info("命令行执行cmd:{}".format(cmd))
    print(f"cmd的命令:{cmd}")
    try:
        os.system(cmd)
    except Exception as e:
        logging.error('命令【{}】执行失败！'.format(cmd))
        sys.exit()
    # 定义allure报告环境信息
    # modify_report_environment_file(report_dir)

    # 保存历史数据
    save_history(history_dir, report_dir)


if __name__ == "__main__":
    run_all_case()
    # history_dir = os.path.abspath("./Report/history")
    # result_dir = os.path.abspath("./Report/allure-result")
    # import_history_data(history_dir,result_dir)

#Todo
# 增加异常日志打印处理
# 增加json-schema对比处理
# 增加缓存，装饰器等流程处理
#
