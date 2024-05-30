import 'package:flutter/material.dart';
import 'package:my_new_app/services/api_service.dart';
import 'Register_1.dart';
import 'AdminScreen.dart'; // 관리자 화면 import (예시, 실제 파일 경로에 맞게 수정)

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _IDController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  Future<void> _login() async {
    String id = _IDController.text;
    String password = _passwordController.text;

    var response = await loginUser(id, password);

    if (response['message'].startsWith('Meal provided')) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(response['message'])),
      );
      await Future.delayed(Duration(seconds: 5));
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => LoginScreen()),
      );
    } else if (response['message'].startsWith('Meal capacity')) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(response['message'])),
      );
      await Future.delayed(Duration(seconds: 5));
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => LoginScreen()),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(response['message'])),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: IconThemeData(color: Colors.black), // 뒤로가기 버튼 색상 설정
        elevation: 0, // 구분선 제거
        actions: <Widget>[
          IconButton(
            icon: Icon(Icons.admin_panel_settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => AdminScreen()),
              );
            },
            color: Colors.black, // 아이콘 색상 설정
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
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
                  backgroundColor: Colors.black, // 검은색 배경
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
                  backgroundColor: Colors.transparent, // 투명 배경
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
