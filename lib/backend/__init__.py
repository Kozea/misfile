from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG', silent=True)
if not app.config.get('MISFILE_DIR'):
    raise ValueError('MISFILE_DIR must be set')
misfile_path = Path(app.config['MISFILE_DIR'])

if not app.config.get('ALLOWED_MISFILES'):
    raise ValueError('ALLOWED_MISFILES must be set')
allowed_files = app.config['ALLOWED_MISFILES'].split(',')

if not misfile_path.exists():
    misfile_path.mkdir(parents=True, exist_ok=True)

if not misfile_path.is_dir():
    raise TypeError('MISFILE_DIR must be a directory')


@app.route('/')
def index():
    length = len([None for _ in misfile_path.glob('*')])
    return f'<h1>Misfile</h1><p>Misfile has misfiled {length} files.</p>'


@app.route('/add/<filename>', methods=['POST'])
def add(filename):
    if not len(request.data):
        return jsonify(
            {'status': 'error', 'message': 'File must not be empty.'}
        )

    if '.' not in filename:
        return jsonify(
            {'status': 'error', 'message': 'File must have an extension.'}
        )

    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in allowed_files:
        return jsonify({'status': 'error', 'message': 'File not allowed.'})

    for i in range(10):
        uid = (
            f'{uuid4().hex}{uuid4().hex}{uuid4().hex}{uuid4().hex}.{extension}'
        )
        if not (misfile_path / uid).exists():
            break
    else:
        return jsonify(
            {
                'status': 'error',
                'message': 'Unable to generate unique identifier',
            }
        )

    with open(misfile_path / uid, 'wb') as new_file:
        new_file.write(request.data)

    return jsonify({'status': 'success', 'filename': uid})


if app.debug:

    @app.route('/get/<filename>')
    def get(filename):
        return send_from_directory(misfile_path, filename)

    @app.route('/test')
    def test():
        with open(Path(__file__).parent / 'test.html') as test:
            return test.read()
