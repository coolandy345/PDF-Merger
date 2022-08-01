from PyPDF2 import PdfMerger
import os
import csv
from natsort import natsorted

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def search_file_inTarget():
    pdf_Path = []
    dir_path = "tartget"
    file_name_list=[]

    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass

    print(bcolors.OKCYAN + "ファイル検索を開始します..."+bcolors.ENDC,end="")
    # Iterate directory
    for path in os.listdir(dir_path):
        file_name_list.append(path)

    if not file_name_list:
        print(bcolors.FAIL + "[失敗]"+bcolors.ENDC+" : 'target'フォルダーの中には合併できるファイルはありません。もう一度ご確認ください。")
        return []

    print(bcolors.OKGREEN + "[成功]"+bcolors.ENDC+" : ファイルを検知しました。")
    
    file_name_list=natsorted(file_name_list)

    return file_name_list

def check_order(list,targets):

    iner_list=[]
    if list:
        for unit in natsorted(list.keys()):
            iner_list.append(list[unit])

        if len(iner_list) == len(targets):
            content_good=True
            for target in targets:
                try:
                    iner_list.index(target)
                except ValueError:
                    content_good=False

            return content_good
        else:
            return False
    else:
        return False

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

# option=0
# print(bcolors.HEADER + "PDF合併ツール1.0 製作By "+bcolors.OKBLUE + "Kou " +bcolors.HEADER + "ようこそへ"+ bcolors.ENDC)

def print_option():
    print("-----------------------------------------------------------")
    print("key["+bcolors.FAIL + "1"+bcolors.ENDC + "] : 'target'フォルダー中のpdfを合併開始する")
    print("key["+bcolors.FAIL + "2"+bcolors.ENDC + "] : 入っているpdf件名を表示する")
    print("key["+bcolors.FAIL + "3"+bcolors.ENDC + "] : 合併list内容を表示する")
    print("key["+bcolors.FAIL + "4"+bcolors.ENDC + "] : このツールを終了する")
    print("key["+bcolors.FAIL + "5"+bcolors.ENDC + "] : 現在入っているpdfに基づくlistを出力する(順番なし)")
    GoodOption=False
    while not GoodOption:
        print("")
        enter_key=input(bcolors.BOLD + "Option Key を入力ください: "+ bcolors.ENDC)
        if (enter_key.isnumeric() and
            int(enter_key)>=1 and
            int(enter_key)<=5 ):
            GoodOption=True
        else:
            print(bcolors.FAIL + "認識出来ないオプションが入力されました。もう一度ご確認ください。"+ bcolors.ENDC)

    return int(enter_key)

def Merge_file():
    file_name_list=search_file_inTarget()
    csv_list=Search_List()


    if check_order(csv_list,file_name_list):

        merger = PdfMerger()

        

        for pdf_name in natsorted(csv_list.keys()):
            dir_path = "tartget"
            merger.append(os.path.join(dir_path,csv_list[pdf_name]))

        name=input(bcolors.BOLD + "出力ファイル名を入力してください: "+ bcolors.ENDC)
        if not name:
            name="output_file"
        merger.write(f"{name}.pdf")
        merger.close()
    else:
        print(bcolors.FAIL + "Listとフォルダー内容は一致しなかった為、もう一度ご確認ください。"+ bcolors.ENDC)

def Show_file():
    file_name_list=search_file_inTarget()
    
    index=1
    for name in file_name_list:
        print(f"No.{index:3} - {name}")
        index+=1

def Search_List():
    csv_path="list.csv"
    print(bcolors.OKCYAN + "'list.csv'を読み取ります..."+bcolors.ENDC,end="")
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            print(bcolors.OKGREEN + "[成功]"+bcolors.ENDC)
            reader=csv.reader(csvfile)
            content={}
            for line in reader:
                if line[0]!="順番":
                    content[line[0]]=line[1]

            return content
    except FileNotFoundError:
        print(bcolors.FAIL + "[失敗]"+bcolors.ENDC,end="")
        print(" : 作成リスト(件名:'list.csv')存在していないため...")
        option=input(bcolors.OKBLUE + "新たなリストを作成しますか？"+bcolors.ENDC+" はい:[Y] いええ:[N] : ")
        if option.capitalize()=="Y":
            Make_list()
        else:
            return []

def Show_list():
    content=Search_List()
    if content:
        for index in natsorted(content.keys()):
            print(f"{index:4} - {content[index]}")
    else:
        pass

      
def Make_list():
    file_name_list=search_file_inTarget()

    csv_path="list.csv"
    print(bcolors.OKCYAN + "'list.csv'を再製作します..."+bcolors.ENDC,end="")
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["順番","ファイル名"])

        # check_order()
        index=1
        for name in file_name_list:
            writer.writerow([index,name])
            index+=1

        print(bcolors.OKGREEN + "[成功]"+bcolors.ENDC)

os.system("")
option=0
print(bcolors.HEADER + "PDF合併ツール1.0 製作By "+bcolors.OKBLUE + "Kou " +bcolors.HEADER + "ようこそへ"+ bcolors.ENDC)
while not option==4:
    option=print_option()
    if option==1:
        print(bcolors.HEADER + "key[1] : pdfを合併"+ bcolors.ENDC)
        Merge_file()
    elif option==2:
        print(bcolors.HEADER + "key[2] : pdf件名を表示"+ bcolors.ENDC)
        Show_file()
    elif option==3:
        print(bcolors.HEADER + "key[3] : list内容を表示"+ bcolors.ENDC)
        Show_list()
    elif option==4:
        print(bcolors.HEADER + "key[4] : ツールを終了"+ bcolors.ENDC)
        pass
    elif option==5:
        print(bcolors.HEADER + "key[5] : listを出力"+ bcolors.ENDC)
        Make_list()

