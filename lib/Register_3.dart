import 'package:flutter/material.dart';
import 'Login.dart';

class RegisterScreen3 extends StatefulWidget {
  const RegisterScreen3({Key? key}) : super(key: key);

  @override
  _RegisterScreen3State createState() => _RegisterScreen3State();
}

class _RegisterScreen3State extends State<RegisterScreen3> {
  final TextEditingController _numberController = TextEditingController();

  void _saveNumber() {
    // 주민등록번호를 저장하는 로직을 구현하세요.
    String number = _numberController.text;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: IconThemeData(color: Colors.black),
        elevation: 0,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text(
              'Register',
              style: TextStyle(
                color: Colors.black,
                fontSize: 36,
              ),
            ),
            const SizedBox(height: 20),
            Container(
              width: 343,
              height: 74, // 두 개의 컨테이너를 감싸는 높이
              child: Column(
                children: [
                  Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                      border: Border(
                        bottom: BorderSide(
                          color: Colors.black,
                          width: 2.0,
                        ),
                      ),
                    ),
                    padding: const EdgeInsets.symmetric(horizontal: 2.0),
                    alignment: Alignment.centerLeft,
                    child: Text(
                      '주민등록번호',
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  Container(
                    width: double.infinity,
                    height: 52, // 입력 박스의 높이
                    decoration: BoxDecoration(
                      border: Border(
                        left: BorderSide(
                          color: Colors.black,
                          width: 2.0,
                        ),
                        right: BorderSide(
                          color: Colors.black,
                          width: 2.0,
                        ),
                        bottom: BorderSide(
                          color: Colors.black,
                          width: 2.0,
                        ),
                      ),
                    ),
                    padding: const EdgeInsets.only(left: 8.0),
                    child: TextField(
                      controller: _numberController,
                      decoration: InputDecoration(
                        border: InputBorder.none,
                        hintText: 'Enter your resident registration number',
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 42),
            SizedBox(
              width: 343,
              height: 52,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => LoginScreen()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  primary: Colors.black,
                  padding: EdgeInsets.zero,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(6),
                    side: BorderSide(color: Colors.black, width: 2.0),
                  ),
                  textStyle: TextStyle(color: Colors.white),
                ),
                child: const Text('SIGN UP'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
