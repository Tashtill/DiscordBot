requirements.txtにはvenv内のパッケージが入っている。
これは以下のコマンドで取得可能
pip freeze > requirements.txt
これらを他の他のPCの環境にインストールする際は以下のコマンドを実行する
pip install -r requirments.txt