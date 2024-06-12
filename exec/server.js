const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

// 웹 서버에 엔드포인트 추가 : Express 앱에 엔드포인트를 추가해 정답을 비교할 수 있도록 한다
app.post('/check-answer', (req, res) => {
  const receivedCode = req.body.code; // 백엔드 서버로부터 받은 파이썬 코드
  const answerCode = fs.readFileSync('/home/user/answer.py', 'utf-8'); // 정답 코드 파일 읽기
  if (receivedCode === answerCode) {
    res.send({ result: '정답' });
  } else {
    res.send({ result: '오답' });
  }
});
