from flask import Blueprint, redirect, render_template, request, jsonify, current_app, session
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from flask_app import db
from .utils import assistant
from flask_app.models import Users, Chats
import os
from openai import OpenAI



bp = Blueprint('chat', __name__)

@bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    user_id = current_user.get_id()

    if request.method == 'GET':
        return render_template('chat/chat.html', user_id=user_id)

    if request.method == 'POST':
        user_message = request.form.get('message')
        user_file = request.files.get('file')
        upload_folder = current_app.config['UPLOAD_PATH']

        file_message = None
        file_path = None

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if user_file:
            try:
                file_name = secure_filename(user_file.filename)
                file_path = os.path.join(upload_folder, file_name)
                user_file.save(file_path)
                session['file_path'] = file_path
                file_message = 'File uploaded successfully'
            
            except Exception as e:
                file_message = f'File upload failed: {str(e)}'
        elif len(os.listdir(upload_folder)) == 0:
            file_message = 'No file uploaded'
        else:
            file_path = session.get('file_path')
            if not file_path:
                file_message = 'No previous file found'
        
        if file_message:
            return jsonify({"message": file_message})

        # Instantiate the Assistant
        client = OpenAI(api_key = current_app.config['API_KEY'])
        chatbot = assistant.Assistant(client, file_path)
        session['assistant_id'] = chatbot.create_assistant()

        # Check if thread_id exists in session
        thread_id = session.get('thread_id')

        if user_message:
            if not thread_id:
                # Create a new thread if no thread_id in session
                thread = client.beta.threads.create()
                session['thread_id'] = thread.id
            else:
                thread = client.beta.threads.retrieve(thread_id)
            
            run = chatbot.run_thread(session.get('thread_id'), session.get('assistant_id'), user_message)

            run = chatbot.wait_on_run(run, thread)
            bot_message, conversation = chatbot.get_assistant_message(thread)

            # Record data into the database
            chat = Chats(uid=user_id, thread_id=thread.id, user_input=user_message, bot_input=bot_message)
            db.session.add(chat)
            db.session.commit()

            return jsonify({"message": conversation})

@bp.route('/clear_thread_id', methods=['POST'])
def clear_thread_id():
    session.pop('thread_id', None)
    return '', 204

@bp.route('/url_helper', methods=['GET', 'POST'])
@login_required
def url_helper():
    user_id = current_user.get_id()

    if request.method == 'GET':
        return render_template('chat/url_helper.html', user_id=user_id)

    if request.method == 'POST':
        url_list = request.form['urls']

        # Initialize URL_helper
        client = OpenAI(api_key = current_app.config['API_KEY'])
        url_helper = assistant.URL_helper(client, url_list)
        response = url_helper.webpage_reader()
        response_formatted = url_helper.formatted_output(response)

        return jsonify({"formatted_output": response_formatted})
