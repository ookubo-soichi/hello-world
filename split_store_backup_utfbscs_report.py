import os
import re
import shutil
import ctypes
dll = ctypes.windll.trash

animetitle_long = ["アルドノア",
                   "さばげぶっ！",
                   "魔法科高校の劣等生",
                   "ソノ黒キ鋼",
                   "ハマトラ",
                   "月刊少女野崎くん",
                   "Ｆｒｅｅ！",
                   "グラスリップ",
                   "キャプテン・アース",
                   "白銀の意思",
                   "東京喰種",
                   "ＲＡＩＬ　ＷＡＲＳ！",
                   "ＲＡＩＬ ＷＡＲＳ！",
                   "普通の女子校生が",
                   "六畳間の侵略者",
                   "少年ハリウッド",
                   "ばらかもん",
                   "人生相談",
                   "アカメが斬る",
                   "アオハライド",
                   "ハナヤマタ",
                   "ＤＲＡＭＡｔｉｃａｌ",
                   "まじもじるるも",
                   "残響のテロル",
                   "ＰＳＹＣＨＯ－ＰＡＳＳ",
                   "東京ＥＳＰ",
                   "精霊使いの剣舞",
                  ]

animetitle_short = ["ひめゴト",
                    "闇芝居",
                    ]

animetitle = animetitle_long + animetitle_short


utf = ['チャンネル:ＴＯＫＹＯ\u3000ＭＸ１\n',
       'チャンネル:テレビ東京１\n',
       'チャンネル:ＴＢＳ１\n',
       'チャンネル:日テレ１\n',
       'チャンネル:フジテレビ\n',
       ]

bscs = ['チャンネル:ＢＳ１１\n']

def existHDST(title):
    for file in os.listdir():
        if re.search(title+".*HD(-\d)?\.ts",file):
            return 1
        else:
            pass
    return 0

def error_or_drop(file):
    is_error_or_drop = 0
    for line in open(file,errors='ignore').readlines():
        if ((re.search("総パケットエラー数",line)
             and (not re.search("総パケットエラー数:0",line)))
            or
            (re.search("総パケットドロップ数",line)
             and (not re.search("総パケットドロップ数:0",line)))):
            is_error_or_drop = 1
        else:
            pass
    return is_error_or_drop

for title in animetitle:
    if not os.path.exists("UTF\\"+title):
        os.mkdir("UTF\\"+title)
    if not os.path.exists("BS\\"+title):
        os.mkdir("BS\\"+title)

if not os.path.exists("その他"):
    os.mkdir("その他")

for title in animetitle:
    for file in os.listdir():
        if re.search(title+".*\.txt",file):
            if error_or_drop(file):
                print(file.split('.')[0])
                for line in open(file,errors='ignore').readlines():
                    if re.search("チャンネル",line):
                        print(line.rstrip().split(":")[-1],end=", ")
                    elif re.search("総パケットエラー数",line):
                        print(line.rstrip(),end=", ")
                    elif re.search("総パケットドロップ数",line):
                        print(line.rstrip()+'\n')
                    else:
                        pass

for title in animetitle_long:
    for file in os.listdir():
        if re.search(title+".*\.ts",file):
            os.system("TsSplitter -SD -1SEG -SEP2 -SEPA "+file)

for title in animetitle_long:
    for file in os.listdir():
        if re.search(title+".*\.ts",file) and 1024 ** 3 > os.path.getsize(file):
            dll.trash(file)

for title in animetitle:
    for file in os.listdir():
        if re.search(title+".*HD(-\d)?\.ts",file):
            dll.trash(file.split('_')[0]+'.ts')

for title in animetitle:
    if existHDST(title):
        for file in os.listdir():
            if re.search(title+".*HD(-\d)?\.ts",file):
                if open(file.split('_')[0]+'.txt', 'r').readline() in utf:
                    shutil.move(file,"UTF\\"+title)
                else:
                    shutil.move(file,"BS\\"+title)
            elif re.search(title+".*\.ts",file):
                if open(file.split('.')[0]+'.txt', 'r').readline() in utf:
                    shutil.move(file,"UTF\\"+title)
                else:
                    shutil.move(file,"BS\\"+title)
            else:
                pass
    else:
        for file in os.listdir():
            if re.search(title+".*\.ts",file):
                if open(file.split('.')[0]+'.txt', 'r').readline() in utf:
                    shutil.move(file,"UTF\\"+title)
                else:
                    shutil.move(file,"BS\\"+title)
            else:
                pass

for file in os.listdir():
    if os.path.splitext(file)[1] == ".ts":
        shutil.move(file,"その他")

for title in animetitle:
    for file in os.listdir():
        if re.search(title+".*\.txt",file):
            dll.trash(file)

for title in animetitle:
    if not os.path.exists("F:\\animebackup\\UTF\\"+title):
        os.mkdir("F:\\animebackup\\UTF\\"+title)
    if not os.path.exists("F:\\animebackup\\BS\\"+title):
        os.mkdir("F:\\animebackup\\BS\\"+title)

uncopyed_num = 0
copyed_num = 0

for title in animetitle:
    uncopyed_num += len(list(set(os.listdir("D:\\animeonair\\UTF\\"+title))
                             -set(os.listdir("F:\\animebackup\\UTF\\"+title))))
    uncopyed_num += len(list(set(os.listdir("D:\\animeonair\\BS\\"+title))
                             -set(os.listdir("F:\\animebackup\\BS\\"+title))))

for title in animetitle:
    for uncopyed in list(set(os.listdir("D:\\animeonair\\UTF\\"+title))
                         -set(os.listdir("F:\\animebackup\\UTF\\"+title))):
        copyed_num += 1
        print("copying %d/%d" % (copyed_num,uncopyed_num))
        print(uncopyed)
        shutil.copy("D:\\animeonair\\UTF\\"+title+"\\"+uncopyed,"F:\\animebackup\\UTF\\"+title)
    for uncopyed in list(set(os.listdir("D:\\animeonair\\BS\\"+title))
                         -set(os.listdir("F:\\animebackup\\BS\\"+title))):
        copyed_num += 1
        print("copying %d/%d" % (copyed_num,uncopyed_num))
        print(uncopyed)
        shutil.copy("D:\\animeonair\\BS\\"+title+"\\"+uncopyed,"F:\\animebackup\\BS\\"+title)
