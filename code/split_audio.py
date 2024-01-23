from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
import os

def spl_audio(dizhi, name, min_len_silence, luyinshijian):
    sound = AudioSegment.from_wav(dizhi + name + ".wav")
    loudness = sound.dBFS
    #print("loundness:", loudness)

    chunks = split_on_silence(sound, min_silence_len=min_len_silence, silence_thresh=loudness*1.3, keep_silence=0)
    if len(chunks) > 1:
        for i, chunk in enumerate(chunks):
            if i == len(chunks)-1:
                chunk.export(dizhi + name + "_-1.wav", format("wav"))
                break
            chunk.export(dizhi + name + "_{}.wav".format(i), format("wav"))
        os.remove(dizhi + name + ".wav")

    if len(chunks) == 1:
        if "-1" not in str(name):
            chunks[0].export(dizhi + name + "_-1.wav", format("wav"))
            os.remove(dizhi + name + ".wav")

    #qianpin = 0
    #houpin = 0
    timestamp_list = detect_nonsilent(sound, min_silence_len=min_len_silence, silence_thresh=loudness*1.3, seek_step=1)
    #if timestamp_list[0][0] <= min_len_silence:
        #qianpin = timestamp_list[0][0]
    #if timestamp_list[-1][1] >= sound.duration_seconds - min_len_silence:
        #houpin = luyinshijian - timestamp_list[-1][1]

    print("timestamp_list:", timestamp_list)
    #print("qianpin:", qianpin)
    #print("houpin:", houpin)
    #return([qianpin, houpin])

if __name__ == "__main__":
    spl_audio('D:/django-try/emd/xitong/first_save/', '0', 1000, 10000)