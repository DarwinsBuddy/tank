import os

from flask import send_from_directory, request, jsonify, render_template

from tank.config import AppConfig
from tank.storage import InMemoryStore


def setup(app, store: InMemoryStore, config: AppConfig):
    def _corsify_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        print(app.static_folder)
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    @app.route('/history')
    def history():
        limit = int(request.args.get('limit')) or config.MAX_HISTORY_DATA
        print("LIMIT: ", limit)
        response = {'history': store.get_history(limit)}
        return _corsify_actual_response(jsonify(response))

    @app.route('/ws-test')
    def ws_test(self):
        return render_template('ws.html', sync_mode=self.socket.async_mode)
