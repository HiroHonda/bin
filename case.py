#! /usr/local/bin/python3.3
import sys
import re
bc = re.compile('^￼裁判年月日')
ec = re.compile('^裁判官|Westlaw作成目次')
yousi = re.compile('^要旨')
yousikm = re.compile('^◆|民事法篇|刑事法篇|公法篇')
kshs = re.compile('^新判例体系|裁判経過|出典|評釈|参照条文')
sk = re.compile('Westlaw Japan K.K., all rights reserved')
# a line next of the line of 'Westlaw Japan K.K., all rights reserved' is a page number
file = sys.argv[1:]
print('files are', file,file=sys.stderr)
for w in file:
    with open(w, mode='r',encoding='utf-16') as a_file:
        pl = False
        skn = False
        yousict = -1
        for a_line in a_file:
            #Westlawの行
            #Westlawの次の行はページ番号と仮定
            if sk.findall(a_line):
                 skn = True                   
                 continue
            elif skn:
                skn = False
                continue
            #開始と終了を調べ 各みだしに対応
            if bc.findall(a_line):#裁判年月日の行
                pl = True
                print('* ' + re.sub('.txt', '.pdf', w, count=0, flags=0))
                a_line = a_line.replace('￼', '', 1)
            elif ec.findall(a_line):#裁判官 or Westlaw作成目次 の行
                if pl == True:
                    print()
                    break
            elif yousi.match(a_line):#要旨の行
                yousict =0
                if pl:
                    print('** ',end='')
            # '◆'が要旨の内容の開始マークになっている 判例体系からのものも
            elif yousikm.findall(a_line):
                if yousict >1:
                    print()
                yousict = 1
            elif kshs.match(a_line):#裁判経過|出典|評釈|参照条文の行
                if pl:
                    if yousict >= 0:
                        print('\n** ',end='')
                        yousict = -1
                    else:
                        print('** ',end='')
            # 印刷する
            if pl :
##                print(yousict,end='')#for debugging
                if yousict > 1:
                    if a_line == "":
                        print()
                    else:
                        print(a_line.rstrip(),end='')
                    yousict = yousict +1
                elif yousict == 1:
                    print(a_line.rstrip(),end='')
                    yousict = yousict +1
                elif yousict == 0:
                    print(a_line.rstrip())
                    yousict = yousict +1
                else:
                    print(a_line.rstrip())

                    
