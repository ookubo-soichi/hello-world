import os, sys, re, shutil, send2trash

animetitle_long = ["＜アニメギルド＞・アニメ",
                   "乙女ゲームの破滅フラグ",
                   "かぐや様は告らせたい",
                   "ダーウィンズゲーム",
                   "ＬＩＳＴＥＮＥＲＳ",
                   "放課後ていぼう日誌",
                   "エヴァーガーデン",
                   "地縛少年花子くん",
                   "白猫プロジェクト",
                   "バトルの時間です",
                   "マギアレコード",
                   "デンドログラム",
                   "波よ聞いてくれ",
                   "イエスタデイ",
                   "推しが武道館",
                   "グレイプニル",
                   "食戟のソーマ",
                   "恋する小惑星",
                   "かくしごと",
                   "とある科学",
                   "痛いのは嫌",
                   "プランダラ",
                   "理系が恋に",
                   "サクラ大戦",
                   "ULTRAMAN",
                   "富豪刑事",
                   "天晴爛漫",
                   "神之塔",
                   "計算中",
                   "ＢＮＡ",
                   "球詠",
                   "八男",
                   "A3",
                  ]

animetitle_short = ["おーばーふろぉ",
                    "八十亀ちゃん",
]

main_dir = '/home/anisaba/animeonair/'
#backup_dir = 'F:\\animebackup\\'
bs = '/BS/'
utf = '/UTF/'
other = '/other/'

animetitle_long = list(set(animetitle_long))
animetitle = list(set(animetitle_long + animetitle_short))

utf_chs = ['ＴＯＫＹＯ　ＭＸ１',
           '東海テレビ',
           'テレビ愛知１',
           '中京テレビ１',
           'ＣＢＣテレビ',
           'テレビ東京１',
           'フジテレビ',
           'ＴＢＳ１',
           '日テレ１',]

bscs_chs = ['ＢＳ１１イレブン',
            'ＢＳ－ＴＢＳ',
            'ＢＳ日テレ',
            'ＢＳフジ',
            'ＢＳジャパン',]

def existHDST(title):
    for file in os.listdir(main_dir):
        if re.search(title+".*HD(-\d)?.*\.m2ts",file):
            return 1
        else:
            pass
    return 0

# Gnerate Directory
for title in animetitle:
    for d in [main_dir+bs, main_dir+utf]:#, backup_dir+bs, backup_dir+utf]:
        if not os.path.exists(d+title):
            os.mkdir(d+title)

# Check animetitle_long and animetitle_short is correct
wrong_short_flag = False
for title in animetitle_long:
    for file in os.listdir(main_dir):
        if re.search(title+".*\.m2ts",file) and 1.5 * 1024 ** 3 > os.path.getsize(file):
            print ('Short Title:'+title)
            wrong_short_flag = True
if wrong_short_flag:
    input()
    sys.exit()

# # Apply TsSplitter
# for title in animetitle_long:
#     for file in os.listdir(main_dir):
#         if re.search(title+".*\.m2ts",file):
#             os.system(main_dir+'/TsSplitter.sh "'+file+'"')

# Remove Small Size Files
for title in animetitle_long:
    for file in os.listdir(main_dir):
        if re.search(title+".*\.m2ts",file) and 1024 ** 3 > os.path.getsize(main_dir+file):
            send2trash.send2trash(main_dir+file)

# Remove Original if TsSplitted File Exists
for title in animetitle:
    for file in os.listdir(main_dir):
        if re.search(title+".*HD(-\d)?.*\.m2ts",file):
            send2trash.send2trash(main_dir+file.split('_HD')[0]+'.m2ts')

# Check File Size is not too Small (TsSplited to Multiple Files)
for title in animetitle_long:
    for file in os.listdir(main_dir):
        if re.search(title+".*\.m2ts",file) and 1.6 * (1000 ** 3) > os.path.getsize(main_dir+file):
            print("Warning : File Size is Small")
            print(file)
            print("End of Warning")

# Move to Each Directories
for title in animetitle:
    if existHDST(title):
        for file in os.listdir(main_dir):
            if re.search(title+".*HD(-\d)?.*\.m2ts",file):
                if file.split('[')[3].split(']')[0] in utf_chs:
                    shutil.move(file, main_dir+utf+title)
                else:
                    shutil.move(file, main_dir+bs+title)
            elif re.search(title+".*\.m2ts",file):
                if file.split('[')[3].split(']')[0] in utf_chs:
                    shutil.move(file, main_dir+utf+title)
                else:
                    shutil.move(file, main_dir+bs+title)
            else:
                pass
    else:
        for file in os.listdir():
            if re.search(title+".*\.m2ts",file):
                if file.split('[')[3].split(']')[0] in utf_chs:
                    shutil.move(file, main_dir+utf+title)
                else:
                    shutil.move(file, main_dir+bs+title)
            else:
                pass

# Move Unmached TS Files to Other Directory 
for file in os.listdir():
    if os.path.splitext(file)[1] == ".m2ts":
        shutil.move(file, main_dir+other)

# uncopyed_num = 0
# copyed_num = 0

# for title in animetitle:
#     for ch in [bs, utf]:
#         uncopyed_num += len(list(set(os.listdir(main_dir+ch+title)) - set(os.listdir(backup_dir+ch+title))))        

# for title in animetitle:
#     for ch in [bs, utf]:
#         for uncopyed in list(set(os.listdir(main_dir+ch+title))-set(os.listdir(backup_dir+ch+title))):
#             copyed_num += 1
#             print("copying %d/%d" % (copyed_num,uncopyed_num))
#             print(uncopyed)
#             shutil.copy(main_dir+ch+title+"\\"+uncopyed,backup_dir+ch+title)

# Remove Empty Directory
for d in [main_dir+bs, main_dir+utf]:#, backup_dir+bs, backup_dir+utf]:
    folders = [x for x in os.listdir(d) if os.path.isdir(d)]
    for f in folders:
        if os.listdir(d+f) == []:
            os.rmdir(d+f)
