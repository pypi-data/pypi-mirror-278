import time, yaml
import streamlit as st
import streamlit_authenticator as stauth
import openai

class Container():
    def __init__(self, role, blocks):
        self.container = st.empty()
        self.role = role
        self.blocks = blocks

    def _write_blocks(self):
        with st.chat_message(self.role):
            for block in self.blocks:
                if block['type'] == 'text':
                    st.write(block['content'], unsafe_allow_html=True)
                elif block['type'] == 'code':
                    st.code(block['content'])
                elif block['type'] == 'image':
                    st.image(block['content'])

    def write_blocks(self, stream=False):
        if stream:
            with self.container:
                self._write_blocks()
        else:
            self._write_blocks()

class EventHandler(openai.AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.container = None

    def on_text_delta(self, delta, snapshot):
        if self.container is None:
            self.container = Container("assistant", [])
        if not self.container.blocks or self.container.blocks[-1]['type'] != 'text':
            self.container.blocks.append({'type': 'text', 'content': ""})
        if delta.annotations is not None:
            for annotation in delta.annotations:
                if annotation.type == "file_citation":
                    cited_file = st.session_state.client.files.retrieve(annotation.file_citation.file_id)
                    delta.value = delta.value.replace(annotation.text, f"""<a href="#" title="{cited_file.filename}">[❞]</a>""")
        self.container.blocks[-1]["content"] += delta.value
        self.container.write_blocks(stream=True)

    def on_image_file_done(self, image_file):
        if self.container is None:
            self.container = canu.Container("assistant", [])
        if not self.container.blocks or self.container.blocks[-1]['type'] != 'image':
            self.container.blocks.append({'type': 'image', 'content': ""})
        image_data = st.session_state.client.files.content(image_file.file_id)
        image_data_bytes = image_data.read()
        self.container.blocks[-1]["content"] = image_data_bytes
        self.container.write_blocks(stream=True)

    def on_end(self):
        if self.container is not None:
            st.session_state.containers.append(self.container)

def update_yaml_file():
    with open("./auth.yaml", 'w', encoding="utf-8-sig") as f:
        yaml.dump(st.session_state.config, f, allow_unicode=True)

def authenticate():
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "authenticator" not in st.session_state:
        with open("./auth.yaml") as f:
            config = yaml.load(f, Loader=yaml.loader.SafeLoader)
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
        )
        st.session_state.config = config
        st.session_state.authenticator = authenticator

def add_message(role, content):
    st.session_state.client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role=role,
        content=content
    )
    st.session_state.containers.append(
        Container(role, [{'type': 'text', 'content': content}])
    )

def write_stream(event_handler=None):
    if event_handler is None:
        event_handler = EventHandler()
    with st.session_state.client.beta.threads.runs.stream(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

def show_login_page():
    st.session_state.name, st.session_state.authentication_status, st.session_state.username = st.session_state.authenticator.login(location="main", fields={'Form name':'로그인', 'Username':'아이디', 'Password':'비밀번호', 'Login':'로그인'})
    if st.session_state.authentication_status:
        st.session_state.page = "chatbot"
        st.rerun()
    elif st.session_state.authentication_status is False:
        st.error("아이디 또는 비밀번호가 잘못되었습니다.")
    elif st.session_state.authentication_status is None:
        pass

def show_profile_page():
    if "file_uploader_key" in st.session_state:
        uploaded_files = get_uploaded_files()
    if st.button("돌아가기"):
        st.session_state.page = "chatbot"
        st.rerun()
    if st.session_state.authenticator.reset_password(st.session_state.username, fields={'Form name':'비밀번호 변경', 'Current password':'현재 비밀번호', 'New password':'새로운 비밀번호', 'Repeat password': '새로운 비밀번호 확인', 'Reset':'변경'}):
        st.success("비밀번호가 성공적으로 변경되었습니다.")
        time.sleep(3)
        update_yaml_file()
        st.session_state.page = "chatbot"
        st.rerun()

def get_uploaded_files():
    uploaded_files = st.sidebar.file_uploader(
        "파일 업로드",
        accept_multiple_files=True,
        key=st.session_state.file_uploader_key
    )
    return uploaded_files