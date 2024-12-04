USE db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO usuarios (username, password) VALUES
('lQNZ', '06j31Os1'),
('LmYy', 'VTTvaQqu'),
('rPUU', 'fDbmtFYu'),
('eAZQ', 'Fp9jwO1W'),
('mFrH', 'ho7euEZE'),
('OBqL', 'fwL0Jzay'),
('nMRI', 'Ak8wtOE8'),
('ToNS', 'n3Xbl3Kp'),
('uxOQ', 'RxQfV8U0'),
('pbIk', 'xkz7qNsL'),
('HKtT', '66s0sXOu'),
('XubY', 'AS7kovIq'),
('ZDGy', 'wJwFA7ru'),
('xAmX', 'lu6eLVme'),
('IOCs', 'Pkx6PdUB'),
('aYZy', 'fYJ92nrl'),
('deZu', 'u46veLOQ'),
('UHky', '8lqRqRjX'),
('jtlL', 'cGyZCmSd'),
('blNo', '0XAj3Edi'),
('EbMS', 'rUPpNvfj'),
('ijTB', 'w1VVbTj3'),
('mUUo', 'myV3m4XA'),
('LWQK', '4xbdJZLx'),
('nzOH', '8QomWlRw'),
('MWKi', 'czHJD8B6'),
('Nbdm', 'SVzc4bYW'),
('IyhW', 'yL5Mn7mf'),
('ulvR', 'joOzYJcq'),
('dTHf', 'K60MNE8e'),
('MLcR', 'Fd1aAbru'),
('wEJN', '1UMy8Q93'),
('cKzD', 'dCboBQwS'),
('NBLY', 'oONh3LeU'),
('pNce', 'ht3Zklyy'),
('COyN', 'UUEAEb2W'),
('WqOm', 'XDhlovjO'),
('KXyp', 'bP3h6QDZ'),
('Qsyu', 'IfeUSOzQ'),
('iwdp', 'OtvyTJlV'),
('VgMY', 'B5yYTXF3'),
('YUHP', '05tNHkSx'),
('shZp', 'VFJ7VZdz'),
('lIgc', 'BdlKkjJd'),
('pQkP', 'QnwjnkiL'),
('PWYW', '3j8p3Oy6'),
('ekLx', 'AMYeD66Y'),
('Pytr', 'xr10BpXh'),
('KAVc', 'uwaBokP9'),
('RyAA', 'wR183wv3');

CREATE TABLE IF NOT EXISTS flags (
    flag VARCHAR(255) NOT NULL
);

COMMIT;e