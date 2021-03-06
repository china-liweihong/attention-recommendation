import pickle
import random

wd = 'music/'
wd = ''
f = open(wd + 'user_info.txt', 'r')
user_info = f.readlines()
f.close()
f = open(wd + 'song_info.txt', 'r', encoding='utf8')
song_info = f.readlines()
f.close()

'''
读取音乐数据 
'''
song_info = song_info[1:]
song_dic = {}
for line in song_info:
    sname, sid, singer, album, cnum, zuoqu, zuoci, rateduser = line.split('\t')
    sid = int(sid)
    song_dic[sid] = [singer, album, zuoci, zuoqu]

'''
读取用户数据
'''
user_info = user_info[1:]
user_dic = {}
rated_song = set()

for line in user_info:
    uid, cnum, songls = line.split('\t')
    uid = int(uid)
    songls = eval(songls)
    songls = list(map(lambda x: int(x), songls))
    unknowsong = []
    for song in songls:
        if song not in song_dic:
            unknowsong.append(song)
        else:
            rated_song.add(song)
    for song in unknowsong:
        songls.remove(song)
    user_dic[uid] = list(set(songls))

uidls = list(user_dic.keys())
sidls = list(song_dic.keys())
print(len(rated_song))
'''
删除未出现过的歌曲
'''
for i in sidls:
    if i not in rated_song:
        sidls.remove(i)

'''
将用户、歌曲重新编号。使其为连续的自然数。
'''


def get_new_uid(uid):
    return uidls.index(uid)


def get_new_sid(sid):
    return sidls.index(sid)


vocabulary = ['Unknown']
user_info = {}
song_info = {}
for i in sidls:
    singer, album, zuoci, zuoqu = song_dic[i]
    if singer not in vocabulary:
        vocabulary.append(singer)
    if album not in vocabulary:
        vocabulary.append(album)
    if zuoci not in vocabulary:
        vocabulary.append(zuoci)
    if zuoqu not in vocabulary:
        vocabulary.append(zuoqu)
    sinfo = 's' + str(get_new_sid(i))
    if sinfo not in vocabulary:
        vocabulary.append(sinfo)
    #song_info[get_new_sid(i)] = [vocabulary.index(sinfo), vocabulary.index(singer), vocabulary.index(album),
    #                             vocabulary.index(zuoci)]


    #song_info[get_new_sid(i)] = [vocabulary.index(sinfo)] * 4 + [vocabulary.index(singer)] * 4 + \
    #                            [vocabulary.index(album)] * 4 + [vocabulary.index(zuoci)] * 4


    song_info[get_new_sid(i)] = []
    for j in range(4):
        song_info[get_new_sid(i)] += [vocabulary.index(sinfo), vocabulary.index(singer), vocabulary.index(album),
                                      vocabulary.index(zuoci)]


dataset = 'music'
f = open(wd + "music.train.rating", "r")

r = f.readlines()
train = {}
for line in r:
    uid, iid, rating = line.strip().split('\t')
    uid = int(uid)
    iid = int(iid)
    if rating == '5':
        if uid not in train:
            train[uid] = []
        train[uid].append(iid)

for user_id in user_dic:
    nuid = get_new_uid(user_id)
    u_info = 'u' + str(nuid)
    vocabulary.append(u_info)
    user_info[nuid] = []
    if nuid not in train:
        train[nuid] = []

    for song in train[nuid]:
        for info in song_info[song][0:4]:
            user_info[nuid].append(info)
        # sinfo = 's' + str(song)
        # user_info[nuid].append(vocabulary.index(sinfo))
        if len(user_info[nuid]) == 40:
            break
    while len(user_info[nuid]) < 40:
        user_info[nuid].append(0)

    user_info[nuid].append(vocabulary.index(u_info))
    for j in range(3):
        user_info[nuid].append(vocabulary.index(u_info))

f.close()

'''

print(vocabulary[3])

#张学友
sp=['s33004','s33003','s33092','s32964','s33081','s32944',
#许冠杰
's3543','s7880'
#else
,'s14930'
,'s20688']

ssp=user_info[100][10]
user_info[100]=[]
for i in sp:
    user_info[100].append(vocabulary.index(i))
user_info[100].append(ssp)
'''

pickle.dump(user_info, open('user_hist_withinfo_music_HK', 'wb'))
pickle.dump(song_info, open('song_info_music_HK_w', 'wb'))
print(len(vocabulary))
exit()

def look(i):
    return vocabulary[i]


def ttt(k):
    uinfo = user_info[k]
    for i in uinfo:
        # if vocabulary[i][1:]=='Unknown':
        #    continue
        print(list(map(look, song_info[int(vocabulary[i][1:])][1:])))
        # print(song_info[int(vocabulary[i][1:])][1:])


'''
106
[14385, 14395, 14398, 14411, 14431, 14438, 14434, 14390, 14432, 14437, 47150]
10287
[14385, 14378, 14379, 14378]


134
[46076, 46149, 38675, 46102, 30870, 0, 0, 0, 0, 0, 47178]
[46076, 46149, 38675, 46102, 30870, 363, 333, 4765, 4796, 5472, 47178]



#25723157
46076
[46076, 1027, 46044, 3]

46149
[46149, 1027, 46132, 918]


1013
[17986, 35784, 20161, 23189, 23419, 35903, 23303, 24167, 14371, 20417, 48057]

17986
[17986, 17981, 17984, 17981]
'''

t = [46076, 46149, 38675, 46102, 30870, 29217, 14985, 4765, 4796, 5472, 47178]
t2 = [46149, 1027, 46132, 918]
tl = list(map(look, t))
for i in tl:
    i = int(i[1:])
    print(list(map(look, song_info[i])))

tl2 = list(map(look, t2))

'''
['s32347', '周杰伦', '天台 电影原声带', '']
['s32411', '周杰伦', '跨时代', '方文山']
['s26938', '五月天', '知足 最真杰作选', '']
['s32373', '周杰伦', '天台 电影原声带', '周杰伦']
['s21551', '南拳妈妈', '决斗巴赫', '']
['s286', '伍佰', '树枝孤鸟', '']
['s32328', '周杰伦', 'The One 演唱会', '']
['s3400', '许冠杰', '环球萃取升级精选 许冠杰3', '']
['s3420', '许冠杰', '许冠杰金装精选', '']
['s3920', '信', '反正我信了', '信']


['s32411', '周杰伦', '跨时代', '方文山']
'''
'''
可爱女人
[46201, 1027, 46169, 2452]
'''
vocabulary.index('s32457')

song_raw = user_dic[uidls[100]]
song_new = list(map(get_new_sid, song_raw))

count = 0
totalcount = 0
for s in song_new:
    totalcount += 1
    if song_info[s][3] == 3:
        count += 1
    # print(sidls[int(vocabulary[song_info[s][0]][1:])])
    print(totalcount - 1)
    print(list(map(look, song_info[s])))
