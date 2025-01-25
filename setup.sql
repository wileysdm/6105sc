-- 创建用户表
CREATE TABLE account (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    nickname TEXT NOT NULL,
    reviewer BOOLEAN,
    author BOOLEAN
);

-- 创建论文表
CREATE TABLE paper (
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    DID TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    keywords TEXT NOT NULL
);

-- 创建作者论文关系表
CREATE TABLE paper_author (
    DID TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (DID) REFERENCES paper (DID),
    FOREIGN KEY (author_id) REFERENCES account (account_id)
);

-- 插入测试数据
INSERT INTO account (password, nickname, reviewer, author) VALUES
('attention123', 'Vaswani', 1, 1),
('deep123', 'Shazeer', 1, 1),
('learning123', 'Parmar', 0, 1),
('example123', 'Alice', 0, 1),
('test123', 'Bob', 1, 0);

INSERT INTO paper (title, abstract, DID, keywords) VALUES
('Attention Is All You Need', 
 'This paper introduces the Transformer model, a novel architecture for NLP tasks.', 
 'DID_ATTENTION', 
 'Transformer, NLP, Attention'),
('Deep Learning', 
 'An overview of deep learning techniques and their applications in various fields.', 
 'DID_DEEP', 
 'Deep Learning, Neural Networks');


INSERT INTO paper_author (DID, author_id) VALUES
('DID_ATTENTION', 1), -- Vaswani
('DID_ATTENTION', 2), -- Shazeer
('DID_ATTENTION', 3), -- Parmar
('DID_DEEP', 4),      -- Alice
('DID_DEEP', 1);      -- Vaswani
