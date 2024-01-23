from __future__ import print_function
import os
import shutil
import pyaudio
import wave
from .split_audio import spl_audio
from pydub import AudioSegment
from .Ifasr_new import RequestApi
from .new_method import LtpParser
from .new_method import youdao
from .new_method import en_cixing
from .comparison import Ltpcomparison
import pandas as pd
import re

def start_audio(time = 3, RECORD_SECONDS = 60):
    #yield "Loading..."
    huifu = "no emotional blackmail" 
    ls_huifu = []   

    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit
    CHANNELS = 1
    RATE = 16000
    ltppar = LtpParser()
    ltpcom = Ltpcomparison()
    fp2 = pd.read_csv('/home/pua/Downloads/try_pua/EBDCH/xitong/train_input.csv')
    train_contents = []
    for i in range(len(fp2['category'])):
        train_contents.append(fp2['category'][i])

    filepath1 = "/home/pua/Downloads/try_pua/EBDCH/xitong/first_save"
    if not os.path.exists(filepath1):
        os.mkdir(filepath1)
    else:
        shutil.rmtree(filepath1)
        os.mkdir(filepath1)

    filepath2 = "/home/pua/Downloads/try_pua/EBDCH/xitong/second_save"
    if not os.path.exists(filepath2):
        os.mkdir(filepath2)
    else:
        shutil.rmtree(filepath2)
        os.mkdir(filepath2)

    filepath3 = "/home/pua/Downloads/try_pua/EBDCH/xitong/save_txt"
    if not os.path.exists(filepath3):
        os.mkdir(filepath3)
    else:
        shutil.rmtree(filepath3)
        os.mkdir(filepath3)


    p = pyaudio.PyAudio()	#初始化
    print("ON")
    #yield "Recording..."

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)#创建录音文件

    for count in range(0, int(RECORD_SECONDS/time)):
        frames = []
        for i in range(count * int(RATE / CHUNK * time), (count+1) * int(RATE / CHUNK * time)):
            data = stream.read(CHUNK)
            frames.append(data)
        wf = wave.open("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/" + str(count) + ".wav", 'wb')  # 保存
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        if count >= 1:
            file_name_1 = os.listdir("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/")
            #ls_panduan = []
            for fn in file_name_1:
                guodu = str(fn).split(".")[0]
                #print("guodu: ", guodu)
                spl_audio("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/", guodu, 1000, 10000)
            file_name_2 = os.listdir("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/")

            if len(file_name_2) < 2:
                print("error")
                break

            if len(file_name_2) == 2:
                print("=2")
                ls_audio_fn = []
                for fn in file_name_2:
                    ls_audio_fn.append(AudioSegment.from_wav("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/"+fn))

                for fn in file_name_2:
                    os.remove("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/"+fn)

                hecheng_audio = ls_audio_fn[0]+ls_audio_fn[1]
                hecheng_audio.export("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/" + str(count) + ".wav", format="wav")
                

            if len(file_name_2) > 2:
                print(">2")

                ls_audio_fn = []
                for fn in file_name_2:
                    #print(fn)

                    #print(str(fn).split("_")[0])

                    if str(count) == str(fn).split("_")[0] and "-1" in str(fn):
                        continue
                    ls_audio_fn.append(AudioSegment.from_wav("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/"+fn))

                hecheng_audio = 0
                for laf in ls_audio_fn:
                    hecheng_audio = hecheng_audio + laf
                hecheng_audio.export("/home/pua/Downloads/try_pua/EBDCH/xitong/second_save/" + str(count-1) + ".wav", format="wav")

                for fn in file_name_2:
                    if str(count) == str(fn).split("_")[0] and "-1" in str(fn):
                        continue
                    os.remove("/home/pua/Downloads/try_pua/EBDCH/xitong/first_save/"+fn)

                ls_wav = os.listdir("/home/pua/Downloads/try_pua/EBDCH/xitong/second_save/")
                for lw in ls_wav:
                    api = RequestApi(appid = "0da4904a",
                                 secret_key = "5d934a0240f2f43189f2ec844cfd3008",
                                 upload_file_path = "/home/pua/Downloads/try_pua/EBDCH/xitong/second_save/"+lw)
                    api.get_result(str(lw).split(".")[0])
                    os.remove("/home/pua/Downloads/try_pua/EBDCH/xitong/second_save/"+lw)

                ls_txt = os.listdir("/home/pua/Downloads/try_pua/EBDCH/xitong/save_txt/")
                contents = []
                for lt in ls_txt:
                    fp = open("/home/pua/Downloads/try_pua/EBDCH/xitong/save_txt/"+lt, "r", encoding = 'utf-8')
                    content = fp.read().splitlines()
                    fp.close()
                    for con in content:
                        contents.append(con)
                    os.remove("/home/pua/Downloads/try_pua/EBDCH/xitong/save_txt/" + lt)



                tents = []
                ni_zhouwei = []
                for i in range(len(contents)):
                    lianxu = contents[i]
                    while True:
                        daice = ltppar.dengju_qiefen(str(lianxu))
                        jiance_result = ltppar.ni_nin_v(str(daice[0]))
                        if jiance_result[0] == 1:
                            tents.append(str(daice[0]))
                            # print("daice[0]: ", daice[0])
                            ni_zhouwei.append(jiance_result[1])
                        # print("jiance_result[1]: ", jiance_result[1])
                        if daice[1] == 0:
                            break
                        lianxu = ltppar.anbiaodian_qiefen(str(lianxu))

                daixunlian = []
                input = []
                for j in range(len(tents)):
                    # content = '你别说真是，老想要喝水，'
                    cixing_panduan = ltppar.test_cixing_zuhe(tents[j])
                    if cixing_panduan[0] == 1:
                        cx1 = cixing_panduan[1]  # 所有lunci
                        for i in range(len(cixing_panduan[1])):
                            daixunlian.append(tents[j])

                            cx1i = cx1[i]  # 每一lunci
                            # yuy = ltppar.test_yuyi(content, cx1i)
                            po_yu = ltppar.test_pos_yuyi(tents[j])

                            jiehe = ltppar.test_yuyi_cixing(cx1i, po_yu, ni_zhouwei[j])
                            input.append(jiehe)



                label = []
                for ip in input:
                    test = ip.split("#")
                    #print("test:", test)
                    panduan = 0
                    for train_content in train_contents:
                        train = train_content.split("#")
                        #print("train:", test)
                        p5 = ltpcom.part5(test[4], train[4])
                        result = ltpcom.part1(test, train) + p5[0]
                        if result == 3:
                            c4 = test[2]
                            tc4 = train[2]
                            c5 = test[3]
                            tc5 = train[3]

                            c4 = c4[:-1]
                            tc4 = tc4[:-1]
                            c5 = c5[:-1]
                            tc5 = tc5[:-1]

                            test4 = c4.split("_")
                            train4 = tc4.split("_")
                            test5 = c5.split("_")
                            train5 = tc5.split("_")
                            if len(train4) > 1 and len(test4) > 1 and len(train5) > 1 and len(test5) > 1:
                                # print("train4, test4, train5, test5: ", train4, test4, train5, test5)
                                result_p2 = ltpcom.part2(train4, test4, p5[1])
                                result_p3 = ltpcom.part3(train4, train5, test5, result_p2[3], p5[1])
                                if len(result_p2[5]) > 0 and len(result_p3[3]) > 0:
                                    result1 = result_p2[0] * ltpcom.for_part52(test4, result_p2[1], result_p2[2],
                                                                               result_p2[4], result_p2[5], p5[2])
                                    result2 = result_p3[0] * ltpcom.for_part53(test5, result_p2[4], result_p3[1],
                                                                               result_p3[2], result_p3[3], p5[2])
                                    if result1+result2 >= 1:
                                        panduan = 1
                                        break

                    label.append(panduan)
                print("label: ", label)
                daiset = []
                for i in range(len(label)):
                    if label[i] == 1:
                        daiset.append(daixunlian[i])

                zanshi_set = set(daiset)
                final_content = list(zanshi_set)
                for fc in final_content:

                    print("结果：", fc)
                    ls_huifu.append(fc)


    print("OFF")

    stream.stop_stream()
    stream.close()
    p.terminate()
    if len(ls_huifu)>0:
        huifu = str(ls_huifu[0])
    return huifu



if __name__ == "__main__":
    start_audio(10, 60)
