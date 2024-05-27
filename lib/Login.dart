import 'package:flutter/material.dart';
import 'Register_1.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _IDController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  int remainingQuantity = 100; // 남은 수량 변수 추가

  void _login() {
    // 로그인 로직을 구현하세요.
    print('ID: ${_IDController.text}');
    print('Password: ${_passwordController.text}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: IconThemeData(color: Colors.black), // 뒤로가기 버튼 색상 설정
        elevation: 0, // 구분선 제거
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Remaining Quantity',
              style: TextStyle(
                color: Colors.black, // 검은색 글씨
                fontSize: 24, // 폰트 크기
              ),
            ),
            const SizedBox(height: 20),
            Container(
              width: 148,
              height: 40,
              padding: const EdgeInsets.all(0),
              child: Center(
                child: Text(
                  '$remainingQuantity',
                  style: TextStyle(
                    color: Colors.black, // 검은색 글씨
                    fontSize: 30, // 폰트 크기 30px
                  ),
                ),
              ),
            ),
            Container(
              height: 50, // 높이 설정
              padding: const EdgeInsets.all(0),
              child: Center(
                child: Text(
                  '주문이 성공적으로 완료되었습니다.',
                  style: TextStyle(
                    color: Colors.black, // 검은색 글씨
                    fontSize: 15, // 폰트 크기
                  ),
                ),
              ),
            ),
            Text(
              'Log in',
              style: TextStyle(
                color: Colors.black, // 검은색 글씨
                fontSize: 36, // 폰트 크기
              ),
            ),
            SizedBox(height: 20),
            Container(
              width: 343,
              height: 52,
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.black,
                  width: 2.0, // 테두리 두께
                ),
                borderRadius: BorderRadius.circular(0), // 둥근 테두리 제거
              ),
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _IDController,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  labelText: 'ID',
                  contentPadding: EdgeInsets.zero,
                  labelStyle: TextStyle(color: Colors.black), // 검은색 글씨
                ),
              ),
            ),
            const SizedBox(height: 12),
            Container(
              width: 343,
              height: 52,
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.black,
                  width: 2.0,
                ),
                borderRadius: BorderRadius.circular(0),
              ),
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _passwordController,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  labelText: 'Password',
                  contentPadding: EdgeInsets.zero,
                  labelStyle: TextStyle(color: Colors.black), // 검은색 글씨
                ),
                obscureText: true,
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: 343,
              height: 52,
              child: ElevatedButton(
                onPressed: _login,
                style: ElevatedButton.styleFrom(
                  primary: Colors.black, // 검은색 배경
                  padding: EdgeInsets.zero,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(6), // 2의 radius 적용
                    side: BorderSide(color: Colors.black, width: 2.0),
                  ),
                  textStyle: TextStyle(color: Colors.white), // 흰색 글씨
                ),
                child: const Text('LOG IN'),
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: 343,
              height: 20,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => RegisterScreen1()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  primary: Colors.transparent, // 투명 배경
                  shadowColor: Colors.transparent, // 그림자 효과 없음
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.zero,
                  ),
                ),
                child: Text(
                  'Register',
                  style: TextStyle(
                    color: Colors.black, // 검은색 글씨
                    fontSize: 15, // 폰트 크기
                  ),
                ),
              ),
            ),
            SizedBox(height: 20),
            Container(
              width: 343,
              padding: EdgeInsets.all(0),
              child: Text(
                '회원이 아닙니다. 가입을 진행해주세요.',
                style: TextStyle(
                  color: Colors.red, // 검은색 글씨
                  fontSize: 15, // 폰트 크기
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
