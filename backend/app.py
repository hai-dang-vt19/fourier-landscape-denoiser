"""
Flask API server cho hệ thống xử lý ảnh với biến đổi Fourier
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image

from core.image_processor import ImageProcessor
from utils.validation import validate_processing_params, validate_image_file
from utils.image_io import read_image, save_image, convert_bgr_to_rgb

app = Flask(__name__)
CORS(app)

# Cấu hình
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Tạo thư mục nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Kiểm tra extension file có được phép không"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_base64(image: np.ndarray) -> str:
    """Chuyển đổi numpy array thành base64 string"""
    # Chuyển BGR sang RGB nếu cần
    if len(image.shape) == 3 and image.shape[2] == 3:
        image_rgb = convert_bgr_to_rgb(image)
    else:
        image_rgb = image
    
    # Chuyển sang PIL Image
    if len(image_rgb.shape) == 2:
        pil_image = Image.fromarray(image_rgb, mode='L')
    else:
        pil_image = Image.fromarray(image_rgb, mode='RGB')
    
    # Chuyển sang base64
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server đang hoạt động'})


@app.route('/api/process', methods=['POST'])
def process_image():
    """
    Xử lý ảnh với bộ lọc Fourier
    
    Request body:
    - image: base64 encoded image hoặc file upload
    - filter_type: 'ideal', 'butterworth', 'gaussian'
    - filter_mode: 'lowpass', 'highpass', 'bandreject'
    - cutoff: float (tần số cắt)
    - order: int (bậc bộ lọc, mặc định 2)
    - center_freq: float (cho band-reject, optional)
    - bandwidth: float (cho band-reject, optional)
    """
    print("=== Received /api/process request ===")
    print(f"Content-Type: {request.content_type}")
    print(f"Has files: {'image' in request.files}")
    print(f"Has json: {request.is_json}")
    try:
        # Lấy tham số
        filter_type = request.form.get('filter_type', 'gaussian').lower()
        filter_mode = request.form.get('filter_mode', 'lowpass').lower()
        cutoff = float(request.form.get('cutoff', 50.0))
        order = int(request.form.get('order', 2))
        center_freq = request.form.get('center_freq')
        bandwidth = request.form.get('bandwidth')
        
        center_freq = float(center_freq) if center_freq else None
        bandwidth = float(bandwidth) if bandwidth else None
        
        # Validate tham số
        is_valid, error_msg = validate_processing_params(
            filter_type, filter_mode, cutoff, order, center_freq, bandwidth
        )
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Lấy ảnh từ request
        image_data = None
        
        # Thử lấy từ file upload
        if 'image' in request.files:
            print("Reading image from file upload...")
            file = request.files['image']
            if file and file.filename:  # Có filename
                if not allowed_file(file.filename):
                    return jsonify({'error': 'Định dạng file không được phép'}), 400
            # Đọc ảnh từ file (có thể không có filename nếu là blob)
            file_bytes = file.read()
            print(f"File size: {len(file_bytes)} bytes")
            if len(file_bytes) == 0:
                return jsonify({'error': 'File rỗng'}), 400
            nparr = np.frombuffer(file_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                return jsonify({'error': 'Không thể đọc ảnh từ file. Có thể file không phải là ảnh hợp lệ.'}), 400
            print(f"Image decoded successfully. Shape: {image.shape}")
        
        # Thử lấy từ base64
        elif 'image' in request.json:
            image_base64 = request.json['image']
            if image_base64.startswith('data:image'):
                # Bỏ qua data URL prefix
                image_base64 = image_base64.split(',')[1]
            
            image_bytes = base64.b64decode(image_base64)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                return jsonify({'error': 'Không thể đọc ảnh từ base64'}), 400
        
        else:
            return jsonify({'error': 'Không tìm thấy ảnh trong request'}), 400
        
        # Xử lý ảnh
        print(f"Processing image with filter_type={filter_type}, filter_mode={filter_mode}, cutoff={cutoff}")
        processor = ImageProcessor()
        processor.load_image_from_array(image)
        
        print("Starting image processing...")
        processed_image = processor.process_image(
            filter_type=filter_type,
            filter_mode=filter_mode,
            cutoff=cutoff,
            order=order,
            center_freq=center_freq,
            bandwidth=bandwidth
        )
        print("Image processing completed")
        
        # Lấy các thông tin bổ sung
        magnitude_spectrum = processor.get_magnitude_spectrum_image()
        filter_mask = processor.get_filter_mask_image()
        metrics = processor.get_metrics()
        
        # Chuyển đổi sang base64
        original_base64 = image_to_base64(image)
        processed_base64 = image_to_base64(processed_image)
        magnitude_base64 = image_to_base64(magnitude_spectrum)
        mask_base64 = image_to_base64(filter_mask)
        
        return jsonify({
            'success': True,
            'original_image': original_base64,
            'processed_image': processed_base64,
            'magnitude_spectrum': magnitude_base64,
            'filter_mask': mask_base64,
            'metrics': metrics
        })
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in process_image: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500


@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Upload ảnh lên server"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Không có file ảnh'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Không có file được chọn'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Đọc ảnh để trả về preview
            image = read_image(filepath)
            image_base64 = image_to_base64(image)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'preview': image_base64
            })
        else:
            return jsonify({'error': 'Định dạng file không được phép'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Lỗi upload: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

