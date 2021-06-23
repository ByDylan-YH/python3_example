from flask import Flask, request;
import time;
import json;

app = Flask(__name__);


@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        _txtName = '%s_%s.txt' % (request.remote_addr,
                                  time.strftime('%Y%m%d%H%M%S', time.localtime()));
        with open(_txtName, 'w', encoding='utf-8') as f:
            f.writelines(json.loads(request.data));
    return "小哥，里面玩儿啊";


if __name__ == '__main__':
    # 端口可自行设置,这里必须写自己IP
    app.run(host='192.168.1.101', port=9999, debug=True);
