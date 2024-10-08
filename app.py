from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', error="URL không hợp lệ hoặc không được cung cấp")
    
    try:
        # Kiểm tra URL
        yt = YouTube(url)
        
        # Lấy video với độ phân giải tốt nhất
        stream = yt.streams.get_highest_resolution()
        
        # Tạo thư mục tải xuống nếu chưa tồn tại
        output_path = 'downloads'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Đặt đường dẫn tệp video
        file_path = os.path.join(output_path, 'video.mp4')
        
        # Tải video
        stream.download(output_path=output_path, filename='video.mp4')
        
        # Trả về tệp video để tải xuống
        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        # Ghi lại lỗi và trả về thông báo lỗi cho người dùng
        error_message = f"Lỗi xảy ra: {str(e)}"
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True, host='0.0.0.0')
