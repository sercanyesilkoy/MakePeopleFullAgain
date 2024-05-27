import 'package:flutter/material.dart';
import 'Login.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MakePeopleFullAgain',
      theme: ThemeData(
        primarySwatch: Colors.grey,
        primaryColor: Colors.black,
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.white,
          titleTextStyle: TextStyle(
            color: Colors.black, // AppBar의 제목 텍스트의 색을 검은색으로 지정
            fontSize: 30, // 폰트 크기 30px
          ),
        ),
        scaffoldBackgroundColor: Colors.white,
        colorScheme: ColorScheme.fromSwatch(
          accentColor: Colors.black, // 액센트 색상을 검은색으로 설정
        ),
        // 나머지 테마 속성들을 여기에 추가할 수 있습니다.
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MakePeopleFullAgain'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const LoginScreen()),
            );
          },
          child: const Text('Login / Register'),
        ),
      ),
    );
  }
}
