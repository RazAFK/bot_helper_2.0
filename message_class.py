class Parsed_message:
    def __init__(self, id: int, theme_id: int, sender: int, receiver: int, content_ids: list, caption: str, send_time, comand: int, msg_type: int, parsed: bool, media_group_id: int):
        self.id = id
        self.theme_id = theme_id
        self.sender = sender
        self.receiver = receiver
        self.content_ids = content_ids
        self.caption = caption
        self.send_time = send_time
        self.comand = comand
        self.msg_type = msg_type
        self.parsed = parsed
        self.media_group_id = media_group_id
    
    def __eq__(self, media_group_id):
        return self.media_group_id == media_group_id
    
    def __str__(self):
        return f'{self.id, self.theme_id, self.sender, self.receiver, self.content_ids, self.caption}'
    
    def add_id(self, id):
        self.content_ids.append(id)