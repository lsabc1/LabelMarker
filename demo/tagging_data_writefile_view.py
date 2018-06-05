# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf


#  先将标注写入文件，之后跳转到tagging_cache.html再进行新页面的跳转
def tagging_push(request):
    ctx = {}
    # # 先将已有的labels存入字典中
    # file_object = open('label_data/labeled_data.txt', 'r')  # 用来把已测试的data加入字典，并删除前面的序号
    # s = set()
    # for f in file_object:
    #     pair = f.strip().split()
    #     curs = ""
    #     for i in range(1, len(pair)):
    #         if i > 1:
    #             curs += ' '
    #         curs += str(pair[i])
    #     s.add(curs.strip())
    # file_object.close()
    with open('label_data/index.txt', 'r+', encoding='utf-8') as f:  # 查看下一个要标注的地方
        f.seek(0, 0)
        index = f.readline()
        if index:
            index_list = index.split()
        else:
            f.write('1 1')
            index_list = [1, 1]

    line = int(index_list[0])
    str_num = int(index_list[1])

    with open('label_data/unlabeled_data.txt', encoding='utf-8') as f:  # 找到要标注的句子和字符
        lines = f.readlines()
        sentence = lines[line-1].strip()



    # file_object = open('label_data/unlabeled_data.txt', 'r') #从没标记的里面随机选一个
    # all_list = []
    # for f in file_object:
    #     all_list.append(f.strip())
    # ln = len(all_list)
    # next_title = all_list[random.randint(0, ln - 1)]`

    if 'label' in request.GET and 'title' in request.GET:  # 找到返回的GET里的东西
        print(str(request.GET) + ".....")
        title = str(request.GET['title']).strip()
        label = str(request.GET['label']).strip()
        title_char = title[-1]
        if label:
            with open('label_data/labeled_data.txt',
                               'a', encoding='utf-8') as file_object:
                file_object.write(title_char + " " + label + "\n")  # 把没标过的东西加入已标注
                if str_num == len(sentence):
                    str_num = 1
                    line += 1
                    file_object.write('\n')
                    if line > len(lines):  
                        return render(request, "over.html", ctx)
                else:
                    str_num += 1

            with open('label_data/index.txt', 'w+') as f:  # 改变下一个要标注的地方
                f.write(str(line) + ' ' + str(str_num))
        else:
            print('用户未选择label')

    # if len(s) >= len(all_list):  # 如果完成了所有的标注，跳转到结束页面
    #     return render(request, "over.html", ctx)

    # while next_title in s:  # 如果冲突就再选
    #     next_title = all_list[random.randint(0, ln - 1)].strip()
    with open('label_data/unlabeled_data.txt', encoding='utf-8') as f:
        lines = f.readlines()
        next_sentence = lines[line-1]
        next_str = next_sentence[str_num-1]
        next_title = next_sentence + '<br/>' + next_str

    ctx['next'] = "<input id='next' value='" + \
        next_title + "' style='display:none;'></input>"

    return render(request, "tagging_cache.html", ctx)  # 将下一个要标注的信息传递出去
