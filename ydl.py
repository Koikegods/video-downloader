from yt_dlp import YoutubeDL
import os
import threading


# プレイリスト、チャンネルの動画の一斉ダウンロードもできます。(Youtube)
def gui():
    # guiの作成
    # tkinterのインポート
    import tkinter
    import tkinter as tk
    import tkinter.ttk as ttk

    # 関数の定義
    def dl():
        mp3_mp4 = "none"
        wav_check = "none"
        if not wavs.get():
            mp3_mp4 = "mp3"
            if bln.get():
                mp3_mp4 = "mp4"
        else:
            wav_check = "wav"
        threading.Thread(target=download_video, args=(entry.get(), mp3_mp4, wav_check)).start()
        entry.delete(0, tk.END)

    # rootフレームの設定
    root = tk.Tk()
    root.title("VideoDL")
    root.geometry("250x100")
    root.resizable(0, 0)

    # bln.set(False)
    # フレームの作成と設置
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)
    # 各種ウィジェットの作成
    label = ttk.Label(frame, text="Link：")
    entry = ttk.Entry(frame)
    bln = tkinter.BooleanVar()
    wavs = tkinter.BooleanVar()
    entry.insert(tk.END, "")
    chk = ttk.Checkbutton(frame, variable=bln, text='MP4')
    wav = ttk.Checkbutton(frame, variable=wavs, text='WAV')
    button_execute = ttk.Button(frame, text="Run", command=dl)

    # 各種ウィジェットの設置
    label.grid(row=0, column=0)
    chk.grid(row=1, column=0)
    wav.grid(row=1, column=1)
    entry.grid(row=0, column=1)
    button_execute.grid(row=2, column=1)

    root.mainloop()


def download_video(link, download_mode="none", download_mode_wav="none"):
    # mp3かmp4の条件分岐
    if download_mode == "mp3":
        # titleの取得
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_title = info_dict.get('title', None)
        ydl_opts = {
            'format': 'bestaudio/best',
            #  'outtmpl': f"{os.getcwd()}/video/{video_title}" + '.%(ext)s',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio',
                 'preferredcodec': 'mp3',
                 'preferredquality': '192'},
                {'key': 'FFmpegMetadata'},
            ],
        }
        # download
        ydl = YoutubeDL(ydl_opts)
        ydl.extract_info(f"{link}", download=True)
    # mp3かmp4の条件分岐
    elif download_mode == "mp4":
        # titleの取得
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_title = info_dict.get('title', None)
        ydl_opts = {

            #    'outtmpl': f"{os.getcwd()}/video/{video_title}" + '.%(ext)s',
            'format': 'best+mp4'
        }
        # download
        ydl = YoutubeDL(ydl_opts)
        ydl.download(link)
    if download_mode_wav == "wav":
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio',
                 'preferredcodec': 'wav',
                 'preferredquality': '192'},
                {'key': 'FFmpegMetadata'},
            ],
        }
        # download
        ydl = YoutubeDL(ydl_opts)
        ydl.download(link)


if __name__ == '__main__':
    gui()
