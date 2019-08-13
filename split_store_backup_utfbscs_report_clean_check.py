import os
import re
import shutil
import ctypes
dll = ctypes.windll.trash

animetitle_long = ["通常攻撃が全体攻撃で二回攻撃のお母さんは好きですか",
                   "可愛ければ変態でも好きになってくれますか",
                   "この世の果てで恋を唄う少女",
                   "ありふれた職業で世界最強",
                   "世話やきキツネの仙狐さん",
                   "荒ぶる季節の乙女どもよ",
                   "かつて神だった獣たちへ",
                   "とある科学の一方通行",
                   "女子高生の無駄づかい",
                   "ダンベル何キロ持てる",
                   "異世界チート魔術師",
                   "フルーツバスケット",
                   "ロード・エルメロイ",
                   "うちの娘の為ならば",
                   "ヴィンランド・サガ",
                   "魔王様、リトライ",
                   "ナカノヒトゲノム",
                   "彼方のアストラ",
                   "まちカドまぞく",
                   "コップクラフト",
                   "トライナイツ",
                   "グランベルム",
                   "炎炎ノ消防隊",
                   "チューズデイ",
                   "ＳＴＯＮＥ",
                   "サイコパス",
                   "鬼滅の刃",
                   "ギヴン",
                   "胡蝶綺",
                   "ＢＥＭ",
                  ]

animetitle_short = ["手品先輩",
                    "ソウナンですか",]

animetitle_long = list(set(animetitle_long))
animetitle = list(set(animetitle_long + animetitle_short))

utf_chs = ['チャンネル:ＴＯＫＹＯ\u3000ＭＸ１\n',
           'チャンネル:東海テレビ０１１\n',
           'チャンネル:テレビ愛知１\n',
           'チャンネル:中京テレビ１\n',
           'チャンネル:ＣＢＣテレビ\n',
           'チャンネル:テレビ東京１\n',
           'チャンネル:フジテレビ\n',
           'チャンネル:ＴＢＳ１\n',
           'チャンネル:日テレ１\n',
           ]

bscs_chs = ['チャンネル:ＢＳ１１イレブン\n',
            'チャンネル:ＢＳアニマックス\n',
            'チャンネル:ＢＳフジ・１８１\n',
            'チャンネル:ＢＳジャパン\n',
            'チャンネル:ＢＳ－ＴＢＳ\n',
            ]

main_dir = "D:\\animeonair\\"
backup_dir = "F:\\animebackup\\"
bs = "BS\\"
utf = "UTF\\"

def existHDST(title):
    for file in os.listdir():
        if re.search(title+".*HD(-\d)?.*\.ts",file):
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
    for d in [main_dir+bs, main_dir+utf, backup_dir+bs, backup_dir+utf]:
        if not os.path.exists(d+title):
            os.mkdir(d+title)

if not os.path.exists("その他"):
    os.mkdir("その他")

wrong_short_flag = False
for title in animetitle_long:
    for file in os.listdir():
        if re.search(title+".*\.ts",file) and 1.5 * 1024 ** 3 > os.path.getsize(file):
            print ('Short Title:'+title)
            wrong_short_flag = True
if wrong_short_flag:
    input()
    sys.exit()

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
            os.system('TsSplitter -SD -1SEG -SEP2 -SEPA "'+file+'"')
            pass

for title in animetitle_long:
    for file in os.listdir():
        if re.search(title+".*\.ts",file) and 1024 ** 3 > os.path.getsize(file):
            dll.trash(file)

for title in animetitle:
    for file in os.listdir():
        if re.search(title+".*HD(-\d)?.*\.ts",file):
            dll.trash(file.split('_')[0]+'.ts')

for title in animetitle_long:
    for file in os.listdir():
        if re.search(title+".*\.ts",file) and 1.6 * (1000 ** 3) > os.path.getsize(file):
            print("Warning : File Size is Small")
            print(file)
            print("End of Warning")

for title in animetitle:
    if existHDST(title):
        for file in os.listdir():
            if re.search(title+".*HD(-\d)?.*\.ts",file):
                if open(file.split('_')[0]+'.txt', 'r', errors='ignore').readline() in utf_chs:
                    shutil.move(file,utf+title)
                else:
                    shutil.move(file,bs+title)
            elif re.search(title+".*\.ts",file):
                if open(file.split('.')[0]+'.txt', 'r', errors='ignore').readline() in utf_chs:
                    shutil.move(file,utf+title)
                else:
                    shutil.move(file,bs+title)
            else:
                pass
    else:
        for file in os.listdir():
            if re.search(title+".*\.ts",file):
                if open(file.split('.')[0]+'.txt', 'r', errors='ignore').readline() in utf_chs:
                    shutil.move(file,utf+title)
                else:
                    shutil.move(file,bs+title)
            else:
                pass

for file in os.listdir():
    if os.path.splitext(file)[1] == ".ts":
        shutil.move(file,"その他")

for title in animetitle:
    for file in os.listdir():
        if re.search(title+".*\.txt",file):
            dll.trash(file)

uncopyed_num = 0
copyed_num = 0

for title in animetitle:
    for ch in [bs, utf]:
        uncopyed_num += len(list(set(os.listdir(main_dir+ch+title)) - set(os.listdir(backup_dir+ch+title))))        

for title in animetitle:
    for ch in [bs, utf]:
        for uncopyed in list(set(os.listdir(main_dir+ch+title))-set(os.listdir(backup_dir+ch+title))):
            copyed_num += 1
            print("copying %d/%d" % (copyed_num,uncopyed_num))
            print(uncopyed)
            shutil.copy(main_dir+ch+title+"\\"+uncopyed,backup_dir+ch+title)

for d in [main_dir+bs, main_dir+utf, backup_dir+bs, backup_dir+utf]:
    folders = [x for x in os.listdir(d) if os.path.isdir(d)]
    for f in folders:
        if os.listdir(d+f) == []:
            dll.trash(d+f)
