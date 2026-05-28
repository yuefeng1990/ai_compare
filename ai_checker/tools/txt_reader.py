class TxtReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.keywords = []
    
    def read_keywords(self):
        """读取TXT文件中的关键字"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.keywords = [line.strip() for line in file.readlines() if line.strip()]
            return self.keywords
        except Exception as e:
            raise Exception(f"读取TXT文件失败: {str(e)}")
    
    def get_keywords(self):
        """获取关键字列表"""
        if not self.keywords:
            self.read_keywords()
        return self.keywords